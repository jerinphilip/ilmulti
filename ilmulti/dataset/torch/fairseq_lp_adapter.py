from fairseq.data.language_pair_dataset import LanguagePairDataset, collate
from fairseq import utils
from .tensor_parallel_dataset import TensorParallelDataset

class LPAdapter(LanguagePairDataset):
    def __init__(
            self, pf_parallel, duplex=True,
            left_pad_source=True, left_pad_target=False,
            max_source_positions=1024, max_target_positions=1024,
            shuffle=True, input_feeding=True, remove_eos_from_source=False,
            append_eos_to_target=False,
    ):
        assert(isinstance(pf_parallel, TensorParallelDataset))

        self.duplex = duplex
        self.dataset = pf_parallel
        self.left_pad_source = left_pad_source
        self.left_pad_target = left_pad_target
        self.max_source_positions = max_source_positions
        self.max_target_positions = max_target_positions
        self.shuffle = shuffle
        self.input_feeding = input_feeding
        self.remove_eos_from_source = remove_eos_from_source
        self.append_eos_to_target = append_eos_to_target
        self.src_dict = self.dataset.left.vocab
        self.tgt_dict = self.dataset.right.vocab
        self.src_sizes = self.dataset.left.sizes + self.dataset.right.sizes
        self.tgt_sizes = self.dataset.right.sizes + self.dataset.left.sizes
        assert(self.src_dict == self.tgt_dict)

    def __len__(self):
        multiplier = 2 if self.duplex else 1
        return multiplier*len(self.dataset)

    def __getitem__(self, idx):
        _qidx, _ridx = idx//len(self.dataset), idx%len(self.dataset)
        items = self.dataset[_qidx]
        src, tgt = items[:3], items[3:]
        if _qidx:
            src, tgt = tgt, src
        
        src_idxs, src_tokens, src_lengths = src
        tgt_idxs, tgt_tokens, tgt_lengths = tgt

        def swap_lang_token(src, tgt):
            src_lang_token = src[0].clone()
            tgt_lang_token = tgt[0].clone()
            src[0] = tgt_lang_token
            tgt = tgt[1:]
            return src, tgt

        src_idxs, tgt_idxs = swap_lang_token(src_idxs, tgt_idxs)

        if self.append_eos_to_target:
            eos = self.tgt_dict.eos() if self.tgt_dict else self.src_dict.eos()
            if tgt_idxs and tgt_idxs[-1] != eos:
                tgt_idxs = torch.cat([tgt_idxs, torch.LongTensor([eos])])
        if self.remove_eos_from_source:
            eos = self.src_dict.eos()
            if src_idxs[-1] == eos:
                src_idxs = src_idxs[:-1]

        return {
            'id': idx,
            'source': src_idxs,
            'target': tgt_idxs,
        }

    def collater(self, samples):
        return collate(
            samples, pad_idx=self.src_dict.pad(), eos_idx=self.src_dict.eos(),
            left_pad_source=self.left_pad_source, left_pad_target=self.left_pad_target,
            input_feeding=self.input_feeding,
        )

    def get_dummy_batch(self, num_tokens, max_positions, src_len=128, tgt_len=128):
        """Return a dummy batch with a given number of tokens."""
        src_len, tgt_len = utils.resolve_max_positions(
            (src_len, tgt_len),
            max_positions,
            (self.max_source_positions, self.max_target_positions),
        )
        bsz = max(num_tokens // max(src_len, tgt_len), 1)
        return self.collater([
            {
                'id': i,
                'source': self.src_dict.dummy_sentence(src_len),
                'target': self.tgt_dict.dummy_sentence(tgt_len) if self.tgt_dict is not None else None,
            }
            for i in range(bsz)
        ])

    def num_tokens(self, index):
        """Return the number of tokens in a sample. This value is used to
        enforce ``--max-tokens`` during batching."""
        return max(self.src_sizes[index], self.tgt_sizes[index] if self.tgt_sizes is not None else 0)

    def size(self, index):
        """Return an example's size as a float or tuple. This value is used when
        filtering a dataset with ``--max-positions``."""
        return (self.src_sizes[index], self.tgt_sizes[index] if self.tgt_sizes is not None else 0)

    def ordered_indices(self):
        """Return an ordered list of indices. Batches will be constructed based
        on this order."""
        if self.shuffle:
            indices = np.random.permutation(len(self))
        else:
            indices = np.arange(len(self))
        if self.tgt_sizes is not None:
            indices = indices[np.argsort(self.tgt_sizes[indices], kind='mergesort')]
        return indices[np.argsort(self.src_sizes[indices], kind='mergesort')]

    @property
    def supports_prefetch(self):
        return (
            getattr(self.src, 'supports_prefetch', False)
            and getattr(self.tgt, 'supports_prefetch', False)
        )

    def prefetch(self, indices):
        self.src.prefetch(indices)
        self.tgt.prefetch(indices)

