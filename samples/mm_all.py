
from ilmulti.translator.pretrained import mm_all
from argparse import ArgumentParser

model = mm_all()

result = model('hello world', tgt_lang='hi')
from pprint import pprint
pprint(result)

