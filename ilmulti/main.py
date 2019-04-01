from ilmulti.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from ilmulti.filters import PairDetect
from tqdm import tqdm
import sys
import yaml
import os
from ilmulti.dataset import ParallelWriter


config_path = sys.argv[1]
with open(config_path) as fp:
    config = yaml.load(fp)
    task = config['task']
    kw = task['kwargs']
    exts = kw['exts']
    for split in kw['splits']:
        prefix = os.path.join(kw['prefix'], split)
        parallel = ParallelDataset(prefix, exts)

        writer = ParallelWriter(kw['out'], split, 'src', 'tgt')
        multi = MultilingualDataset([parallel])
        for i, (src, tgt) in tqdm(enumerate(multi)):
            writer.write(src, tgt)
