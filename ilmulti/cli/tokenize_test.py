import pytest
import os
from .tokenize import create_parser, tokenize_main
from ..utils.env_utils import resolve

def test_ssplit_cmdline():
    for tokenizer_type in ['ilmulti-v1']:
        parser = create_parser()
        for lang in [None, 'en', 'hi']:
            argv = []
            if lang is not None:
                argv.extend(['--lang', lang])
            argv.extend(['--type', tokenizer_type])
            args = parser.parse_args(argv)
            tokenize_main(args, ["Hello World.", "This is a car.", "9.2 miles away."])

