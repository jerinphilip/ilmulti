from abc import ABC, abstractmethod


class ConfigBuildable(ABC):
    @classmethod
    @abstractmethod
    def fromConfig(cls, config):
        return

    @classmethod
    def validateConfig(cls, config):
        return True

    @classmethod
    def build(cls, config):
        assert cls.validateConfig(config)
        return cls.fromConfig(config)
