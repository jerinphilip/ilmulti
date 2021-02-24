import os
from warnings import warn
from sentencepiece import SentencePieceProcessor
from collections import Counter

from ..utils.language_utils import language_token, detect_lang
from ..meta import InvertibleFunctor, MultiFunctor, ConfigBuildable

def _detokenize(tokenized_text):
    SPM_SYMBOL = '▁'
    tokenized_text = tokenized_text.replace(' ', '')
    tokenized_text = tokenized_text.replace(SPM_SYMBOL, ' ')
    if not tokenized_text:
        return ''
    if tokenized_text[0] == ' ':
        tokenized_text = tokenized_text[1:]
    return tokenized_text


class SentencePieceTokenizer(InvertibleFunctor, ConfigBuildable):
    def __init__(self, path, lang, units):
        self.path = path
        self.lang = lang
        self.units = units
        self.load_vocabulary()
        self.load_model()

    @classmethod
    def fromConfig(cls, config):
        return cls(config['path'], config['lang'], config['units'])

    def load_model(self):
        model_file = '{lang}.{units}.model'.format(lang=self.lang, units=self.units)
        model_path = os.path.join(self.path, model_file)
        self.model = SentencePieceProcessor()
        self.model.load(model_path)

    def load_vocabulary(self):
        vocab_file = '{}.{}.vocab'.format(self.lang, self.units)
        vocab_path = os.path.join(self.path, vocab_file)
        self.vocab = set()
        with open(vocab_path) as fp:
            for line in fp:
                word, _ = line.strip().split()
                self.vocab.add(word)

    def transform(self, text: str):
        tokens = self.model.EncodeAsPieces(text)
        clean = lambda x: x in self.vocab 
        tokens = list(filter(clean, tokens))
        return ' '.join(tokens)

    def inv(self, tokenized_text: str):
        return _detokenize(tokenized_text)


    def dictionary_fairseq(self):
        return fairseq_dictionary_from_vocab(self.vocab)


class MultiSentencePieceTokenizer(MultiFunctor, InvertibleFunctor):
    Functor = SentencePieceTokenizer

    @property
    def vocab(self):
        vocab_ = set()
        # Add language_tokens
        langs, _ = list(zip(*self.functorDict.keys()))
        langs = list(map(language_token, langs))
        vocab_ = vocab_.union(set(langs))

        for key in self.tokenizer:
            tokenizer_vocab_ = self.functorDict[key].vocab
            vocab_ = vocab_.union(tokenizer_vocab_)

        # Sorting is critical; 
        vocab_ = sorted(list(vocab_))
        return vocab_

    def dictionary_fairseq(self):
        return fairseq_dictionary_from_vocab(vocab)

    def inv(self, datum):
        return _detokenize(datum)


def fairseq_dictionary_from_vocab(vocab):
        from fairseq.data.dictionary import Dictionary
        dictionary = Dictionary()
        for word in self.vocab:
            dictionary.add_symbol(word)
        return dictionary
