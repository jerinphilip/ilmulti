

from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.dataset.torch_dataset import TorchTensorParallelDataset
from pf.dataset import AgnosticTokenizedDataset
from pf.filters import PairDetect
from pf.sentencepiece import SentencePieceTokenizer
import os
from pf.dataset import ParallelWriter
from pf.dataset import FakeParallelDataset
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
            pass
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

from pf.dataset.torch_dataset import TorchTensorMultiDataset

dataset = TorchTensorMultiDataset(pairs, tokenizer)
for i in range(len(dataset)):
    src, src_lengths, tgt, tgt_lengths = dataset[i]
    print(src_lengths, tgt_lengths)
exit()



# multi = AgnosticTokenizedDataset(pairs, tokenizer)
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

# multi = AgnosticTokenizedDataset(pairs, tokenizer)
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

# multi = AgnosticTokenizedDataset(pairs, tokenizer)
# writer = ParallelWriter('dump', 'test', 'src', 'tgt')
# for src, tgt in tqdm(multi):
#     writer.write(src, tgt)


