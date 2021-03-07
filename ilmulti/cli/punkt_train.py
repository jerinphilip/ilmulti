from argparse import ArgumentParser
from nltk.tokenize.punkt import PunktTrainer, PunktSentenceTokenizer
import nltk
import pickle
from ..ssplit.punkt import PunktDelimiter, inspect_tokenizer



def train(args):
    # Refer:
    # https://github.com/alvations/DLTK/blob/84bb7daeda21c18424518731928aea103c15caa1/dltk/tokenize/tokenizer.py#L37

    def buffered_read(fp, num_lines, max_lines):
        _buffer = []
        iterator = iter(fp)
        idx = 0
        while True:
            try:
                line = next(iterator)
            except UnicodeDecodeError:
                continue

            _buffer.append(line)
            idx = idx + 1
            if idx % num_lines == 0:
                yield '\n'.join(_buffer)
                _buffer = []
            if idx >= max_lines:
                break
        yield '\n'.join(_buffer)


    with open(args.train_corpus) as fp:
        language_vars = PunktDelimiter(args.lang)()
        punkt = PunktTrainer(lang_vars=language_vars)
        # contents = fp.read()
        iterator = buffered_read(fp, args.lines_buffer, args.max_lines) 
        for idx, _buffer in enumerate(iterator, 1):
            print("{idx} batches processed...".format(idx=idx))
            punkt.train(_buffer, verbose=False, finalize=False)

        punkt.finalize_training(verbose=True)
        model = PunktSentenceTokenizer(punkt.get_params())

        with open(args.save_model, 'wb+') as save_file:
            pickle.dump(model, save_file, protocol=pickle.HIGHEST_PROTOCOL)

    # inspect_tokenizer(model)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--train-corpus', type=str, required=True)
    parser.add_argument('--save-model', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)
    parser.add_argument('--lines-buffer', type=int, default=250000)
    parser.add_argument('--max-lines', type=int, default=10**6)
    args = parser.parse_args()
    train(args)

