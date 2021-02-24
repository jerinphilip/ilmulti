
from functools import partial
from collections import defaultdict
from ..meta import ConfigBuildable

REGISTRY = defaultdict(dict)

def register(tag: str, cls: ConfigBuildable, _type: str):
    """
    To be used as a decorator for a generating function, which generates configs.
    configs are dictionaries.
    """
    def populator(generatingFunction):
        REGISTRY[_type][tag] = lambda: cls.fromConfig(generatingFunction())
    return populator


register_splitter =  partial(register, _type='splitter')
"""
specialization of register to register splitters
usage

.. code-block::

  @register_splitter('punkt/pib')
  def _punkt_pib_generating_function():
     ....

"""

register_tokenizer = partial(register, _type='tokenizer')
"""
specialization of register to register tokenizers
usage

.. code-block::

  @register_tokenizer('sentencepiece/ilmulti-v1')
  def _v1config_generating_function():
     ....

"""
register_translator = partial(register, _type='translator')

def registry() -> str:
    """
    Returns a formatted view of the entries in the global REGISTRY.
    """
    from pprint import pformat
    intermediate = {}
    for cls in REGISTRY:
        intermediate[cls] = tuple(REGISTRY[cls].keys())
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

    f = REGISTRY[_type][tag]
    return f()


from .splitters import *
