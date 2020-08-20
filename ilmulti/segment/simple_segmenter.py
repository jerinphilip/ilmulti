from .base_segmenter import BaseSegmenter
from ..utils import detect_lang

class SimpleSegmenter(BaseSegmenter):
    def __init__(self):
        pass

    def __call__(self, paragraph, **unused):
        _, lang = detect_lang(paragraph)[0]
        lines = paragraph.splitlines()
        return (lang, lines)


