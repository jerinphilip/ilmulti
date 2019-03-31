import torch
from tqdm import tqdm
import bisect

class MGANAdapter:
    def __init__(self, truncate, dataset):
        self.truncate = truncate
        self.dataset = dataset
        self._length = self._build_inverse_index(truncate)

    def _build_inverse_index(self, n):
        N = len(self.dataset)
        pbar = tqdm(
          range(N), total=N,
          desc='building inv-idx', leave=True
        )

        self.cumulative = [0]
        previous = 0
        for idx in pbar:
            idxs, tokens, length = self.dataset[idx]
            # tokens = self.tokenizer(sample)
            count = max(0, len(tokens) - n)
            previous = previous + count
            self.cumulative.append(previous)
        return previous

    def __len__(self):
        return self._length

    def __getitem__(self, idx):
    # Find the rightmost entry less than idx
        p_idx = bisect.bisect_right(self.cumulative, idx)
        j = idx - self.cumulative[p_idx-1]
        contents = self.dataset[p_idx-1]
        idxs, tokens, length = contents
        segment = idxs[j:j+self.truncate]
        item = deepcopy(segment)
        return item


