from pf.dataset import MonolingualDataset, ParallelDataset
from pf.filters import PairDetect
from tqdm import tqdm
import sys

prefix = sys.argv[1]
exts = sys.argv[2], sys.argv[3]

parallel = ParallelDataset(prefix, exts)

f = PairDetect('en', 'de', 0.9)
for i, (src, tgt) in enumerate(tqdm(parallel)):
    pair = (src, tgt)
    if not f(pair):
        print(i, ">", src)
        print(i, "<", tgt)



