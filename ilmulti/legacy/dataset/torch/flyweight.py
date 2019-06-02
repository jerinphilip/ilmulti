from .tensor_mono_dataset import TensorMonoDataset

class DatasetFlyWeightFactory:
    def __init__(self):
        self._flyweights = {}

    def __getitem__(self, dataset):
        assert( isinstance(dataset, TensorMonoDataset) )
        key = dataset.__repr__()
        if key not in self._flyweights:
            dataset.build()
            self._flyweights[key] = dataset

        return self._flyweights[key]

manager = DatasetFlyWeightFactory()
