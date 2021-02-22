from argparse import ArgumentParser
import sys

def create_parser():
    from ..translate.pretrained import PRETRAINED_CONFIG
    parser = ArgumentParser(description='Translates a blob of text')
    parser.add_argument('--model', choices=list(PRETRAINED_CONFIG.keys()), help='Model to use in translation', required=True)
    parser.add_argument('--input', default=None, help='Path to input file, default is stdin')
    parser.add_argument('--debug', action='store_true', help='Print debug statements')
    return parser

def align_main(args, text):
    from ..translate import from_pretrained, PRETRAINED_CONFIG
    from ..align import BLEUAligner
    model = from_pretrained(args.model)
    aligner = BLEUAligner(model.translator, model.tokenizer, model.splitter)

    files = text.splitlines()
    for line in files:
        src, src_lang, tgt, tgt_lang = line.split('\t')
        with open(src) as srcf, open(tgt) as tgtf:
            src_content = srcf.read()
            tgt_content = tgtf.read()
            # translation = model(src_content, tgt_lang=tgt_lang)
            # hyps = [entry['tgt'] for entry in translation]
            _ , (src_aligned, tgt_aligned) = aligner(src_content, src_lang,
                    tgt_content, tgt_lang)

            aligned_fname = lambda fname, other: '{}-{}.aligned.txt'.format(fname, other)
            with open(aligned_fname(src, tgt_lang), 'w+') as fp:
                print('\n'.join(src_aligned), file=fp)

            with open(aligned_fname(tgt, src_lang), 'w+') as fp:
                print('\n'.join(tgt_aligned), file=fp)

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    align_main(args, blob)


