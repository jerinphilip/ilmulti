from torch.utils.data import Dataset
from .tensor_parallel_dataset import TensorParallelDataset
from .flyweight import manager

# class TensorMultiDataset(Dataset):
#     def __init__(self, parallel_datasets, tokenizer):
#         self.parallel_datasets = parallel_datasets
#         self.tokenizer = tokenizer
#         self.load_datasets()

class TensorMultiDataset(Dataset):
    def __init__(self, parallel_datasets, tokenizer):
        self.parallel_datasets = parallel_datasets
        self.tokenizer = tokenizer
        self.load_datasets()

    def load_datasets(self):
        self.dataset = []
        self.lengths = []
        self.length = 0

        for dataset in self.parallel_datasets:
            tensor_dataset = TensorParallelDataset(
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
        return TensorParallelDataset.collate

    def load_datasets(self):
        self.dataset = []
        self.lengths = []
        self.length = 0

        for dataset in self.parallel_datasets:
            tensor_dataset = TensorParallelDataset(
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
        return TensorParallelDataset.collate

