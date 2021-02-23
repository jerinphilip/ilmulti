import re
import warnings
from ..utils import detect_lang
from ..utils.functional import ForwardFunctor, MultiFunctor, ConfigBuildable

class PatternSplitter(ForwardFunctor, ConfigBuildable):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    @classmethod
    def fromConfig(cls, config):
        return cls(config['pattern'])

    def _paragraph_sentence(self, paragraph):  
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

    def transform(self, paragraph):
        "returns sentences"
        paragraphs = paragraph.splitlines()
        cleaned = []
        for paragraph in paragraphs:
            _cleaned = self._paragraph_sentence(paragraph)
            cleaned.extend(_cleaned)
        return cleaned


class MultiPatternSplitter(MultiFunctor, ConfigBuildable):
    Functor = PatternSplitter

