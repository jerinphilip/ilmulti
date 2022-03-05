import abc
import os

MAX_BUF_SIZE = 1024 * 1024


class IOBase(abc.ABC):
    def __init__(self, prefix, name, src, tgt):
        self.src = self.fp(prefix, name, src)
        self.tgt = self.fp(prefix, name, tgt)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.src.close()
        self.tgt.close()

    @abc.abstractmethod
    def fp(self, *args, **kwargs):
        return


class ParallelWriter(IOBase):
    def __init__(self, prefix, name, src, tgt, buf_size=MAX_BUF_SIZE):
        self.buf_size = buf_size
        super().__init__(prefix, name, src, tgt)

    def fp(self, prefix, name, ext):
        fname = "{}.{}".format(name, ext)
        fpath = os.path.join(prefix, fname)
        return open(fpath, "w+", buffering=self.buf_size)

    def write(self, src, tgt):
        print(src, file=self.src)
        print(tgt, file=self.tgt)


class ParallelReader(IOBase):
    def __init__(self, prefix, name, src, tgt):
        super().__init__(prefix, name, src, tgt)

    def __iter__(self):
        return self

    def __next__(self):
        src = next(self.src)
        tgt = next(self.tgt)
        return src, tgt

    def fp(self, prefix, name, ext):
        fname = "{}.{}".format(name, ext)
        fpath = os.path.join(prefix, fname)
        return open(fpath, "r")
