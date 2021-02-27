from ..meta import Filter
from langid.langid import LanguageIdentifier
from langid.langid import model as m

class LangMatch(Filter):
    def __init__(self, src_lang: str, tgt_lang: str, threshold=0.8):
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.identifier = LanguageIdentifier.from_modelstring(m, norm_probs=True)
        self.identifier.set_languages([src_lang, tgt_lang])
        self.threshold = threshold

    def condition(self, src_line: str, tgt_line: str) -> bool:
        def check(line, lang_expected):
            lang, prob = self.identifier.classify(line)
            src = (prob >= self.threshold)
            if not src: return False
            if lang != lang_expected: return False

        if not check(src_line, self.src_lang): return False
        if not check(tgt_line, self.tgt_lang): return False
        return True

