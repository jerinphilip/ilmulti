import os
from . import register_tokenizer
from ..utils.env_utils import resolve
from ..tokenize import SentencePieceTokenizer, MultiSentencePieceTokenizer

@register_tokenizer('sentencepiece/v0', MultiSentencePieceTokenizer)
def _v0_generating_function():
    langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn']
    config = {lang: 4000 for lang in langs}
    return config

@register_tokenizer('sentencepiece/v1', MultiSentencePieceTokenizer)
def _v1_generating_function():
    langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn', 'gu', 'pa', 'or', 'mr']
    uconfig = {lang: 4000 for lang in langs}
    ASSETS_DIR = resolve()
    model_path = os.path.join(ASSETS_DIR, 'sentencepiece/v1')   
    config = {}
    for lang, units in uconfig.items():
        config[lang] = { 'lang': lang, 'units': units, 'path' : model_path }
    return config


