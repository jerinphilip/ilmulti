from argparse import ArgumentParser
import sys

def create_parser():
    from ..translate.pretrained import PRETRAINED_CONFIG
    parser = ArgumentParser(description='Translates a blob of text')
    parser.add_argument('--model', choices=list(PRETRAINED_CONFIG.keys()), help='Model to use in translation', required=True)
    parser.add_argument('--src-lang', required=False, help='Language of the input-blob of text if known')
    parser.add_argument('--tgt-lang', required=True, help='Language of the input-blob of text if known')
    parser.add_argument('--src-file', default=None, help='Path to input file, default is stdin')
    parser.add_argument('--tgt-file', default=None, help='Path to output file, default is stdout')
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