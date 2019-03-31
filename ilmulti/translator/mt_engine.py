import pf

class MTEngine:
    def __init__(self, translator, segmenter, tokenizer):
        self.segmenter = segmenter
        self.tokenizer = tokenizer
        self.translator = translator

    def __call__(self, source, tgt_lang, src_lang=None):
        lang, lines = self.segmenter(source)
        sources = []
        for line in lines:
            lang, tokens = self.tokenizer(line)
            src_lang = src_lang or lang
            # Unsupervised tokenization.
            tokens = [pf.utils.language_token(tgt_lang)] + tokens
            content = ' '.join(tokens)
            sources.append(content)

        return self.translator(sources)
