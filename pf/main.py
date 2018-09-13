from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.filters import PairDetect
from tqdm import tqdm
import sys

prefix = sys.argv[1]
exts = sys.argv[2], sys.argv[3]

parallel = ParallelDataset(prefix, exts)

multi = MultilingualDataset([parallel])

f = PairDetect('en', 'de', 0.9)
for i, (src, tgt) in enumerate(tqdm(multi)):
    print(i, ">", src)
    print(i, "<", tgt)

    if i > 10:
        break



