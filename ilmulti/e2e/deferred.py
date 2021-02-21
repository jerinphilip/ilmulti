from ..utils.language_utils import inject_token
from ..utils.storage import LMDBStorage

class DeferredTranslator:
    """
    Special mode of packaged translation task to optimize decoding over several
    requests. Add requests, which are preprocessed and stored in storage. 

    This solves an unnecessary problem where one does not want crashes because of
    memory, but still speed. Should be able to change Storage to RAM/SSD for
    faster IO, by adjusting Storage class.

    """
    def __init__(self, translator, splitter, tokenizer, storage, max_tokens):
        """
        :param translator fairseq translator instance
        :param splitter   sentence-splitter instance
        :param tokenizer  tokenizer instance
        """
        self.splitter = splitter
        self.tokenizer = tokenizer
        self.translator = translator
        self.storage = storage
        self.max_tokens = max_tokens
        self.sizes = {}
        self.lines = {}

    def queue(self, Id, source, tgt_lang, src_lang=None):
        """
        Queues a request identified by ``(Id, Source)``. Does not translate
        immediately, preprocesses for optimal batch allocation. 
        """
        lang, lines = self.splitter(source, lang=src_lang)

        # Keep account of how many lines we have.
        self.lines[Id] = len(lines)

        for line_id, line in enumerate(lines):
            lang, tokens = self.tokenizer(line, lang=src_lang)
            line_num_tokens = len(tokens) + 1  # accounting of injected
            tokenized_line = ' '.join(tokens)
            key = '{}-{}'.format(Id, line_id)
            self.sizes[key] = line_num_tokens
            with_target_token = inject_token([tokenized_line], tgt_lang)
            self.storage.set_source(key, with_target_token[0])

    def run(self, detokenize=True):
        """
        Runs the translation after all the requests are in. Blocks until all
        the requests have finished translating.
        """

        # Translate batches, set to lmdb.
        for batch in get_batches(self.storage, self.sizes, self.max_tokens):
            export = self.translator(batch['sources'], detokenize)
            for Id, entry in zip(batch['ids'], export):
                transform = lambda x: self.tokenizer.detokenize(x) if detokenize else lambda x: x
                self.storage.set_target(Id, transform(entry['tgt']))

    def collect(self, Id):
        """
        Used by the client to collect translation for each request identified
        by ``Id`` once ``run()`` finishes translations.
        """
        translations = []
        for line_id in range(self.lines[Id]):
            key = '{}-{}'.format(Id, line_id)
            translation = self.storage.get_target(key)
            translations.append(translation)

        return '\n'.join(translations)

    def _handle_empty_lines_noise(self, exports):
        _exports = []
        for entry in exports:
            if not entry['src'].strip():
                entry['tgt'] = ''
            _exports.append(entry)
        return _exports


    def _detokenize(self, export):
        _exports = []
        for entry in export:
            for key in ['src', 'tgt']:
                entry[key] = self.tokenizer.detokenize(entry[key])
            entry['src'] = entry['src'][9:]
            _exports.append(entry)
        return _exports

    @classmethod
    def fromBlocking(cls, blocking_translator, storage, max_tokens):
        return cls(blocking_translator.translator, blocking_translator.splitter, blocking_translator.tokenizer, storage, max_tokens)

def get_batches(storage, sizes, max_tokens):
    tuples = list(sizes.items())
    # sort on the basis of length
    sorted_tuples = sorted(tuples, key=lambda x: x[1])
    sources = []
    Ids = []
    current_tokens = 0

    for candidate in sorted_tuples:
        Id, current_size = candidate

        if current_size * (len(sources) + 1) <= max_tokens:
            source = storage.get_source(Id)
            sources.append(source)
            Ids.append(Id)
            current_tokens += current_size

        else:
            yield {'sources': sources, 'ids': Ids}
            # Reset
            sources.clear()
            Ids.clear()
            current_tokens *= 0

            source = storage.get_source(Id)
            sources.append(source)
            Ids.append(Id)
            current_tokens += current_size

    if sources:
        yield {'sources': source, 'ids': Ids}
