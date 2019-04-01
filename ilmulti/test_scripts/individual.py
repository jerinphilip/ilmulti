from argparse import ArgumentParser
from ilmulti.dataset import ParallelDataset
from ilmulti.sentencepiece import SentencePieceTokenizer
from ilmulti.dataset.torch import TensorMultiDataset
from ilmulti.dataset import ParallelWriter

parser = ArgumentParser()
parser.add_argument("--root", type=str, required=True)
parser.add_argument("--src", type=str, required=True)
parser.add_argument("-tgt", type=str, required=True)
for split in ['train', 'dev', 'test']:
    parser.add_argument("--{}pref".format(split), required=True, default=split)

parser.add_argument('--output', type=str, required=True)


def augmented(prefix, exts):
    src, tgt = exts
    return  [
        ParallelDataset(prefix, (src, tgt)),
        ParallelDataset(prefix, (tgt, src)),
    ]

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

def collect(args, split_pref):
    pairs = Collector()
    prefix = os.path.join(args.root, split_pref)
    parallels = augment(prefix, (args.src, args.tgt))
    for parallel in parallels:
        pairs.add(parallel)
    return pairs


def write(output_path, split, dataset):
    writer = ParallelWriter(output_path, split, 'src', 'tgt')
    for i in trange(len(dataset)):
        src, src_tokens, src_lengths, tgt, tgt_tokens, tgt_lengths = dataset[i]
        f = lambda x:  ' '.join(x)
        source_sentence = f(src_tokens)
        target_sentence = f(tgt_tokens)
        writer.write(source_sentence, target_sentence)
        writer.write(src, tgt)

args = parser.parse_args()
tokenizer = SentencePieceTokenizer()

def build_and_write(args, split):
    pairs = collect(args, split)
    dataset = TensorMultiDataset(pairs, tokenizer)
    write(args.output, split, dataset)

build_and_write(args.trainpref)
build_and_write(args.testpref)
build_and_write(args.validpref)


    





