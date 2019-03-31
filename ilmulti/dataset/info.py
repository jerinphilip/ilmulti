import os
from pf.datasets.torch.fairseq_lp_adapter import LPAdapter
from pf.datasets import ParallelDataset
from pf.sentencepiece import SentencePieceTokenizer

def build(root, split, src, tgt):
    tokenizer = SentencePieceTokenizer()
    prefix = os.path.join(root, split)
    pf_dataset = ParallelDataset(prefix, (src, tgt))
    dataset = LPAdapter(pf_dataset, tokenizer.dictionary(), tokenizer)
    return dataset
    

def load_datasets(fs):
    datasets = []
    for root, split, src, tgt in fs:
        dataset = build(root, split, src, tgt)
        datasets.append(dataset)


