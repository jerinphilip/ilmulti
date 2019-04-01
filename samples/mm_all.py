
from ilmulti.translator.pretrained import mm_all
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--path', type=str, required=True)
args = parser.parse_args()

model = mm_all(root=args.path)

result = model('hello world', tgt_lang='hi')
from pprint import pprint
pprint(result)

