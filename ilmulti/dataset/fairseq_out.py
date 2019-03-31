from .bi import ParallelDataset
from pf.filters import PairDetect

class FairseqPrediction:
    def __init__(self, src=None, tgt=None, ppl=None):
        self.src = src
        self.tgt = tgt
        self.ppl = ppl

    def complete(self):
        bsrc = self.src is not None
        btgt = self.tgt is not None
        bppl = self.ppl is not None
        return bsrc and btgt and bpplt

    @staticmethod
    def decode(pieces):
        return ''.join(pieces).replace("▁", " ")

    def hypothesis(self, line):
        _id, ppl, *pieces = line.split()
        nppl = float(ppl)
        _, iid = _id.split('-')

        # Update
        self.ppl = nppl
        self.tgt = FairseqPrediction.decode(pieces)

    def source(self, line):
        _id, *pieces = line.split()
        _, iid = _id.split('-')

        # Update
        self.src = FairseqPrediction.decode(pieces)

    def update(self, key, value):
        delegator = {
            "S": lambda value: self.source(value),
            "H": lambda value: self.hypothesis(value)
        }
        noop = lambda value: None
        delegator.get(key, noop)(value)



class FairseqOutput(ParallelDataset):
    def __init__(self, path, src, tgt, 
            max_count=7500000, 
            min_length=8, max_length=30, 
            plb=0.1, pub=0.4):
        self.path = path
        self.exts = (src, tgt)
        self.max_count = max_count

        self.min_length = min_length
        self.max_length = max_length

        self.plb = 0.1
        self.pub = 0.4

        self.langdetect = PairDetect(src, tgt, 0.99)

    def __iter__(self):
        self.counter = 0
        self.fp = iter(open(self.path))
        return self

    def __next__(self):
        return self._next()
    

    def _next(self):
        if self.counter > self.max_count:
            raise StopIteration
        order = ["S", "H"]
        predn = None
        while not self.check(predn):
            predn = FairseqPrediction()
            for i, key in enumerate(order):
                line = next(self.fp).strip()
                predn.update(key, line)

        self.counter = self.counter + 1
        return (predn.src, predn.tgt)

    def check(self, predn):
        if predn is None: return False

        def within(x, y):
            def __inner(z):
                return x <= z and z <= y
            return __inner

        _lwithin = lambda s: within(self.min_length, self.max_length)(len(s.split()))
        lwithin = _lwithin(predn.src) and _lwithin(predn.tgt)
        pwithin = within(self.plb, self.pub)(-1*predn.ppl)
        if lwithin and pwithin:
            lang_ok = self.langdetect((predn.src, predn.tgt))
            return lang_ok

