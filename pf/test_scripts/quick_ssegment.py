import numpy as np
import sys
from argparse import ArgumentParser

lsentences = []
sentences_per_lines = []
llines = []

parser = ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--threshold', type=int, required=True)

args = parser.parse_args()
outfile = open(args.output, 'w+')
with open(args.input) as fp:
    for line in fp:
        line = line.strip()
        sentences = line.split('.')
        for sentence in sentences:
            lsentences.append(len(sentence))
            if len(sentence) > args.threshold:
                print(sentence+'.', file=outfile)
        llines.append(len(line))
        sentences_per_lines.append(len(sentences))


def summarize(ls):
    ls = np.array(ls)
    print(ls.min(), ls.mean(), ls.max())

summarize(lsentences)
summarize(sentences_per_lines)
summarize(llines)

            
