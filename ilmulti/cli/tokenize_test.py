import pytest
import os
from .tokenize import create_parser, tokenize_main
from ..utils.env_utils import resolve

def test_tokenize_cmdline():
    for tokenizer_type in ['ilmulti-v1']:
        parser = create_parser()
        for lang in ['en', 'hi']:
            argv = []
            argv.extend(['--lang', lang])
            argv.extend(['--type', tokenizer_type])
            args = parser.parse_args(argv)
            tokenize_main(args, "Hello World.\nThis is a car.\n9.2 miles away.")

