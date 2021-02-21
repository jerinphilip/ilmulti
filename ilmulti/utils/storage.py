import lmdb

class LMDBStorage:
    def __init__(self, path):
        self.env = lmdb.open(path, map_size=map_size)

    def __setitem__(key, value):
        with self.env.begin(write=True) as txn:
            key = '{}'.format(key)
            key = key.encode("ascii")
            txn.put(key, value) 

    def __getitem__(self, key):
        key = key.encode("ascii")
        with self.env.begin() as txn:
            record = txn.get(key)
            return record
        return None

    def set_source(key, value):
        key = 'source-{}'.format(key)
        self.__setitem__(key, value)

    def set_target(key, value):
        key = 'target-{}'.format(key)
        self.__setitem__(key, value)

    def get_source(key):
        key = 'source-{}'.format(key)
        return self.__getitem__(key)

    def get_target(key):
        key = 'target-{}'.format(key)
        return self.__getitem__(key)
