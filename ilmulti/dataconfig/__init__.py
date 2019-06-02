import os
from collections import namedtuple

DATASET_REGISTRY = {}
def dataset_register(tag, splits):
    def __inner(f):
        DATASET_REGISTRY[tag] = (splits, f)
        return f
    return __inner

DATA_ROOT = 'ilmt-data/consolidated'
def data_abspath(sub_path):
    path = os.path.join(DATA_ROOT, sub_path)
    return path

Corpus = namedtuple('Corpus', 'tag path lang')
def sanity_check(collection):
    for corpus in collection:
        print(corpus)

from . import corpora

