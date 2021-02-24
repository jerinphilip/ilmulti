import os
import nltk
from typing import Sequence, List
from nltk.tokenize.punkt import PunktLanguageVars

from ..utils.env_utils import resolve
from ..meta import ForwardFunctor, MultiFunctor, ConfigBuildable


def PunktDelimiter(lang: str):
    DEVANAGIRI = '\u0964\u0965'
    ARABIC_FULL_STOP = '\u06D4'

    delimiters = {
        'hi': DEVANAGIRI,
        'bn': DEVANAGIRI,
        'or': DEVANAGIRI,
        'pa': DEVANAGIRI,
        'ur': ARABIC_FULL_STOP
    }

    # The symbols are obtainable here.
    # https://apps.timwhitlock.info/unicode/inspect?

    lang_delimiters = delimiters.get(lang, '')
    lang_vars_class_name = 'PunktLanguageVars_{}'.format(lang)

    base_end_chars = PunktLanguageVars.sent_end_chars
    sent_end_chars = tuple(list(base_end_chars) + list(lang_delimiters))

    overrides = {
        'sent_end_chars': sent_end_chars
    }

    cls = type(lang_vars_class_name, (PunktLanguageVars,), overrides)
    return cls


class PunktSplitter(ForwardFunctor, ConfigBuildable):
    def __init__(self, path: str, lang: str):
        self.path = path
        self.lang = lang

        # Critical bit: This is where the model loading happens.
        nltk_uri = 'file:{}'.format(self.path)
        self.model = nltk.data.load(nltk_uri)
        lang_vars = PunktDelimiter(self.lang)()
        self.model._lang_vars = lang_vars

    def transform(self, content: str) -> List[str]:
        return self.model.tokenize(content)

    @classmethod
    def fromConfig(cls, config):
        return cls(config['path'], config['lang'])


class MultiPunktSplitter(MultiFunctor):
    Functor = PunktSplitter

def inspect_tokenizer(tokenizer):
    param_keys = ['abbrev_types', 'collocations', 'sent_starters']
    for key in param_keys:
        print(key, getattr(tokenizer._params, key))
        print()
