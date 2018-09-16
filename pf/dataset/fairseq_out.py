from .bi import ParallelDataset

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
        delegator[key](value)



class FairseqOutput(ParallelDataset):
    def __init__(self, path, src, tgt, max_length=7500000):
        self.path = path
        self.exts = (src, tgt)
        self.max_length = max_length

    def __iter__(self):
        self.fp = iter(open(self.path))
        start = 7
        for i in range(start):
            _ = next(self.fp)
        return self

    def __next__(self):
        order = ["S", "T", "H", "P"]
        predn = FairseqPrediction()
        for i, key in enumerate(order):
            line = next(self.fp).strip()
            predn.update(key, line)
        return predn

            


