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
