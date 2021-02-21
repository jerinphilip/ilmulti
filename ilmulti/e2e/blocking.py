from ..utils.language_utils import inject_token

class BlockingTranslator:
    """
    A blocking translator.
    """
    def __init__(self, translator, splitter, tokenizer):
        self.splitter = splitter
        self.tokenizer = tokenizer
        self.translator = translator

    def __call__(self, source, tgt_lang, src_lang=None, detokenize=True):
        """
        Uses splitter -> tokenizer -> translator and lays out the
        interaction.
        """
        lang, lines = self.splitter(source, lang=src_lang)
        sources = []
        for line in lines:
            lang, tokens = self.tokenizer(line, lang=src_lang)
            tokenized_lines = ' '.join(tokens)
            sources.append(tokenized_lines)

        with_target_token = inject_token(sources, tgt_lang=tgt_lang)
        export = self.translator(with_target_token)
        export = self._handle_empty_lines_noise(export)
        if detokenize:
            export = self._detokenize(export)
        return export

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
