import os

import pytest

from ..utils.env_utils import resolve
from .ssplit import create_parser, ssplit_main


def test_ssplit_cmdline():
    for splitter_type in ["simple", "pattern", "punkt/pib"]:
        parser = create_parser()
        for lang in ["en", "hi"]:
            argv = []
            argv.extend(["--lang", lang])
            argv.extend(["--type", splitter_type])
            args = parser.parse_args(argv)
            ssplit_main(args, "Hello World. This is a car. 9.2 miles away.")
