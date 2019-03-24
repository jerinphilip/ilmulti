
class PatternSegmenter:
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def __call__(self, paragraph):
        "returns segments"
        paragraph = re.sub(r'[.]+', '.', paragraph)
        segments = self.pattern.split(text)
        return segments

class Segmenter:
    def __init__(self):
        self._segmenter = {}
        patterns = {
            "en": "([.;!?…])",
            "ur": "([.;!?…])",
            "hi": "([_;!?_|I])",
            "default": "([.;!?…])"

        }
        for pattern in patterns:
            self._segmenter[pattern] = PatternSegmenter(pattern)

    def __call__(self, paragraph, lang=None):
        _lang, prob = langid.classify(paragraph)
        if lang is None:
            lang = _lang

        if _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")
            # warnings.warn(paragraph)
        
        default = self._segmenter["default"]
        segmenter = self._segmenter.get(lang, default)
