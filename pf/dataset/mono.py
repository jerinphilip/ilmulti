import os
import warnings
from pf.utils import language_token

class MonolingualDataset:
    def __init__(self, path, lang):
        self.path = path
        self.lang = lang

    def __repr__(self):
        return '{path}.{lang}'.format(path=self.path, lang=self.lang)

    def unique_id(self):
        return self.__repr__()

    def lang_token(self):
        return language_token(self.lang)

    def __iter__(self):
        self.fp = open(self.path)
        self.iter = iter(self.fp)
        return self

    def __next__(self):
        contents = next(self.iter).strip()
        if not contents:
            warnings.warn("Empty line detected")
        return contents



