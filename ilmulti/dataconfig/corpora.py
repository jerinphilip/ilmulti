from . import DATASET_REGISTRY
from . import dataset_register, data_abspath
from . import Corpus, sanity_check

@dataset_register('iitb-hi-en', ['train', 'dev', 'test'])
def IITB_meta(split):
    corpora = []
    for lang in ['en', 'hi']:
        sub_path = 'iitb-hi-en/parallel/{}.{}'.format(split, lang)
        corpus = Corpus('iitb-hi-en', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora


@dataset_register('wat-ilmpc', ['train', 'dev', 'test'])
def WAT_meta(split):
    corpora = []
    langs = ['bn', 'hi', 'ml', 'si', 'ta', 'te', 'ur']
    for lang in langs:
        for src in [lang, 'en']:
            sub_path = 'wat-ilmpc/parallel/{}-en/{}.{}'.format(
                    lang, split, src
            )
            corpus_name = 'wat-ilmpc-{}-{}'.format(lang, 'en')
            corpus = Corpus(corpus_name, data_abspath(sub_path), src)
            corpora.append(corpus)
    return corpora

@dataset_register('ufal-en-tam', ['train', 'dev', 'test'])
def UFALEnTam_meta(split):
    corpora = []
    for lang in ['en', 'ta']:
        sub_path = 'ufal-en-tam/{}.{}'.format(split, lang)
        corpus = Corpus('ufal-en-tam', data_abspath(sub_path), lang)
        corpora.append(corpus)
    return corpora



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

