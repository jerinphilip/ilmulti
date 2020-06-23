
"""
This file creates models already trained and available.
"""

import os
import sys

PRETRAINED_CONFIG = {
    'mm-all': {
        'model': 'mm-all/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v0'
        'segmenter': 'simple'
    },

    'mm-all-iter1': {
        'model': 'mm-all-iter1',
        'tokenizer': 'ilmulti-v1'
        'segmenter': 'simple'
    }
}

def from_pretrained(tag, use_cuda=False):
    config = PRETRAINED_CONFIG['tag']
    from .translator import build_translator
    from ..segment import build_segmenter
    from ..sentencepiece import build_tokenizer

    translator = build_translator(config['model'])
    segmenter = build_segmenter(config['segmenter'])
    tokenizer = build_tokenizer(config['tokenizer'])
    self.engine = MTEngine(translator, segmenter, tokenizer)
    return engine


def mm_all(*args, **kwargs):
    return from_pretrained('mm-all')
