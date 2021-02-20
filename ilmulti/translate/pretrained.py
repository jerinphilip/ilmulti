
"""
This file creates models already trained and available.
"""

import os
import sys


PRETRAINED_CONFIG = {
    'mm-all': {
        'model': 'mm-all/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v0',
        'splitter': 'punkt.pib',
    },

    'mm-all-iter1': {
        'model': 'mm-all-iter1/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'splitter': 'punkt.pib',
    },

    'mm-all-iter0': {
        'model': 'mm-all-iter0/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'splitter': 'punkt.pib',
    },

    'mm-to-en-iter1': {
        'model': 'mm-to-en-iter1/checkpoint_last.pt',
        'tokenizer': 'ilmulti-v1',
        'splitter': 'punkt.pib',
    },

    'mm-to-en-iter2': {                                                 
        'model': 'mm-to-en-iter2/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'splitter': 'punkt.pib',                                         
    }, 

    'mm-to-en-iter3': {                                                 
        'model': 'mm-to-en-iter3/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'splitter': 'punkt.pib',                                         
    },
    
    'mm-all-iter3': {                                                 
        'model': 'mm-all-iter3/checkpoint_last.pt',                   
        'tokenizer': 'ilmulti-v1',                                      
        'splitter': 'punkt.pib',                                         
    }, 

}

def from_pretrained(tag, use_cuda=False):
    config = PRETRAINED_CONFIG[tag]
    from .translator import build_translator
    from ..ssplit import build_splitter
    from ..tokenize import build_tokenizer
    from ..packaged import PackagedSystem

    translator = build_translator(config['model'], use_cuda=use_cuda)
    splitter = build_splitter(config['splitter'])
    tokenizer = build_tokenizer(config['tokenizer'])
    engine = PackagedSystem(translator, splitter, tokenizer)
    return engine
