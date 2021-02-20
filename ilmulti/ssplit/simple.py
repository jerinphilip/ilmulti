from ..utils import detect_lang
import warnings

class SimpleSplitter:
    def __init__(self):
        pass

    def __call__(self, paragraph, lang=None):
        _, _lang = detect_lang(paragraph)[0]
        if lang is None:
            lang = _lang

        elif _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")

        lines = paragraph.splitlines()
        return (lang, lines)


