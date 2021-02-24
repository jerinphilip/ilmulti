from ..meta import Filter

class LengthRatio(Filter):
    def __init__(self, tokenizer, src_lang: str, tgt_lang: str, 
            min_length: int, lower_bound: float, upper_bound: float):

        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.tokenizer = tokenizer
        self.min_length = min_length
    
    def condition(self, src_line:str, tgt_line:str):
        src_tokens = self.tokenizer(src_line, lang=self.src_lang)
        tgt_tokens = self.tokenizer(tgt_line, lang=self.tgt_lang)
        src_len, tgt_len = len(src_tokens), len(tgt_tokens)

        # Also handles the zero degeneracy
        src = (src_len >= self.min_length)
        tgt = (tgt_len >= self.min_length)

        if not (src and tgt):
            return False

        ratio = src_len/tgt_len
        return (self.lower_bound <= ratio) and (ratio <= self.upper_bound)


