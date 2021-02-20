import re
import warnings
from ..utils import detect_lang

class PatternSplitter:
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def paragraph_sentence(self, paragraph):  
        paragraph = re.sub(r'[.]+', '.', paragraph)
        sentences = self.pattern.split(paragraph)
        cleaned = []
        n = len(sentences)
        for i in range(0, n, 2):
            first = sentences[i]
            second = sentences[i+1] if i+1 < n else ''
            _cleaned = '{}{}'.format(first, second)
            _cleaned = _cleaned.lstrip().rstrip()
            cleaned.append(_cleaned)
        return cleaned

    def __call__(self, paragraph):
        "returns sentences"
        paragraphs = paragraph.splitlines()
        cleaned = []
        for paragraph in paragraphs:
            _cleaned = self.paragraph_sentence(paragraph)
            cleaned.extend(_cleaned)
        return cleaned


class MultiPatternSplitter:
    def __init__(self):
        self._splitter = {}
        patterns = {
            "en": "([.;!?…])",
            "ur": "([.;!?…])",
            "hi": "([।;!?…|I])",
            "bn": "([।.;!?…|I])",
            "or": "([।.;!?…|I])",
            "default": "([.;!?…])"

        }
        for lang in patterns:
            pattern = patterns[lang]
            self._splitter[lang] = PatternSplitter(pattern)

    def __call__(self, paragraph, lang=None):
        _, _lang= detect_lang(paragraph)[0]
        if lang is None:
            lang = _lang

        if _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")
            # warnings.warn(paragraph)

        default = self._splitter["default"]
        splitter = self._splitter.get(lang, default)
        return (_lang, splitter(paragraph))
