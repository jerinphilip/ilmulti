from abc import ABC, abstractmethod

class ConfigBuildable(ABC):
    @classmethod
    @abstractmethod
    def fromConfig(cls, config):
        return

    def validateConfig(cls, config):
        return

    @classmethod
    def build(cls, config):
        self.validateConfig(config)
        return cls.fromConfig(config)

