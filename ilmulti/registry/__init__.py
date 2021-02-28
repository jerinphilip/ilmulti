
from functools import partial, wraps
from collections import defaultdict
from ..meta import ConfigBuildable

REGISTRY = defaultdict(dict)

def register(tag: str, cls: ConfigBuildable, _type: str):
    def populator(generatingFunction):
        if tag in REGISTRY[_type]:
            raise ValueError("tag {} already exists for Type {}".format(tag, _type))

        REGISTRY[_type][tag] = (cls, generatingFunction())
    return populator


register_splitter =  partial(register, _type='splitter')
register_tokenizer = partial(register, _type='tokenizer')
register_translator = partial(register, _type='translator')
register_e2e_translator = partial(register, _type='e2e_translator')

def registry(debug=False) -> str:
    """
    Returns a formatted view of the entries in the global REGISTRY.
    """
    from pprint import pformat
    intermediate = {}
    if not debug:
        for cls in REGISTRY:
            intermediate[cls] = tuple(REGISTRY[cls].keys())
    else:
        for cls in REGISTRY:
            intermediate[cls] = dict([(tag, REGISTRY[cls][tag]) for tag in REGISTRY[cls]])
    return pformat(intermediate, indent=2)

def build(_type: str, tag: str):
    """
    Once the registry is populated by decorators, this function can be used to
    build a particular instance.

.. code-block::

    tokenizer = build('tokenizer', 'sentencepiece/ilmulti-v1')
    splitter = build('splitter', 'punkt/pib')
    translator = build('translator', 'm2m4')

    """

    cls, config = REGISTRY[_type][tag]
    return cls.fromConfig(config)


from .splitters import *
from .tokenizers import *
from .translators import *

