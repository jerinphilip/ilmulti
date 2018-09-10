import os

class Shard:
    def __init__(self, shard_path):
        self.root = shard_path
        self.files = os.listdir(self.root)
        shard_id = lambda x: int(x.split('.')[1])
        self.files = sorted(self.files, key = shard_id)
        self.current = -1

    def __iter__(self):
        self.next_file()
        return self

    def next_file(self):
        self.current  += 1
        if self.current > len(self.files): raise StopIteration
        fname = 'shard.{}'.format(self.current)
        fpath = os.path.join(self.root, fname)
        self.fp = iter(open(fpath))

    def __next__(self):
        try:
            line = next(self.fp)
            return line.strip()
        except StopIteration:
            self.next_file()

class ShardBuilder:
    def __init__(self, shard_path, shard_size):
        if not os.path.exists(shard_path):
            os.makedirs(shard_path)
        self.root = shard_path
        self._current = -1 
        self.fp = None
        self.counter = shard_size
        self.shard_size = shard_size

    def write(self, line):
        self.current().write(line)
        self.counter += 1

    def current(self):
        if self.counter < self.shard_size:
            return self.fp
        return self.next_shard()

    def next_shard(self):
        if self.fp is not None:
            self.fp.close()

        # Reset stuff 
        self.counter = 0
        self._current += 1

        fname = 'shard.{}'.format(self._current)
        shard_path = os.path.join(self.root, fname)
        self.fp = open(shard_path, 'w+')

        return self.fp
