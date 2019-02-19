from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.dataset.torch import TensorParallelDataset
from pf.dataset import AgnosticTokenizedDataset
from pf.filters import PairDetect
from pf.sentencepiece import SentencePieceTokenizer
from pf.dataset.torch import TensorMultiDataset
import os
from pf.dataset import ParallelWriter
from pf.dataset import FakeParallelDataset
from tqdm import tqdm, trange

# Create tokenizer

tokenizer = SentencePieceTokenizer()
from argparse import ArgumentParser
dictionary = tokenizer.dictionary()
dictionary.save("mm-raw/vocab.dict")
# exit()

# Declare datasets

def dfilter(sset, ext):
    return sset
    ls = []
    for dataset in sset:
        if ext in dataset.exts:
            ls.append(dataset)
    return set(ls)


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

def augmented(prefix, exts):
    src, tgt = exts
    return  [
        ParallelDataset(prefix, (src, tgt)),
        ParallelDataset(prefix, (tgt, src)),
        FakeParallelDataset(prefix, src),
        FakeParallelDataset(prefix, tgt)
    ]

def augmented(prefix, exts):
    src, tgt = exts
    return  [
        ParallelDataset(prefix, (src, tgt)),
        ParallelDataset(prefix, (tgt, src)),
    ]

root = '/Neutron5/jerin/consolidation/parallel/ilci/'
required = ['bg', 'en', 'hi', 'ml', 'ta', 'te', 'ud']
n = len(required)
for i in range(n):
    for j in range(i+1, n):
        exts = (required[i], required[j])
        prefix = os.path.join(root, 'complete')
        parallels = augmented(prefix, exts)
        for parallel in parallels:
            pairs.add(parallel)


# 2: OpenSubs: OPUS
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'train')
    exts = ('en', lang)
    parallels = augmented(prefix, exts)
    for parallel in parallels:
        pairs.add(parallel)

# 3: National Dataset
root = '/Neutron5/jerin/consolidation/parallel/national'
prefix = os.path.join(root, 'national')
exts = ('en', 'hi')
# parallel = ParallelDataset(prefix, exts)
parallels = augmented(prefix, exts)
for parallel in parallels:
    pairs.add(parallel)


# 4: Monolingual Available
## Malayalam 
root = '/Neutron5/jerin/malayalam-data/'
prefix = os.path.join(root, 'all')
ext = 'ml'
parallel = FakeParallelDataset(prefix, ext)
pairs.add(parallel)

# 5: IIT-Bombay
pairs = dfilter(pairs, 'ml')

dataset = TensorMultiDataset(pairs, tokenizer)
writer = ParallelWriter('mm-raw', 'train', 'src', 'tgt')
for i in trange(len(dataset)):
    src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
    f = lambda x:  ' '.join(x)
    source_sentence = f(src_tokens)
    target_sentence = f(tgt_tokens)
    writer.write(source_sentence, target_sentence)

# Dev Dataset
# -----------------------------------------------------

pairs = Collector()
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'dev')
    exts = ('en', lang)
    parallels = augmented(prefix, exts)
    # parallel = ParallelDataset(prefix, exts)
    for parallel in parallels:
        pairs.add(parallel)

root = '/Neutron5/jerin/consolidation/parallel/f-iitb/f-iitb'
_dir = ''.format(lang)
prefix = os.path.join(root, 'dev')
exts = ('en', 'hi')
parallels = augmented(prefix, exts)
# parallel = ParallelDataset(prefix, exts)
for parallel in parallels:
    pairs.add(parallel)

# multi = AgnosticTokenizedDataset(pairs, tokenizer)
pairs = dfilter(pairs, 'ml')
dataset = TensorMultiDataset(pairs, tokenizer)
writer = ParallelWriter('mm-raw', 'dev', 'src', 'tgt')
for i in trange(len(dataset)):
    src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
    f = lambda x:  ' '.join(x)
    source_sentence = f(src_tokens)
    target_sentence = f(tgt_tokens)
    writer.write(source_sentence, target_sentence)

# Test Dataset
# -----------------------------------------------------

pairs = Collector()
root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']

for lang in langs:
    _dir = 'multiway-{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'test')
    exts = ('en', lang)
    parallels = augmented(prefix, exts)
    # parallel = ParallelDataset(prefix, exts)
    for parallel in parallels:
        pairs.add(parallel)

root = '/Neutron5/jerin/consolidation/parallel/f-iitb/f-iitb'
_dir = ''.format(lang)
prefix = os.path.join(root, 'test')
exts = ('en', 'hi')
parallels = augmented(prefix, exts)
# parallel = ParallelDataset(prefix, exts)
for parallel in parallels:
    pairs.add(parallel)

pairs = dfilter(pairs, 'ml')
dataset = TensorMultiDataset(pairs, tokenizer)
writer = ParallelWriter('mm-raw', 'test', 'src', 'tgt')
for i in trange(len(dataset)):
    src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
    f = lambda x:  ' '.join(x)
    source_sentence = f(src_tokens)
    target_sentence = f(tgt_tokens)
    writer.write(source_sentence, target_sentence)
    writer.write(src, tgt)


