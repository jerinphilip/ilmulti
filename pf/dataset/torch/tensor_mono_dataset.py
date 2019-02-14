import torch
from torch.utils.data import Dataset
from pf.utils import language_token
from .utils import id_filter


class TensorMonoDataset(Dataset):
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
        with open(self.dataset.path) as fp:
            contents = fp.read()
            self.lines = contents.splitlines()
            self.length = len(self.lines)
            # pbar = tqdm(lines, desc=self.dataset.path)
            # for line in pbar:
            #     cleaned = line.strip()
            #     sample = self._toTensor(cleaned)
            #     self.samples.append(sample)

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
        tokens = self.vocab.string(idxs)
        return [idxs, tokens, len(idxs)]

    def __getitem__(self, idx):
        line = self.lines[idx].strip()
        sample = self._toTensor(line)
        return sample

    @staticmethod
    def collate(lsamples):
        idxs, lengths = list(zip(*lsamples))
        idxs = torch.stack(idxs, dim=0)
        lengths = torch.LongTensor(idxs)
        return (idxs, lengths)

