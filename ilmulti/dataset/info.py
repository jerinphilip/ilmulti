import os
from ilmulti.datasets.torch.fairseq_lp_adapter import LPAdapter
from ilmulti.datasets import ParallelDataset
from ilmulti.sentencepiece import SentencePieceTokenizer

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


