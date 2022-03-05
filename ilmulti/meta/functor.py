from abc import ABC, abstractmethod

from .config_buildable import ConfigBuildable


class ForwardFunctor(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Initializes a model from args"""
        return

    def __call__(self, *args, **kwargs):
        return self.transform(*args, **kwargs)

    @abstractmethod
    def transform(self, datum):
        return

    def map(self, data):
        return [self.transform(datum) for datum in data]


class InvertibleFunctor(ForwardFunctor):
    @abstractmethod
    def inv(self, tx):
        return

    def inv_map(self, txs):
        return [self.inv(tx) for tx in txs]


class MultiFunctor(ConfigBuildable, ForwardFunctor):
    def __init__(self, functorDict):
        self.functorDict = functorDict

    @classmethod
    def fromConfig(cls, config):
        functorDict = {}
        for lang, fconfig in config.items():
            functorDict[lang] = cls.Functor.fromConfig(fconfig)
        return cls(functorDict)

    def transform(self, datum, lang):
        return self.functorDict[lang].transform(datum)

    def map(self, data, lang):
        return self.functorDict[lang].map(data)


class PseudoMultiFunctor(MultiFunctor):
    def __init__(self):
        self.functor = self.__class__.Functor()

    @classmethod
    def fromConfig(cls, config):
        return cls()

    def transform(self, datum, lang):
        return self.functor.transform(datum)

    def map(self, data, lang):
        return self.functor.map(data)
