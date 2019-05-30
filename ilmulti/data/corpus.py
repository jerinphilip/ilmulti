import os
from collections import OrderedDict

class BaseCorpus:
    pass


class Mono(BaseCorpus):
    def __init__(self, filepath, lang):
        self.filepath = filepath
        self.lang = lang
        self._sanity_check()

    def _sanity_check(self):
        if not os.path.exists(self.filepath):
            warnings.warn("File {} not  found.".format(self.filepath))

class Parallel(BaseCorpus):
    def __init__(self, _first, _second):
        first, first_lang = _first
        second, second_lang = _second
        self.first = Mono(first, first_lang)
        self.second = Mono(second, second_lang)


class MultiParallel(BaseCorpus):
    def __init__(self, _flangs):
        self.corpora = []
        for filepath, lang in _flangs:
            corpus = Mono(filepath, lang)
            self.corpora.append(corpus)



class InMemoryCorpus:
    def __init__(self, corpus):
        assert(isinstance(corpus, Mono))
        self.lines = open(corpus.filepath).read()

    def __iter__(self):
        return self.lines.__iter__()

    def __len__(self):
        return len(self.lines)
