import os
import sentencepiece as spm
from warnings import warn
from ilmulti.utils import language_token, detect_lang
from collections import Counter

class LazySPM:
    def __init__(self, path, lang, units):
        self.path = path
        self.lang = lang
        self.units = units
        self.build_vocabulary()
        self.load_model()

    def load_model(self):
        model_file = '{lang}.{units}.model'.format(lang=self.lang, units=self.units)
        model_path = os.path.join(self.path, model_file)
        self.model = spm.SentencePieceProcessor()
        self.model.load(model_path)

    def build_vocabulary(self):
        vocab_file = '{}.{}.vocab'.format(self.lang, self.units)
        vocab_path = os.path.join(self.path, vocab_file)
        self.vocab = set()
        with open(vocab_path) as fp:
            for line in fp:
                word, _ = line.strip().split()
                self.vocab.add(word)

    def __call__(self, text):
        tokens = self.model.EncodeAsPieces(text)
        clean = lambda x: x in self.vocab
        tokens = list(filter(clean, tokens))
        return tokens


class SentencePieceTokenizer:
    def __init__(self, config):
        self.tokenizer = {}

        cdir = os.path.abspath(os.path.dirname(__file__))   
        self.model_path = os.path.join(cdir, 'models')   

        for lang, units in config.items():
            self.tokenizer[lang] = LazySPM(self.model_path, lang, units)

    def __call__(self, text, lang=None):
        if lang is None:
            export = detect_lang(text, 'segmented')
            tokens, langs = [], []
            for segment, lang in export:
                tokenizer = self.get_tokenizer(lang)
                segment_tokens = tokenizer(segment)
                tokens.extend(segment_tokens)
                langs.append(lang)

            lang, *_ = Counter(langs).most_common(1)
            return (lang, tokens)

        tokenizer = self.get_tokenizer(lang)
        tokens = tokenizer(text)
        return (lang, tokens)

    def single_dictionary(self, src_lang, tgt_lang):
        from fairseq.data.dictionary import Dictionary
        dictionary = Dictionary()
        vocab = set()

        # Control tokens
        tgt_lang_token = language_token(tgt_lang)
        vocab.add(tgt_lang_token)

        tokenizer_vocab = self.tokenizer[src_lang].vocab
        vocab = vocab.union(tokenizer_vocab)
        vocab = sorted(list(vocab))

        for word in vocab:
            dictionary.add_symbol(word)

        return dictionary


    def dictionary(self):
        from fairseq.data.dictionary import Dictionary
        dictionary = Dictionary()

        vocab = set()

        # Add language_tokens
        langs, _ = list(zip(*self.tokenizer.keys()))
        langs = list(map(language_token, langs))
        vocab = vocab.union(set(langs))

        for key in self.tokenizer:
            tokenizer_vocab = self.tokenizer[key].vocab
            vocab = vocab.union(tokenizer_vocab)

        vocab = sorted(list(vocab))
        for word in vocab:
            dictionary.add_symbol(word)


        return dictionary

    def get_tokenizer(self, lang):
        if lang not in self.tokenizer:
            raise KeyError("{} not enabled with a tokenizer of unit - {}".format(lang, self.units))
        return self.tokenizer.get(lang)

    def detokenize(self, value):
        SPM_SYMBOL = '▁'
        value = value.replace(' ', '')
        value = value.replace(SPM_SYMBOL, ' ')
        if not value:
            return ''
        if value[0] == ' ':
            value = value[1:]
        return value
