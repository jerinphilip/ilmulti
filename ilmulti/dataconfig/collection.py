import pandas as pd
import os
from collections import namedtuple

def _f(sub_path):
    root = 'consolidated'
    path = os.path.join(root, sub_path)
    return path


DATASET_REGISTRY = {}
def dataset_register(tag, splits):
    def __inner(f):
        DATASET_REGISTRY[tag] = (splits, f)
        return f
    return __inner


Corpus = namedtuple('Corpus', 'tag path lang')

@dataset_register('iitb-hi-en', ['train', 'dev', 'test'])
def IITB_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'iitb-hi-en/parallel/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', _f(sub_path), lang)
        corpora.append(corpus)
    return corpora


@dataset_register('wat-ilmpc', ['train', 'dev', 'split'])
def WAT_meta(split):
    corpora = []
    langs = ['bn', 'hi', 'ml', 'si', 'ta', 'te', 'ur']
    for lang in langs:
        for src in [lang, 'en']:
            sub_path = 'wat-ilmpc/parallel/{}-en/{}.{}'.format(
                    lang, split, src
            )
            corpus_name = 'wat-ilmpc-{}-{}'.format(lang, 'en')
            corpus = Corpus(corpus_name, _f(sub_path), src)
            corpora.append(corpus)
    return corpora

@dataset_register('ufal-en-tam', ['train', 'dev', 'split'])
def UFALEnTam_meta(split):
    corpora = []
    for lang in ['en', 'ta']:
        sub_path = 'ufal-en-tam/{}.{}'.format(split, lang)
        corpus = Corpus('ufal-en-tam', _f(sub_path), lang)
        corpora.append(corpus)
    return corpora


def sanity_check(collection):
    for corpus in collection:
        print(corpus)

if __name__ == '__main__':
    def merge(*_as):
        _ase = []
        for a in _as:
            _ase.extend(a)
        return _ase

    ls = []
    for key in DATASET_REGISTRY:
        splits, f = DATASET_REGISTRY[key]
        for split in splits:
            ls.append(f(split))

    _all = merge(*ls)
    sanity_check(_all)

