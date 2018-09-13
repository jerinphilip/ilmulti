import os
import warnings

class MonolingualDataset:
    def __init__(self, path):
        self.path = path

    def __iter__(self):
        self.fp = open(self.path)
        self.iter = iter(self.fp)
        return self

    def __next__(self):
        contents = next(self.iter).strip()
        if not contents:
            warnings.warn("Empty line detected")
        return contents



