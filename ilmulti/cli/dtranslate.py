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
        "--tgt-lang", required=True, help="Language of the input-blob of text if known"
    )
    parser.add_argument(
        "--max-tokens", required=True, help="Max tokens for translator", type=int
    )
    parser.add_argument(
        "--storage",
        required=True,
        help="Temporary storage location for dtranslate to cache for optimal batching",
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Path containing input file, default read from stdin",
    )
    parser.add_argument("--debug", action="store_true", help="Print debug statements")
    return parser


def dtranslate_main(args, text):
    filenames = text.splitlines()
    from ..translate import PRETRAINED_CONFIG, from_pretrained

    translator = from_pretrained(args.model)
    from ..e2e import DeferredTranslator
    from ..utils.storage import LMDBStorage

    storage = LMDBStorage(args.storage)
    dtranslator = DeferredTranslator.fromBlocking(translator, storage, args.max_tokens)

    for Id, fname in enumerate(filenames):
        with open(fname) as fp:
            content = fp.read()
            dtranslator.queue(Id, content, tgt_lang=args.tgt_lang)

    dtranslator.run()
    for Id, fname in enumerate(filenames):
        translation = dtranslator.collect(Id)
        translated_path = "{}.translated.txt".format(fname)
        with open(translated_path, "w+") as fp:
            print(translation, file=fp)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.input is None:
        input_file = sys.stdin
    else:
        input_file = open(args.input)

    blob = input_file.read()
    dtranslate_main(args, blob)
