import os

MAX_BUF_SIZE=1024*1024

class ParallelWriter:
    def __init__(self, prefix, name, src, tgt, buf_size=MAX_BUF_SIZE):
        self.buf_size = buf_size
        self.src = self.fp(prefix, name, src)
        self.tgt = self.fp(prefix, name, tgt)


    def fp(self, prefix, name, ext):
        fname = '{}.{}'.format(name, ext)
        fpath = os.path.join(prefix, fname)
        return open(fpath, 'w+', buffering=self.buf_size)

    def write(self, src, tgt):
        print(src, file=self.src)
        print(tgt, file=self.tgt)
