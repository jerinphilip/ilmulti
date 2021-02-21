#!/bin/bash

from argparse import ArgumentParser
import sys

def create_parser():
    parser = ArgumentParser(description='Tokenize a sequence of sentences')
    parser.add_argument('--type', choices=['ilmulti-v1'], help='Type of tokenizer to use', required=True)
    parser.add_argument('--lang', default=None, help='Language of the input-blob of text if known')
    parser.add_argument('--input', default=None, help='Path to input file')
    parser.add_argument('--output', default=None, help='Path to output file')
    return parser

def tokenize_main(args, lines):
    from ..tokenize import build_tokenizer
    tokenizer = build_tokenizer(args.type)
    if args.output is None:
        output_file = sys.stdout
    else:
        output_file = open(args.output, 'w')
    for line in lines:
        lang, tokenized = tokenizer(line, lang=args.lang)
        print(tokenized, file=output_file)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    tokenize_main(args, blob.splitlines())
