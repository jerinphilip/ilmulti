import torch
from torch.utils.data import Dataset
from ilmulti.utils import language_token, canonicalize
from .utils import id_filter
from tqdm import tqdm


class TensorMonoDataset(Dataset):
    def __init__(self, mono_dataset, tokenize, vocab, 
            move_eos_to_beginning=False, 
            _filter=id_filter):
        self.dataset = mono_dataset
        self.tokenize = tokenize
        self.vocab = vocab
        self.move_eos_to_beginning = move_eos_to_beginning
        self.length = 0
        self.sizes = []
        self.samples = []
        self.built = False
        self.filter = _filter

    def __repr__(self):
        return self.dataset.__repr__()

    def build(self):
        self.built = True
        with open(self.dataset.path) as fp:
            contents = fp.read()
            lines = contents.splitlines()
            pbar = tqdm(
                lines,
                desc="tokenize-{}".format(self.dataset.path)
            )

            lang = canonicalize(self.dataset.lang)

            for line in pbar:
                lang, tokens = self.tokenize(line, lang=lang)
                lang_token = language_token(lang)
                tokens = [lang_token] + tokens
                self.sizes.append(len(tokens))
                self.samples.append(tokens)
            self.length = len(lines)

    def __len__(self):
        assert ( self.built )
        return self.length

    def dummy_item(self):
        return _toTensor('')

    def _toTensor(self, idx):
        tokens = self.samples[idx]
        idxs = []

        if self.move_eos_to_beginning:
            idxs.append(self.vocab.eos())

        # Prepend Language Token

        for token in tokens:
            idxs.append(self.vocab.index(token))

        if not self.move_eos_to_beginning:
            idxs.append(self.vocab.eos())

        idxs = torch.LongTensor(idxs)
        tokens = self.vocab.string(idxs)
        return [idxs, tokens, len(idxs)]

    def __getitem__(self, idx):
        sample = self._toTensor(idx)
        return sample

    @staticmethod
    def collate(lsamples):
        idxs, tokens, lengths = list(zip(*lsamples))
        idxs = torch.stack(idxs, dim=0)
        lengths = torch.LongTensor(idxs)
        return (idxs, tokens, lengths)

