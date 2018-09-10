
from .mono import MonolingualDataset

class BilingualDataset:
    def __init__(self, left, right):
        self.left = MonolingualDataset(left)
        self.right = MonolingualDataset(right)

    @staticmethod
    def build(self, left_path, right_path, save_path):
        return 



