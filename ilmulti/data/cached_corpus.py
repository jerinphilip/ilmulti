from .corpus import Mono, InMemoryCorpus
from collections import OrderedDict

class CachedCorpus:
    def __init__(self):
        self._flyweights = OrderedDict()

    def __getitem__(self, corpus):
        key = corpus.filepath
        if key not in self._flyweights:
            in_memory_corpus = InMemoryCorpus(corpus)
            self._flyweights[key] = in_memory_corpus
        return self._flyweights[key]


