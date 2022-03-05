import sys
from argparse import ArgumentParser


def create_parser():
    from ..registry import REGISTRY

    parser = ArgumentParser(description="Translates a blob of text")
    parser.add_argument(
        "--model",
        choices=list(REGISTRY["e2e_translator"].keys()),
        help="Model to use in translation",
        required=True,
    )
    parser.add_argument(
        "--input", default=None, help="Path to input file, default is stdin"
    )
    parser.add_argument("--debug", action="store_true", help="Print debug statements")
    return parser


def align_main(args, text):
    from ..align import BLEUAligner
    from ..registry import build

    model = build("e2e_translator", args.model)
    aligner = BLEUAligner.fromE2ETranslator(model)

    files = text.splitlines()
    for line in files:
        src, src_lang, tgt, tgt_lang = line.split("\t")
        with open(src) as srcf, open(tgt) as tgtf:
            src_content = srcf.read()
            tgt_content = tgtf.read()
            # translation = model(src_content, tgt_lang=tgt_lang)
            # hyps = [entry['tgt'] for entry in translation]
            src_aligned, tgt_aligned = aligner.align_forward(
                src_content, src_lang, tgt_content, tgt_lang
            )

            aligned_fname = lambda fname, other: "{}-{}.aligned.txt".format(
                fname, other
            )
            with open(aligned_fname(src, tgt_lang), "w+") as fp:
                print("\n".join(src_aligned), file=fp)

            with open(aligned_fname(tgt, src_lang), "w+") as fp:
                print("\n".join(tgt_aligned), file=fp)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    align_main(args, blob)
