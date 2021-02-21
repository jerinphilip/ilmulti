from argparse import ArgumentParser
import sys

def create_parser():
    parser = ArgumentParser(description='Extract sentences from a blob of text')
    parser.add_argument('--model', choices=['mm-all-iter1', 'mm-all-iter2', 'mm-all-iter3'], help='Type of splitter to use', required=True)
    parser.add_argument('--tgt-lang', required=True, help='Language of the input-blob of text if known')
    parser.add_argument('--input', default=None, help='Path to input file, default is stdin')
    parser.add_argument('--output', default=None, help='Path to output file, default is stdout')
    parser.add_argument('--debug', action='store_true', help='Print debug statements')
    return parser

def translate_main(args, text):
    from ..translate import from_pretrained, PRETRAINED_CONFIG
    model = from_pretrained(args.model)
    translation = model(text, tgt_lang=args.tgt_lang)
    if args.output is None:
        output_file = sys.stdout
    else:
        output_file = open(args.output, 'w')
        
    for entry in translation:
        vals = [entry['src'], entry['tgt']]
        print('\t'.join(vals), file=output_file)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    translate_main(args, blob)


