import sys
from ilmulti.dataset import FairseqOutput
from ilmulti.dataset import ParallelWriter
from tqdm import tqdm

path = sys.argv[1]
src = sys.argv[2]
tgt = sys.argv[3]

dataset = FairseqOutput(path, src, tgt, plb=0.4, pub=0.9, max_length=100)
total_pairs = int(62151737/2)

prefix = sys.argv[4]
writer = ParallelWriter(prefix, 'train', src, tgt)

for i, entry in tqdm(enumerate(dataset), total=total_pairs):
    src, tgt = entry
    writer.write(src, tgt)



