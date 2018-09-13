
class Filter:
    pass

class ComposeFilter:
    def __init__(self, *fs):
        self.fs = fs

    def __call__(self, datum):
        for f in self.fs:
            if not self.f:
                return False
        return True

from .flangdetect import LangDetect, PairDetect
