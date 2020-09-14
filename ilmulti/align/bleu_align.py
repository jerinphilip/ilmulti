from io import StringIO
from bleualign.align import Aligner
from ilmulti.utils.language_utils import inject_token

class BLEUAligner:
    def __init__(self, model, tokenizer, segmenter):
        self.model = model
        self.tokenizer = tokenizer
        self.segmenter = segmenter

    def __call__(self, src, src_lang, tgt, tgt_lang, galechurch=False):
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
            missing_idxs = []
            for idx, segment in enumerate(segments):
                if not segment.strip():
                    missing_idxs.append(idx)

            tokenized, _io = create_stringio(segments, lang)
            return tokenized, _io, missing_idxs

        src_tokenized, src_io, missing_idxs = process(src, src_lang)
        tgt_tokenized, tgt_io, _ = process(tgt, tgt_lang)

        if galechurch==True:
            src, tgt = self.bleu_align(src_io, tgt_io, hyp_src_tgt_file=None)
            return ([], []) , (src, tgt)

        # Inject tokens into src_tokenized
        injected_src_tokenized = inject_token(src_tokenized, tgt_lang)

        generation_output = self.model(injected_src_tokenized)
        hyps = [ gout['tgt'] for gout in generation_output ]

        # Remove missing idxs.
        for idx in missing_idxs:
            hyps[idx] = ''

        hyp_io = StringIO('\n'.join(hyps))

        src, tgt = self.bleu_align(src_io, tgt_io, hyp_io)

        return (src_tokenized, hyps), (src, tgt) 



    def bleu_align(self, srcfile, tgtfile, hyp_src_tgt_file=None):
        output = StringIO()
        options = {
            'srcfile': srcfile,
            'targetfile': tgtfile,
            'galechurch' : True if hyp_src_tgt_file is None else False,
            'no_translation_override':True if hyp_src_tgt_file is None else False,
            'srctotarget': [hyp_src_tgt_file] if hyp_src_tgt_file else [],
            'targettosrc': [],
            'verbosity' : 0,
	   }

        a = Aligner(options)
        a.mainloop()
        src_out, tgt_out = a.results()

        srcs = src_out.getvalue().splitlines()
        tgts = tgt_out.getvalue().splitlines()

        return srcs, tgts

    def bleu_align_from_raw(self, src_content, tgt_content, src_to_tgt_content=None, preprocess=False, src_lang=None, tgt_lang=None):
        """
        Wrapper for easier access.
        """

        def preprocess_fn(content, lang):
            _lang, segments = self.segmenter(content, lang)
            tokenized_segments = []
            for segment in segments:
                _lang, tokenized_segment = self.tokenizer(segment, lang)
                joined = ' '.join(tokenized_segment)
                tokenized_segments.append(joined)
            return '\n'.join(tokenized_segments)



        if preprocess:
            src_content = preprocess_fn(src_content, src_lang)
            tgt_content = preprocess_fn(tgt_content, tgt_lang)
            if src_to_tgt_content:
                src_to_tgt_content = preprocess_fn(src_to_tgt_content, tgt_lang)

        srcfile = StringIO(src_content)
        tgtfile = StringIO(tgt_content)
        if src_to_tgt_content:
            src_to_tgt_content = StringIO(src_to_tgt_content)
        return self.bleu_align(srcfile, tgtfile, src_to_tgt_content)

    def postprocess(self, srcs, tgts, src_lang, tgt_lang):
        def output_render(lines):
            detok = lambda x: self.tokenizer.detokenize(x)
            lines = list(map(detok, lines))
            return lines

        srcs = output_render(srcs)
        tgts = output_render(tgts)

        postprocd_srcs = []
        postprocd_tgts = []

        for src, tgt in zip(srcs, tgts):
            _, src_segments = self.segmenter(src, src_lang)
            _, tgt_segments = self.segmenter(tgt, tgt_lang)
            if len(src_segments) == len(tgt_segments):
                postprocd_srcs.extend(src_segments)
                postprocd_tgts.extend(tgt_segments)
            else:
                postprocd_srcs.append(src)
                postprocd_tgts.append(tgt)

        postprocd_src = '\n'.join(postprocd_srcs)
        postprocd_tgt = '\n'.join(postprocd_tgts)
        return postprocd_src, postprocd_tgt