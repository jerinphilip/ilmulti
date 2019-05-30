class Builder:
    pass

class TokenizedBuilder(Builder):
    def __init__(self, dataset, out_path):
        self.dataset = dataset
        self.out_path = outpath
        self.corpus = CachedCorpus()

