import pytest
import os
from .translate import create_parser, translate_main
from ..utils.env_utils import resolve

def test_translate_cmdline():
    for model in ['mm-all-iter1']:
        parser = create_parser()
        for lang in ['en', 'hi', 'bn', 'ml', 'ta']:
            argv = []
            argv.extend(['--tgt-lang', lang])
            argv.extend(['--model', model])
            args = parser.parse_args(argv)
            translate_main(args, "Hello World. This is a car. 9.2 miles away.")

