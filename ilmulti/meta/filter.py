from abc import ABC, abstractmethod

class Filter(ABC):
    def __call__(self, data):
        return self.filter(data)

    @abstractmethod
    def condition(self, datum):
        return

    def filter(self, data):
        return [datum for datum in data if self.condition(datum)]

