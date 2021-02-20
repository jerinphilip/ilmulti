import os
import nltk
import warnings
from ..utils import detect_lang
from nltk.tokenize.punkt import PunktLanguageVars
from ..utils.env_utils import resolve

# @jerin: Danda and Double Danda lol.
DEVANAGIRI = '\u0964\u0965'
ARABIC_FULL_STOP = '\u06D4'

delimiters = {
    'hi': DEVANAGIRI,
    'bn': DEVANAGIRI,
    'or': DEVANAGIRI,
    'pa': DEVANAGIRI,
    'ur': ARABIC_FULL_STOP
}

def PunktDelimiter(lang):
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


class PunktSplitter:
    def __init__(self, path, lang):
        self.path = path
        self.lang = lang
        self.model = self.load_model()

    def load_model(self):
        # Critical bit: This is where the model loading happens.
        nltk_uri = 'file:{}'.format(self.path)
        model = nltk.data.load(nltk_uri)
        lang_vars = PunktDelimiter(self.lang)()
        model._lang_vars = lang_vars
        return model

    def __call__(self, content):
        return self.model.tokenize(content)


class MultiPunktSplitter:
    def __init__(self, variation='punkt/pib'):
        self._splitter = {}
        ASSETS_DIR = resolve()
        self.data_dir = os.path.join(ASSETS_DIR, variation)   
        self.langs = [
            'en', 'hi', 'bn', 'ml', 
            'ur', 'mr', 'gu', 'te',
            'ta', 'pa', 'or'
        ]

        self.default = 'en'
        self._loaded = {}

    def _lazy_load_or_default(self, lang):
        if lang not in self.langs:
            lang = self.default

        if lang not in self._loaded:
            path  = os.path.join(self.data_dir, '{}.pickle'.format(lang))
            self._loaded[lang] = PunktSplitter(path , lang)

        return self._loaded[lang]

    def __call__(self, content, lang=None):
        _, _lang= detect_lang(content)[0]
        if lang is None:
            lang = _lang

        elif _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")

        splitter = self._lazy_load_or_default(lang)
        return (_lang, splitter(content))

def inspect_tokenizer(tokenizer):
    param_keys = ['abbrev_types', 'collocations', 'sent_starters']
    for key in param_keys:
        print(key, getattr(tokenizer._params, key))
        print()
