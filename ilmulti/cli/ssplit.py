#!/bin/bash

import sys
from argparse import ArgumentParser


def create_parser():
    from ..registry import REGISTRY

    parser = ArgumentParser(description="Extract sentences from a blob of text")
    parser.add_argument(
        "--type",
        choices=list(REGISTRY["splitter"].keys()),
        help="Type of splitter to use",
        required=True,
    )
    parser.add_argument(
        "--lang", required=True, help="Language of the input-blob of text if known"
    )
    parser.add_argument("--input", default=None, help="Path to input file")
    parser.add_argument("--output", default=None, help="Path to output file")
    return parser


def ssplit_main(args, blob):
    from ..registry import build

    splitter = build("splitter", args.type)
    sentences = splitter(blob, lang=args.lang)
    if args.output is None:
        output_file = sys.stdout
    else:
        output_file = open(args.output, "w")
    for line in sentences:
        print(line, file=output_file)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    ssplit_main(args, blob)
