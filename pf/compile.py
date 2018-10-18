
from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.dataset import AgnosticTokenizedDataset
from pf.filters import PairDetect
from pf.sentencepiece import SentencePieceTokenizer
import os
from pf.dataset import ParallelWriter
from tqdm import tqdm

# Create tokenizer

tokenizer = SentencePieceTokenizer()

# Declare datasets

class Collector(list):
    def append(self, pset):
        first, second = pset.get_mono_as_parallel()
        super().append(pset)
        super().append(first)
        super().append(second)

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
        pairs.append(parallel)


# 2: OpenSubs: OPUS
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'train')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.append(parallel)

# 3: National Dataset
root = '/Neutron5/jerin/consolidation/parallel/national'
prefix = os.path.join(root, 'national')
exts = ('en', 'hi')
parallel = ParallelDataset(prefix, exts)
pairs.append(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)
writer = ParallelWriter('dump', 'train', 'src', 'tgt')
for src, tgt in tqdm(multi):
    writer.write(src, tgt)

pairs = Collector()
writer = ParallelWriter('dump', 'dev', 'src', 'tgt')
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'dev')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.append(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)
for src, tgt in tqdm(multi):
    writer.write(src, tgt)

pairs = Collector()
writer = ParallelWriter('dump', 'test', 'src', 'tgt')
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']

for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'test')
    exts = ('en', lang)
    parallel = ParallelDataset(prefix, exts)
    pairs.append(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)
for src, tgt in tqdm(multi):
    writer.write(src, tgt)
