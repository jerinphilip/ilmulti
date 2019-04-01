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
mininterval = 100
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--lang', required=True, type=str)
parser.add_argument('--output', required=True, type=str)
args = parser.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)

dictionary = tokenizer.dictionary()
dictionary.save(os.path.join(args.output, "vocab.dict"))

# def dfilter(sset, ext):
#     ls = []
#     for dataset in sset:
#         # if canonicalize(ext) in dataset.exts:
#         # print(dataset, canonicalize(ext) == dataset.exts[1])
#         if canonicalize(ext) == dataset.exts[1]:
#             ls.append(dataset)
#     return set(ls)
# 
# 
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
# 
# root = '/Neutron5/jerin/consolidation/parallel/ilci/'
# required = ['bg', 'en', 'hi', 'ml', 'ta', 'te', 'ud']
# n = len(required)
# for i in range(n):
#     for j in range(i+1, n):
#         exts = (required[i], required[j])
#         prefix = os.path.join(root, 'complete')
#         parallels = augmented(prefix, exts)
#         for parallel in parallels:
#             pairs.add(parallel)
# 
# 
# # 2: OpenSubs: OPUS
# root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
# langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
# for lang in langs:
#     _dir = 'multiway-{}-en'.format(lang)
#     prefix = os.path.join(root, _dir, 'train')
#     exts = ('en', lang)
#     parallels = augmented(prefix, exts)
#     for parallel in parallels:
#         pairs.add(parallel)
# 
# # 3: National Dataset
# root = '/Neutron5/jerin/consolidation/parallel/national'
# prefix = os.path.join(root, 'national')
# exts = ('en', 'hi')
# # parallel = ParallelDataset(prefix, exts)
# parallels = augmented(prefix, exts)
# for parallel in parallels:
#     pairs.add(parallel)


# 4: Monolingual Available
## Malayalam 
# root = '/Neutron5/jerin/malayalam-data/'
# prefix = os.path.join(root, 'all')
# ext = 'ml'
# parallel = FakeParallelDataset(prefix, ext)
# pairs.add(parallel)

# # 5: IIT-Bombay
# root = '/Neutron5/jerin/consolidation/parallel/f-iitb/f-iitb'
# _dir = ''.format(lang)
# prefix = os.path.join(root, 'train')
# exts = ('en', 'hi')
# parallels = augmented(prefix, exts)
# # parallel = ParallelDataset(prefix, exts)
# for parallel in parallels:
#     pairs.add(parallel)

# print("Filtering!")
# pairs = dfilter(pairs, args.lang)
# for pair in pairs:
#     print(pair)
# dataset = TensorMultiDataset(pairs, tokenizer)
# writer = ParallelWriter(args.output, 'train', 'src', 'tgt')
# for i in trange(len(dataset)):
#     src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
# 
#     src_lang_token, *src_tokens = src_tokens
#     tgt_lang_token, *tgt_tokens = tgt_tokens
#     src_tokens = [tgt_lang_token] + src_tokens
# 
#     f = lambda x:  ' '.join(x)
#     source_sentence = f(src_tokens)
#     target_sentence = f(tgt_tokens)
#     writer.write(source_sentence, target_sentence)

# Dev Dataset
# -----------------------------------------------------
# 
# pairs = Collector()
# root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
# langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
# for lang in langs:
#     _dir = 'multiway-{}-en'.format(lang)
#     prefix = os.path.join(root, _dir, 'dev')
#     exts = ('en', lang)
#     parallels = augmented(prefix, exts)
#     # parallel = ParallelDataset(prefix, exts)
#     for parallel in parallels:
#         pairs.add(parallel)
# 
# root = '/Neutron5/jerin/consolidation/parallel/f-iitb/f-iitb'
# _dir = ''.format(lang)
# prefix = os.path.join(root, 'dev')
# exts = ('en', 'hi')
# parallels = augmented(prefix, exts)
# # parallel = ParallelDataset(prefix, exts)
# for parallel in parallels:
#     pairs.add(parallel)
# # 
# # # multi = AgnosticTokenizedDataset(pairs, tokenizer)
# pairs = dfilter(pairs, args.lang)
# dataset = TensorMultiDataset(pairs, tokenizer)
# writer = ParallelWriter(args.output, 'dev', 'src', 'tgt')
# for i in trange(len(dataset), mininterval=mininterval):
#     src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
# 
#     src_lang_token, *src_tokens = src_tokens
#     tgt_lang_token, *tgt_tokens = tgt_tokens
#     src_tokens = [tgt_lang_token] + src_tokens
# 
#     f = lambda x:  ' '.join(x)
#     source_sentence = f(src_tokens)
#     target_sentence = f(tgt_tokens)
#     writer.write(source_sentence, target_sentence)

# Test Dataset
# -----------------------------------------------------

# pairs = Collector()
# root = '/Neutron5/jerin/consolidation/parallel/wat-2018-multi'
# langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']
# 
# for lang in langs:
#     _dir = 'multiway-{}-en'.format(lang)
#     prefix = os.path.join(root, _dir, 'test')
#     exts = ('en', lang)
#     parallels = augmented(prefix, exts)
#     # parallel = ParallelDataset(prefix, exts)
#     for parallel in parallels:
#         pairs.add(parallel)

pairs = Collector()
root = '/Neutron5/jerin/consolidation/parallel/wat-normalized'
langs = ['bn', 'hi', 'ta', 'te', 'ml', 'ur']

for lang in langs:
    _dir = '{}-en'.format(lang)
    prefix = os.path.join(root, _dir, 'test')
    exts = ('en', lang)
    parallels = augmented(prefix, exts)
    # parallel = ParallelDataset(prefix, exts)
    for parallel in parallels:
        pairs.add(parallel)

# root = '/Neutron5/jerin/consolidation/parallel/f-iitb/f-iitb'
# # _dir = ''.format(lang)
# prefix = os.path.join(root, 'test')
# exts = ('en', 'hi')
# parallels = augmented(prefix, exts)
# # parallel = ParallelDataset(prefix, exts)
# for parallel in parallels:
#     print(parallel)
#     pairs.add(parallel)

# pairs = dfilter(pairs, args.lang)
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
