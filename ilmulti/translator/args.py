
from collections import namedtuple

class Args:
    """
    Adapter to sub in for the namespace so the SequenceGenerator can be
    created from fairseq.
    """
    def __init__(self, **kwargs):
        self.custom_set = set()
        self.enhance(**kwargs)

    def __getattr__(self, key):
        return self.__dict__.get(key, None)

    def enhance(self, **kwargs):
        for key, val in kwargs.items():
            if key not in self.__dict__:
                self.custom_set.add(key)
                self.__dict__[key] = val

    def __str__(self):
        lines = []
        for key in sorted(list(self.custom_set)):
            line = '{key} : {val}'.format(key=key, val=self.__dict__[key])
            lines.append(line)
        return '\n'.join(lines)
