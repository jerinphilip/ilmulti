import os
from .shard import ShardBuilder, Shard

class MonolingualDataset:
    def __init__(self, path):
        self.path = path
        self.asserts()

    def asserts(self):
        """ Checks if required files are present """
        required = [
            "shards"
        ]

        for fname in required:
            fpath = os.path.join(self.path, fname)
            assert os.path.exists(fpath)

    def __iter__(self):
        shard_path = os.path.join(self.path, 'shards')
        return Shard(shard_path).__iter__()



    @staticmethod
    def build(text_path, save_path, shard_size):
        builder = MonolingualBuilder(text_path, save_path, shard_size)
        return MonolingualDataset(save_path)


class MonolingualBuilder:
    def __init__(self, text_path, save_path, shard_size):
        self.save_path = save_path
        self.text_path = text_path
        self.shard_size = shard_size
        self.build_shards()

    def build_shards(self):
        with open(self.text_path) as fp:
            shard_path = os.path.join(self.save_path, 'shards')
            builder = ShardBuilder(shard_path, self.shard_size)
            for line in fp:
                builder.write(line)
