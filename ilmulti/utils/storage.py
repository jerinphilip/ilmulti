import lmdb

MAP_SIZE = 1024 * 1024


class LMDBStorage:
    def __init__(self, path, map_size=MAP_SIZE):
        self.env = lmdb.open(path, map_size=map_size)

    def __setitem__(self, key, value):
        with self.env.begin(write=True) as txn:
            key = "{}".format(key)
            key = key.encode("ascii")
            txn.put(key, value.encode())

    def __getitem__(self, key):
        key = key.encode("ascii")
        with self.env.begin() as txn:
            record = txn.get(key)
            return record.decode("utf-8")
        return None

    def set_source(self, key, value):
        key = "source-{}".format(key)
        self.__setitem__(key, value)

    def set_target(self, key, value):
        key = "target-{}".format(key)
        self.__setitem__(key, value)

    def get_source(self, key):
        key = "source-{}".format(key)
        return self.__getitem__(key)

    def get_target(self, key):
        key = "target-{}".format(key)
        return self.__getitem__(key)
