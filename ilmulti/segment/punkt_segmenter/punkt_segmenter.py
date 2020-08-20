import os
import nltk
import warnings
from ...utils import detect_lang
from ..base_segmenter import BaseSegmenter
from .utils import PunktDelimiter

class PunktSegmenterLang:
    def __init__(self, model_dir, domain, lang):
        self.model_dir = model_dir
        self.domain = domain
        self.lang = lang
        self.model = self.load_model()

    def load_model(self):
        # Critical bit: This is where the model loading happens.
        model_fname = '{}.{}'.format(self.lang, self.domain)
        model_path = os.path.join(self.model_dir, model_fname)
        nltk_uri = 'file:{}'.format(model_path)
        model = nltk.data.load(nltk_uri)
        lang_vars = PunktDelimiter(self.lang)()
        model._lang_vars = lang_vars
        return model

    def __call__(self, content):
        return self.model.tokenize(content)


class PunktSegmenter(BaseSegmenter):
    def __init__(self):
        self._segmenter = {}
        cdir = os.path.abspath(os.path.dirname(__file__))   
        self.model_dir = os.path.join(cdir, 'models')   
        self.domain = 'pib.news.pickle'
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
            self._loaded[lang] = PunktSegmenterLang(
                self.model_dir, self.domain, lang
            )

        return self._loaded[lang]

    def __call__(self, content, lang=None):
        _, _lang= detect_lang(content)[0]
        if lang is None:
            lang = _lang

        if _lang != lang:
            warnings.warn("Language mismatch on text, please sanitize.")
            warnings.warn("Ignore if you know what you're doing")

        segmenter = self._lazy_load_or_default(lang)
        return (_lang, segmenter(content))
