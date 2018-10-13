from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
import os
import sentencepiece as spm
from warnings import warn


class SentencePieceTokenizer:
    def __init__(self, model_path=None, units=4000):

        if model_path is None:
            cdir = os.path.abspath(os.path.dirname(__file__))
            model_path = os.path.join(cdir, 'models')

        self.model_path = model_path

        self.tokenizer = {}
        self.units = units

    def __call__(self, text, lang=None):
        if lang is None:
            best = detect_langs(text)[0]
            lang = best.lang

        tokenizer = self.get_tokenizer(lang)
        text = ' '.join(tokenizer.EncodeAsPieces(text))
        return (lang, text)

    def get_tokenizer(self, lang):
        def get_model(lang):
            fname = '{lang}.{units}.model'.format(lang=lang, units=self.units)
            model_fpath = os.path.join(self.model_path, fname)
            return model_fpath

        if lang not in self.tokenizer:
            sp = spm.SentencePieceProcessor() 
            try:
                sp.Load(get_model(lang))
                self.tokenizer[lang] = sp
            except OSError:
                warn("[SPM] {} not found, defaulting to en".format(lang))
                lang = 'en'

        return self.tokenizer[lang]


if __name__ == '__main__':
    sp = SentencePieceTokenizer()
    s = sp("Hello World")
    print(s)
