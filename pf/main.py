from pf.dataset import MonolingualDataset, ParallelDataset, MultilingualDataset
from pf.filters import PairDetect
from tqdm import tqdm
import sys
import yaml
import os


class ParallelWriter:
    def __init__(self, prefix, name, src, tgt):
        self.src = self.fp(prefix, name, src)
        self.tgt = self.fp(prefix, name, tgt)


    def fp(self, prefix, name, ext):
        fname = '{}.{}'.format(name, ext)
        fpath = os.path.join(prefix, fname)
        return open(fpath, 'w+')

    def write(self, src, tgt):
        print(src, file=self.src)
        print(tgt, file=self.tgt)


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



