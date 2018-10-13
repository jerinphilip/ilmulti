
from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.dataset import AgnosticTokenizedDataset
from pf.filters import PairDetect
from pf.sentencepiece import SentencePieceTokenizer
import os

# Create tokenizer

tokenizer = SentencePieceTokenizer()

# Declare datasets

# 1: ILCI
# C(N, 2) Pairs.

root = '/Neutron5/jerin/consolidation/parallel/ilci/'
required = ['bg', 'en', 'hi', 'ml', 'ta', 'te', 'ud']
n = len(required)
pairs = []
for i in range(n):
    for j in range(i+1, n):
        exts = (required[i], required[j])
        prefix = os.path.join(root, 'complete')
        parallel = ParallelDataset(prefix, exts)
        pairs.append(parallel)

multi = AgnosticTokenizedDataset(pairs, tokenizer)

for src, tgt in multi:
    print(src, tgt)

