from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence


class TorchMonoDataset(Dataset):
    def __init__(self, pf_dataset):
        self.dataset = dataset
        self._preload()

    def _preload(self):
        self.samples = []
        for sample in self.dataset:
            self.samples.append(sample)

        self.length = len(self.samples)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.samples[idx]

class TorchTensorMonoDataset(Dataset):
    def __init__(self, torch_dataset, tokenize, vocab):
        self.dataset = torch_dataset
        self.tokenize = tokenize
        self.vocab = vocab

    @classmethod
    def build(cls, 

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        contents = self.dataset[idx]
        tokens = self.tokenize(contents)
        idxs = []
        for token in tokens:
            idxs.append(vocab.index(token))

        idxs.append(vocab.eos())
        idxs = torch.LongTensor(idxs)
        return [idxs, len(idxs)]

    @staticmethod
    def collate(lsamples):
        idxs, lengths = list(zip(*lsamples))
        idxs = torch.stack(idxs, dim=0)
        lengths = torch.LongTensor(idxs)
        return (idxs, lengths)

class TorchTensorParallelDataset(Dataset):
    def __init__(self, parallel_dataset, 
                src_vocab, src_tokenize, 
                tgt_tokenize=None, tgt_vocab=None):

        if tgt_tokenize is None: tgt_tokenize = src_tokenize
        if tgt_vocab is None: tgt_vocab = src_vocab

        self.dataset = parallel_dataset
        self.left = TorchMonoDataset(self.dataset.left, src_tokenize, src_vocab)
        self.right = TorchMonoDataset(self.dataset.right, tgt_tokenize, tgt_vocab)

    
    def  __getitem__(self, idx):
        src, src_length = self.left[idx]
        tgt, tgt_length = self.right[idx]
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

