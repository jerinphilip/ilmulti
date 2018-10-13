from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
import os
import sentencepiece as spm

class SentencePieceTokenizer:
    def __init__(self, model_path=None, units=4000):

        if model_path is None:
            cdir = os.path.abspath(os.path.dirname(__file__))
            model_path = os.path.join(cdir, 'models')

        self.model_path = model_path

        self.tokenizer = {}
        self.units = units

    def __call__(self, text):
        best = detect_langs(text)[0]
        tokenizer = self.get_tokenizer(best.lang)
        text = tokenizer.EncodeAsPieces(text)
        return (best.lang, text)

    def get_tokenizer(self, lang):
        def get_model(lang):
            fname = '{lang}.{units}.model'.format(lang=lang, units=self.units)
            model_fpath = os.path.join(self.model_path, fname)
            print(model_fpath)
            return model_fpath

        if lang not in self.tokenizer:
            sp = spm.SentencePieceProcessor() 
            sp.Load(get_model(lang))
            self.tokenizer[lang] = sp

        return self.tokenizer[lang]


if __name__ == '__main__':
    sp = SentencePieceTokenizer()
    s = sp("Hello World")
    print(s)
