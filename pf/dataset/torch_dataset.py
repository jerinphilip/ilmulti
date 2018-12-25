import torch
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from pf.utils import language_token
from tqdm import tqdm

id_filter = lambda *a, **kw: True

class DatasetFlyWeightFactory:
    def __init__(self):
        self._flyweights = {}

    def __getitem__(self, dataset):
        assert( isinstance(dataset, TorchTensorMonoDataset) )
        key = dataset.__repr__()
        if key not in self._flyweights:
            dataset.build()
            self._flyweights[key] = dataset

        return self._flyweights[key]

manager = DatasetFlyWeightFactory()

class TorchTensorMonoDataset(Dataset):
    def __init__(self, mono_dataset, tokenize, vocab, 
            move_eos_to_beginning=False, 
            _filter=id_filter):
        self.dataset = mono_dataset
        self.tokenize = tokenize
        self.vocab = vocab
        self.move_eos_to_beginning = move_eos_to_beginning
        self.length = 0
        self.samples = []
        self.built = False
        self.filter = _filter

    def __repr__(self):
        return self.dataset.__repr__()

    def build(self):
        self.built = True
        lines = open(self.dataset.path)

        pbar = tqdm(lines, desc=self.dataset.path)
        for line in pbar:
            contents = line.strip()
            sample = self._toTensor(contents)
            self.samples.append(sample)

    def __len__(self):
        assert ( self.built )
        return self.length

    def dummy_item(self):
        return _toTensor('')

    def _toTensor(self, contents):
        lang, tokens = self.tokenize(contents)

        idxs = []

        if self.move_eos_to_beginning:
            idxs.append(self.vocab.eos())

        # Prepend Language Token
        lang_token = language_token(lang)
        lang_idx = self.vocab.index(lang_token)
        idxs.append(lang_idx)

        for token in tokens:
            idxs.append(self.vocab.index(token))

        if not self.move_eos_to_beginning:
            idxs.append(self.vocab.eos())

        idxs = torch.LongTensor(idxs)
        return [idxs, len(idxs)]

    def __getitem__(self, idx):
        return self.samples[idx]

    @staticmethod
    def collate(lsamples):
        idxs, lengths = list(zip(*lsamples))
        idxs = torch.stack(idxs, dim=0)
        lengths = torch.LongTensor(idxs)
        return (idxs, lengths)

class TorchTensorParallelDataset(Dataset):
    def __init__(self, parallel_dataset, 
                src_vocab, src_tokenize, 
                tgt_tokenize=None, tgt_vocab=None,
                src_filter=id_filter, tgt_filter=id_filter):

        if tgt_tokenize is None: tgt_tokenize = src_tokenize
        if tgt_vocab is None: tgt_vocab = src_vocab

        self.dataset = parallel_dataset

        left = TorchTensorMonoDataset(
            self.dataset.left, src_tokenize, src_vocab
        )

        right = TorchTensorMonoDataset(
            self.dataset.right, tgt_tokenize, 
            tgt_vocab, move_eos_to_beginning=True
        )

        self.left = manager[left]
        self.right = manager[right]

    def __len__(self):
        assert ( len(self.left) == len(self.right) )
        return len(self.left)
    
    def  __getitem__(self, idx):
        def swap_lang_token(src, tgt):
            src_lang_token = src[0].clone()
            tgt_lang_token = tgt[0].clone()
            src[0] = tgt_lang_token
            tgt[0] = src_lang_token
            return src, tgt

        src, src_length = self.left[idx]
        tgt, tgt_length = self.right[idx]

        src, tgt = swap_lang_token(src, tgt)

        return (src, src_length, tgt, tgt_length)

    @staticmethod
    def collate(lsamples):
        srcs, src_lengths, tgts, tgt_lengths = list(zip(*samples))

        # assumes pad value is zero
        srcs = pad_sequence(srcs, batch_first=True)
        tgts = pad_sequence(tgts, batch_first=True)

        src_lengths = torch.LongTensor(src_lengths)
        tgt_lengths = torch.LongTensor(tgt_lengths)

        return (srcs, src_lengths, tgts, tgt_lengths)

class TorchTensorMultiDataset(Dataset):
    def __init__(self, parallel_datasets, tokenizer):
        self.parallel_datasets = parallel_datasets
        self.tokenizer = tokenizer
        self.load_datasets()

    def load_datasets(self):
        self.dataset = []
        self.lengths = []
        self.length = 0

        for dataset in self.parallel_datasets:
            tensor_dataset = TorchTensorParallelDataset(
                dataset, self.tokenizer.dictionary(), 
                self.tokenizer
            )
            self.dataset.append(tensor_dataset)
            self.lengths.append(len(tensor_dataset))
            self.length += len(tensor_dataset)

    def __len__(self):
        return self.length


    def __getitem__(self, idx):
        current = 0
        while idx >= self.lengths[current]:
            idx = idx - self.lengths[current]
            current  = current + 1
        return self.dataset[current][idx]

    @staticmethod
    def collate(samples):
        return TorchTensorParallelDataset.collate

