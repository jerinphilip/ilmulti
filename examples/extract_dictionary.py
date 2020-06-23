
from ilmulti.sentencepiece import build_tokenizer
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--tag', type=str, required=True)
    parser.add_argument('--outfile', type=str, required=True)

    # Optional
    parser.add_argument('--src', type=str)
    parser.add_argument('--tgt', type=str)
    parser.add_argument('--single', action='store_true')


    args = parser.parse_args()

    tokenizer = build_tokenizer(args.tag)
    if args.single:
        dictionary = tokenizer.single_dictionary(args.src, args.tgt)
        print(len(dictionary))
        dictionary.save(args.outfile)
    else:
        dictionary = tokenizer.dictionary()
        dictionary.save(args.outfile)
