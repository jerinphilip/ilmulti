import os

class ParallelWriter:
    def __init__(self, prefix, name, src, tgt, bufsize=1024*1024):
        self.bufsize = bufsize
        self.src = self.fp(prefix, name, src)
        self.tgt = self.fp(prefix, name, tgt)


    def fp(self, prefix, name, ext):
        fname = '{}.{}'.format(name, ext)
        fpath = os.path.join(prefix, fname)
        return open(fpath, 'w+', buffering=self.bufsize)

    def write(self, src, tgt):
        print(src, file=self.src)
        print(tgt, file=self.tgt)
