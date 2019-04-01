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

# Create tokenizer

tokenizer = SentencePieceTokenizer()
# exit()

# Declare datasets
mininterval = 40
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--lang', required=True, type=str)
parser.add_argument('--output', required=True, type=str)
args = parser.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)

dictionary = tokenizer.dictionary()
dictionary.save(os.path.join(args.output, "vocab.dict"))

def dfilter(sset, ext):
    ls = []
    for dataset in sset:
        # if canonicalize(ext) in dataset.exts:
        # print(dataset, canonicalize(ext) == dataset.exts[1])
        if canonicalize(ext) == dataset.exts[1]:
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

def augmented(prefix, exts):
    src, tgt = exts
    return  [
        ParallelDataset(prefix, (src, tgt)),
        ParallelDataset(prefix, (tgt, src)),
    ]

root = '/Neutron5/jerin/consolidation/parallel/mann-ki-baat/'
required = ['bn', 'hi', 'ml', 'ta', 'te', 'ur']
for lang in required:
    tag = 'man_ki_baat.en-{}'.format(lang)
    prefix = os.path.join(root, tag)
    exts = (lang, 'en'.format(lang))
    parallels = augmented(prefix, exts)
    for parallel in parallels:
        pairs.add(parallel)

dataset = TensorMultiDataset(pairs, tokenizer)
writer = ParallelWriter(args.output, 'test', 'src', 'tgt')
mapping_fname = os.path.join(args.output, "test_lang.mapping")
mapping = open(mapping_fname, 'w+')
for i in trange(len(dataset), mininterval=mininterval):
    src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
    src_lang_token, *src_tokens = src_tokens
    tgt_lang_token, *tgt_tokens = tgt_tokens
    src_tokens = [tgt_lang_token] + src_tokens
    f = lambda x:  ' '.join(x)
    source_sentence = f(src_tokens)
    target_sentence = f(tgt_tokens)
    writer.write(source_sentence, target_sentence)
    print(' '.join([str(i), src_lang_token, tgt_lang_token]), file=mapping)
