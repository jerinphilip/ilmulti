
class Config:
    def __init__(self, dictConfig):
        self.config = dictConfig

    @classmethod
    def fromFile(cls, fp):
        config = fp.read()
        instance = cls.fromString(config)

    @classmethod
    def fromString(cls, stringConfig):
        import json
        _dict = json.loads(stringConfig)
        return cls(dictConfig)

    def __getitem__(self, key):
        if key in self.config:
            return self.config[key]
        raise KeyError("{} not found in config".format(key))

from .translate.pretrained import PRETRAINED_CONFIG
validConfigs = set()
for key in PRETRAINED_CONFIG:
    validConfigs.add(Config(PRETRAINED_CONFIG))


class Builder:
    """
    Static methods ``tokenizer(tag)``, ``splitter(tag)``, ``translator(tag)``
    allows construction of incompatible components.  
    
    For safe usage, provide a config, which is checked for validity and then
    the respective tokenizer, splitter and translator can be construcuted
    lazily by calling the equivent member function with the same name.

    .. code-block:: python

        builder = Builder(config)
        # Compatible
        tokenizer = builder.tokenizer()
        splitter = builder.splitter()
        translator = builder.translator()

        # Does not guarantee compatibility.
        tokenizer = Builder.tokenizer(tokenizer_tag)
        splitter = builder.splitter(splitter_tag)
        translator = builder.translator(translator_tag)

    """
    def __init__(self, config):
        assert(isinstance(config, Config))
        assert(config in validConfigs)
        self.config = config

    def tokenizer(self):
        return Builder.tokenizer(config['tokenizer'])

    def splitter(self):
        return Builder.splitter(config['translator'])

    def translator(self):
        return Builder.translator(config['translator'])

    @staticmethod
    def tokenizer(tag):
        from .tokenizer import build_tokenizer
        return build_tokenizer(tag)

    @staticmethod
    def splitter(tag):
        from .sentence import build_splitter
        return build_splitter(tag)

    @staticmethod
    def translator(tag):
        from .translator import build_translator
        return build_translator(tag)



