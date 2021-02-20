import pytest
import os
from .ssplit import create_parser, ssplit_main
from ..utils.env_utils import resolve

def test_ssplit_cmdline():
    for splitter_type in ['simple', 'pattern', 'punkt.pib']:
        parser = create_parser()
        for lang in [None, 'en', 'hi']:
            argv = []
            if lang is not None:
                argv.extend(['--lang', lang])
            argv.extend(['--type', splitter_type])
            args = parser.parse_args(argv)
            if lang is 'hi':
                with pytest.warns(UserWarning):
                    ssplit_main(args, "Hello World. This is a car. 9.2 miles away.")
            else:
                ssplit_main(args, "Hello World. This is a car. 9.2 miles away.")

