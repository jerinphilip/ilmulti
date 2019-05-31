import pandas as pd
import os
from collections import namedtuple

def _f(sub_path):
    root = 'consolidated'
    path = os.path.join(root, sub_path)
    return path


Corpus = namedtuple('Corpus', 'tag path lang')

def IITB_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'iitb-hi-en/parallel/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', _f(sub_path), lang)
        corpora.append(corpus)
    return corpora

IITB_train = IITB_meta('train')
IITB_dev = IITB_meta('dev')
IITB_test = IITB_meta('test')

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

WAT_train = WAT_meta('train')
WAT_dev = WAT_meta('dev')
WAT_test = WAT_meta('test')



def sanity_check(collection):
    for corpus in collection:
        print(corpus)



if __name__ == '__main__':
    def merge(*_as):
        _ase = []
        for a in _as:
            _ase.extend(a)
        return _ase

    _all = merge(
        WAT_train,
        WAT_dev,
        WAT_test,
        IITB_train,
        IITB_dev,
        IITB_test,
    )

    sanity_check(_all)

