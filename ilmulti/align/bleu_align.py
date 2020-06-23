from io import StringIO
from bleualign.align import Aligner
from ilmulti.utils.language_utils import inject_token

class BLEUAligner:
    def __init__(self, model, tokenizer, segmenter):
        self.model = model
        self.tokenizer = tokenizer
        self.segmenter = segmenter

    def __call__(self, src, src_lang, tgt, tgt_lang):
        """
            Input: Paragraphs in two languages and their language codes.
            Output: Obtained parallel sentences using BLEUAlign

        """
        def create_stringio(lines, lang):
            tokenized = [ ' '.join(self.tokenizer(line, lang=lang)[1]) \
                    for line in lines ]
            lstring = '\n'.join(tokenized)
            return tokenized, StringIO(lstring)

        def process(content, lang):
            lang, segments = self.segmenter(content, lang=lang)
            tokenized, _io = create_stringio(segments, lang)
            return tokenized, _io

        src_tokenized, src_io = process(src, src_lang)
        tgt_tokenized, tgt_io = process(tgt, tgt_lang)

        # Inject tokens into src_tokenized
        injected_src_tokenized = inject_token(src_tokenized,tgt_lang)

        # Processing using src_tokenized to get translations
        # TODO(shashank) accumulate list
        generation_output = self.model(injected_src_tokenized)

        hyps = [ gout['tgt'] for gout in generation_output ]

        #hyp_tokenized, hyp_io = create_stringio(hyps, tgt_lang)
        hyps = '\n'.join(hyps)
        hyp_io = StringIO(hyps)

        return self.bleu_align(src_io, tgt_io, hyp_io)

    def bleu_align(self, srcfile, tgtfile, hyp_src_tgt_file):
        output = StringIO()
        # src_out, tgt_out = StringIO(), StringIO()
        options = {
            'verbosity': 0,
            'srcfile': srcfile,
            'targetfile': tgtfile,
            'srctotarget': [hyp_src_tgt_file],
            'targettosrc': [],
            # 'output': output,
            # 'output-src': src_out, 'output-target': tgt_out,
	}

        a = Aligner(options)
        a.mainloop()
        src_out, tgt_out = a.results()
        srcs = src_out.getvalue().splitlines()
        tgts = tgt_out.getvalue().splitlines()
        return srcs, tgts
