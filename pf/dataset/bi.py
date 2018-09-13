
from .mono import MonolingualDataset

class ParallelDataset:
    def __init__(self, prefix, exts):
        self.prefix = prefix
        self.exts = exts

        src, tgt = exts
        left = '{}.{}'.format(prefix, src)
        right = '{}.{}'.format(prefix, tgt)

        self.left = MonolingualDataset(left)
        self.right = MonolingualDataset(right)

    def __iter__(self):
        return zip(iter(self.left), iter(self.right))


