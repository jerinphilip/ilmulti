import re
import warnings
from ..utils import detect_lang
from .base_segmenter import BaseSegmenter

class PatternSegmenter(BaseSegmenter):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def paragraph_segment(self, paragraph):  
        paragraph = re.sub(r'[.]+', '.', paragraph)
        segments = self.pattern.split(paragraph)
        cleaned = []
        n = len(segments)
        for i in range(0, n, 2):
            first = segments[i]
            second = segments[i+1] if i+1 < n else ''
            _cleaned = '{}{}'.format(first, second)
            _cleaned = _cleaned.lstrip().rstrip()
            cleaned.append(_cleaned)
        return cleaned

    def __call__(self, paragraph):
        "returns segments"
        paragraphs = paragraph.splitlines()
        cleaned = []
        for paragraph in paragraphs:
            _cleaned = self.paragraph_segment(paragraph)
            cleaned.extend(_cleaned)
        return cleaned


class Segmenter(BaseSegmenter):
    def __init__(self):
        self._segmenter = {}
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
            self._segmenter[lang] = PatternSegmenter(pattern)

    def __call__(self, paragraph, lang=None):
        _, _lang= detect_lang(paragraph)[0]
        if lang is None:
            lang = _lang

        if _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")
            # warnings.warn(paragraph)

        default = self._segmenter["default"]
        segmenter = self._segmenter.get(lang, default)
        return (_lang, segmenter(paragraph))
