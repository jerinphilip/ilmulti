import sys
from pf.dataset import FairseqOutput
from pf.dataset import ParallelWriter

path = sys.argv[1]
src = sys.argv[2]
tgt = sys.argv[3]

dataset = FairseqOutput(path, src, tgt)
for i, entry in enumerate(dataset):
    src, tgt = entry
    print(i, '>', src)
    print(i, '<', tgt)



