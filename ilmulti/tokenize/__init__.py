
import os
from ..utils.env_utils import resolve
from .sentencepiece import SentencePieceTokenizer, MultiSentencePieceTokenizer

def build_tokenizer(string):
    if string == 'ilmulti-v0':
        langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn']
        config = {lang: 4000 for lang in langs}
        return MultiSentencePieceTokenizer(config=config)

    if string == 'ilmulti-v1':
        langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn', 'gu', 'pa', 'or', 'mr']
        uconfig = {lang: 4000 for lang in langs}
        ASSETS_DIR = resolve()
        model_path = os.path.join(ASSETS_DIR, 'sentencepiece/ilmulti-v1')   
        config = {}
        for lang, units in uconfig.items():
            config[lang] = { 'lang': lang, 'units': units, 'path' : model_path }

        return MultiSentencePieceTokenizer.fromConfig(config)

    if string == 'wmt-de-en':
        langs = ['en', 'de']
        config = {lang: 32000 for lang in langs}
        return MultiSentencePieceTokenizer(config=config)

    raise ValueError("Unknown tag")
