
from ilmulti.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from ilmulti.dataset import AgnosticTokenizedDataset
from ilmulti.filters import PairDetect
from ilmulti.sentencepiece import SentencePieceTokenizer
import os
from ilmulti.dataset import ParallelWriter
from ilmulti.dataset import FakeParallelDataset
from tqdm import tqdm

# Create tokenizer

tokenizer = SentencePieceTokenizer()

# Declare datasets

class Collector(set):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def add(self, pset):
        super().add(pset)
        if not pset.is_mono():
            first, second = pset.get_mono_as_parallel()
            super().add(first)
            super().add(second)

pairs = Collector()
# 1: ILCI
# C(N, 2) Pairs.

root = '/Neutron5/jerin/consolidation/parallel/ilci/'
required = ['bg', 'en', 'hi', 'ml', 'ta', 'te', 'ud']
n = len(required)
for i in range(n):
    for j in range(i+1, n):
        exts = (required[i], required[j])
        prefix = os.path.join(root, 'complete')
        parallel = ParallelDataset(prefix, exts)
        pairs.add(parallel)


# 2: OpenSubs: OPUS
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'train')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.add(parallel)

# 3: National Dataset
root = '/Neutron5/jerin/consolidation/parallel/national'
prefix = os.path.join(root, 'national')
exts = ('en', 'hi')
parallel = ParallelDataset(prefix, exts)
pairs.add(parallel)


# 4: Monolingual Available

## Malayalam 

root = '/Neutron5/jerin/malayalam-data/'
prefix = os.path.join(root, 'all')
ext = 'ml'
parallel = FakeParallelDataset(prefix, ext)
pairs.add(parallel)


multi = AgnosticTokenizedDataset(pairs, tokenizer)
# writer = ParallelWriter('dump', 'train', 'src', 'tgt')
# for src, tgt in tqdm(multi):
#     writer.write(src, tgt)



# Dev Dataset
# -----------------------------------------------------

pairs = Collector()
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'dev')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.add(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)
# writer = ParallelWriter('dump', 'dev', 'src', 'tgt')
# for src, tgt in tqdm(multi):
#     writer.write(src, tgt)

# Test Dataset
# -----------------------------------------------------

pairs = Collector()
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']

for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'test')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.add(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)
# writer = ParallelWriter('dump', 'test', 'src', 'tgt')
# for src, tgt in tqdm(multi):
#     writer.write(src, tgt)


