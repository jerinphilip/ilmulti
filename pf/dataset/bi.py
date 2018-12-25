
from .mono import MonolingualDataset


class ParallelDataset:
    def __init__(self, prefix, exts):
        self.prefix = prefix
        self.exts = exts

        src, tgt = exts
        left = '{}.{}'.format(prefix, src)
        right = '{}.{}'.format(prefix, tgt)

        self.left = MonolingualDataset(left, src)
        self.right = MonolingualDataset(right, tgt)

    def is_mono(self):
        return False

    def __eq__(self, other):
        if isinstance(other, ParallelDataset):
            if self.prefix == other.prefix:
                return self.exts == other.exts
        return False

    def __iter__(self):
        return zip(iter(self.left), iter(self.right))

    def __repr__(self):
        src, tgt = self.exts
        return ('ParallelDataset(prefix={prefix}, exts=(src, tgt))'
                .format(prefix=self.prefix, src=src, tgt=tgt))

    def __hash__(self):
        return hash(self.__repr__())

    def get_mono_as_parallel(self):
        assert (not self.is_mono())
        src, tgt = self.exts
        first = FakeParallelDataset(self.prefix, src)
        second = FakeParallelDataset(self.prefix, tgt)
        return (first, second)


class FakeParallelDataset(ParallelDataset):
    def __init__(self, prefix, ext):
        super().__init__(prefix, (ext, ext))

    def is_mono(self):
        return True


