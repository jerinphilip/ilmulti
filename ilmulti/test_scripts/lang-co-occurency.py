from ilmulti.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from ilmulti.dataset.torch import TensorParallelDataset
from ilmulti.dataset import AgnosticTokenizedDataset
from ilmulti.filters import PairDetect
from ilmulti.sentencepiece import SentencePieceTokenizer
from ilmulti.dataset.torch import TensorMultiDataset
import os
from ilmulti.dataset import ParallelWriter
from ilmulti.dataset import FakeParallelDataset
from ilmulti.utils import canonicalize
from tqdm import tqdm, trange
from argparse import ArgumentParser

def augmented(prefix, exts):
    src, tgt = exts
    return  [
        ParallelDataset(prefix, (src, tgt)),
        ParallelDataset(prefix, (tgt, src)),
    ]
parser = ArgumentParser()
parser.add_argument('--src_lang', type=str, required=True)
parser.add_argument('--tgt_lang', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--threshold', type=int, required=True)
args = parser.parse_args()

tokenizer = SentencePieceTokenizer()
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
root = '/Neutron5/jerin/consolidation/parallel/ilci/'
exts = (args.src_lang, args.tgt_lang)
prefix = os.path.join(root, 'complete')
parallels = augmented(prefix, exts)
pairs.add(parallels[0])
# for parallel in parallels:


from itertools import product
from collections import defaultdict

cooc = defaultdict(int)

dataset = TensorMultiDataset(pairs, tokenizer)
for i in trange(len(dataset)):
    src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
    src_lang_token, *src_tokens = src_tokens
    tgt_lang_token, *tgt_tokens = tgt_tokens
    for x, y in product(src_tokens, tgt_tokens):
        cooc[(x, y)] += 1

output = open(args.output, 'w+')

for key in cooc:
    x, y, = key
    if cooc[key] > args.threshold:
        print(x, y, cooc[key], file=output)
    



