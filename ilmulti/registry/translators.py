import os
from . import register_translator, register_e2e_translator
from ..utils.env_utils import resolve
from ..e2e import BlockingTranslator
from ..translate import FairseqTranslator
# from ..ssplit import PatternSplitter, MultiPunktSplitter


@register_translator('m2en4', FairseqTranslator)
def _config_gen_fn():
    ASSETS_DIR = resolve()
    data = os.path.join(ASSETS_DIR, 'translation', 'm2en4')
    config = {
        'path': os.path.join(data, 'checkpoint_last.pt'),
        'max_tokens': 32000,
        'task': 'translation',
        'source_lang': 'src',
        'target_lang': 'tgt',
        'data': data,
        'buffer_size': 2
    }
    return config


@register_e2e_translator('m2en4', BlockingTranslator)
def _e2e_config_gen_fn():
    return {
        'translator': 'm2en4',
        'splitter': 'punkt/pib',
        'tokenizer': 'sentencepiece/v1'
    }

