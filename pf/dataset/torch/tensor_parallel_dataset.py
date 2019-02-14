import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from .utils import id_filter
from .tensor_mono_dataset import TensorMonoDataset
from .flyweight import manager


class TensorParallelDataset(Dataset):
    def __init__(self, parallel_dataset, 
                src_vocab, src_tokenize, 
                tgt_tokenize=None, tgt_vocab=None,
                src_filter=id_filter, tgt_filter=id_filter):

        if tgt_tokenize is None: tgt_tokenize = src_tokenize
        if tgt_vocab is None: tgt_vocab = src_vocab
        
        self.dataset = parallel_dataset

        left = TensorMonoDataset(
            self.dataset.left, src_tokenize, src_vocab,
            move_eos_to_beginning=False
        )

        right = TensorMonoDataset(
            self.dataset.right, tgt_tokenize, 
            tgt_vocab, move_eos_to_beginning=False
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
            # tgt[1] = src_lang_token
            # tgt = torch.cat([tgt[:1], tgt[2:]])
            tgt = tgt[1:]
            return src, tgt

        src_idxs, src_tokens, src_length = self.left[idx]
        tgt_idxs, tgt_tokens, tgt_length = self.right[idx]

        src_idxs, tgt_idxs = swap_lang_token(src_idxs, tgt_idxs)

        src_tokens = self.left.vocab.string(src_idxs).split()
        tgt_tokens = self.right.vocab.string(tgt_idxs).split()

        return (src_idxs, src_tokens, src_length, 
                tgt_idxs, tgt_tokens, tgt_length)

    def __repr__(self):
        left = self.left.__repr__()
        right = self.right.__repr__()

        left = left.replace("/", "_")
        right = right.replace("/", "_")

        return '{left}-{right}.txt'.format(left=left, right=right)


    @staticmethod
    def collate(lsamples):
        srcs, src_lengths, tgts, tgt_lengths = list(zip(*samples))

        # assumes pad value is zero
        srcs = pad_sequence(srcs, batch_first=True)
        tgts = pad_sequence(tgts, batch_first=True)

        src_lengths = torch.LongTensor(src_lengths)
        tgt_lengths = torch.LongTensor(tgt_lengths)

        return (srcs, src_lengths, tgts, tgt_lengths)
