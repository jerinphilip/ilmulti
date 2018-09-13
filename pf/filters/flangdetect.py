from langdetect import detect_langs
from . import Filter

class LangDetect(Filter):
    def __init__(self, lang, prob=0.98):
        self.lang = lang
        self.prob = prob
        
    def __call__(self, datum):
        best = detect_langs(datum)[0]
        if best.lang == self.lang \
                and best.prob > self.prob:
                return True
        return False

class PairDetect(Filter):
    def __init__(self, first, second, prob):
        self.ffirst = LangDetect(first, prob)
        self.fsecond = LangDetect(second, prob)

    def __call__(self, datum):
        first, second = datum
        if not self.ffirst(first): return False
        if not self.fsecond(second): return False
        return True

