import sys
sys.path.insert(0, '.')

from ilmulti.translator.pretrained import from_pretrained
from ilmulti.utils import detect_lang
from argparse import ArgumentParser
from pprint import pprint

model = from_pretrained('mm-all-iter0')

def test(sample, language):
    result = model(sample, tgt_lang=language)
    pprint(result)
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--tgt-lang', choices=['en'])
    parser.add_argument('--input-file', type=str, default=None)
    args = parser.parse_args()
    
    def process(fp):
        for line in fp:
            line = line.strip()
            _, lang = detect_lang(line)[0]
            test(line, args.tgt_lang)

    if args.input_file is not None:
        with open(args.input_file) as fp:
            process(fp)
    else:
        process(sys.stdin)
