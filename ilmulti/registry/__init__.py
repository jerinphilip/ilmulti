from functools import partial
from collections import defaultdict
from ..meta import ConfigBuildable

REGISTRY = defaultdict(dict)

def register(tag: str, cls: ConfigBuildable, _type: str):
    def populator(generatingFunction):
        REGISTRY[_type][tag] = lambda: cls.fromConfig(generatingFunction())
    return populator

register_splitter =  partial(register, _type='splitter')
register_tokenizer = partial(register, _type='tokenizer')
register_translator = partial(register, _type='translator')

def registry():
    from pprint import pformat
    intermediate = {}
    for cls in REGISTRY:
        intermediate[cls] = tuple(REGISTRY[cls].keys())
    return pformat(intermediate, indent=2)

def build(_type, tag):
    f = REGISTRY[_type][tag]
    return f()


from .splitters import *
