from argparse import ArgumentParser
import nltk
from .punkt import PunktTrainer, PunktSentenceTokenizer
from .utils import PunktDelimiter, inspect_tokenizer
import pickle

def test(lang, test_corpus_path, model):
    lang_vars = PunktDelimiter(lang)()
    model_uri = 'file:{}'.format(model)
    tokenizer = nltk.data.load(model_uri)
    tokenizer._lang_vars = lang_vars

    # inspect_tokenizer(tokenizer)

    with open(test_corpus_path) as test_file:
        contents = test_file.read()
        contents = contents.replace('\n', ' ')
        sentences = tokenizer.tokenize(contents)
        for sentence in sentences:
            print('>', sentence)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--test-corpus', type=str, required=True)
    parser.add_argument('--save-model', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)
    args = parser.parse_args()
    test(args.lang, args.test_corpus, args.save_model)
