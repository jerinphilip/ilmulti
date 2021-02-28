import os
from . import register_translator, register_e2e_translator
from ..utils.env_utils import resolve
from ..e2e import BlockingTranslator
from ..translate import FairseqTranslator
from functools import partial
from typing import Literal
from copy import deepcopy
# from ..ssplit import PatternSplitter, MultiPunktSplitter


def cods_comad_config(_type: Literal['m2m', 'm2en'], _iter: int) -> dict:
    name = '{_type}{_iter}'.format(_type=_type, _iter=_iter)
    ASSETS_DIR = resolve()
    data = os.path.join(ASSETS_DIR, 'translation', name)
    config = {
        'path': os.path.join(data, 'checkpoint_last.pt'),
        'max_tokens': 32000,
        'task': 'translation',
        'source_lang': 'src',
        'target_lang': 'tgt',
        'data': data,
        'buffer_size': 2
    }
    return (name, config)


cods_comad_config_d = {}
for _type in ['m2m', 'm2en']:
    for _iter in range(4):
        name, config = cods_comad_config(_type, _iter)
        print(name, config)
        cods_comad_config_d[name] = deepcopy(config)
        generating_fn = lambda : cods_comad_config_d[name]
        f = register_translator(name, FairseqTranslator)(generating_fn)


available_e2e = [
    ('m2en4', 'sentencepiece/v1', 'punkt/pib'),
    ('m2en3', 'sentencepiece/v1', 'punkt/pib'),
    ('m2m1',  'sentencepiece/v1', 'punkt/pib'),
]


e2e_config = {}
for tx, tokenizer, splitter in available_e2e:
    e2e_config[tx] = {'translator': tx, 'splitter': splitter, 'tokenizer': tokenizer}
    config = deepcopy(e2e_config[tx])
    f = register_e2e_translator(tx, BlockingTranslator)( lambda: config)

