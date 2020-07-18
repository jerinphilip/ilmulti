
"""
This file creates models already trained and available.
"""

import os
import sys


PRETRAINED_CONFIG = {
    'mm-all': {
        'model': 'mm-all/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v0',
        'segmenter': 'pattern',
    },

    'mm-all-iter1': {
        'model': 'mm-all-iter1/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'segmenter': 'pattern',
    },

    'mm-all-iter0': {
        'model': 'mm-all-iter0/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'segmenter': 'pattern',
    },

    'mm-to-en-iter1': {
        'model': 'mm-to-en-iter1/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'segmenter': 'pattern',
    },

    'mm-to-en-iter2': {                                                 
        'model': 'mm-to-en-iter2/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'segmenter': 'pattern',                                         
    }, 

    'mm-to-en-iter3': {                                                 
        'model': 'mm-to-en-iter3/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'segmenter': 'pattern',                                         
    },
    
    'mm-all-iter3': {                                                 
        'model': 'mm-all-iter3/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'segmenter': 'pattern',                                         
    }, 

}

def from_pretrained(tag, use_cuda=False):
    config = PRETRAINED_CONFIG[tag]
    from .translator import build_translator
    from ..segment import build_segmenter
    from ..sentencepiece import build_tokenizer
    from .mt_engine import MTEngine

    translator = build_translator(config['model'], use_cuda=use_cuda)
    segmenter = build_segmenter(config['segmenter'])
    tokenizer = build_tokenizer(config['tokenizer'])
    engine = MTEngine(translator, segmenter, tokenizer)
    return engine


def mm_all(*args, **kwargs):
    return from_pretrained('mm-all')
