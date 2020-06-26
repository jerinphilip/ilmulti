
from .core import SentencePieceTokenizer

def build_tokenizer(string):
    if string == 'ilmulti-v0':
        langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn']
        config = {lang: 4000 for lang in langs}
        return SentencePieceTokenizer(config=config)

    if string == 'ilmulti-v1':
        langs = ['en', 'hi', 'ml', 'ta', 'te', 'ur', 'bn', 'gu', 'pa', 'or', 'mr']
        config = {lang: 4000 for lang in langs}
        return SentencePieceTokenizer(config=config)

    if string == 'wmt-de-en':
        langs = ['en', 'de']
        config = {lang: 32000 for lang in langs}
        return SentencePieceTokenizer(config=config)

    raise ValueError("Unknown tag")
