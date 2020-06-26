## More Documentation

The code works with three main components:


### 1. Segmenter

To handle segmenting a block of text into sentences, accounting for some
Indian Language delimiters. This is a bit crude and rule based and
contributed by [Binu Jasim](https://github.com/bnjasim).

### 2. Tokenization

We use [SentencePiece](https://github.com/google/sentencepiece) to
as an unsupervised tokenizer for Indian languages, which works
surprisingly well in our experiments. There are trained models on
whatever corpora we could find for the specific languages in
[sentencepiece/models](./sentencepiece/models) of 4000 vocabulary units
and 8000 vocabulary units.

Training a joint SentencePiece over all languages lead to character
level tokenization for under-represented languages and since there isn't
much to gain due to the difference in scripts, we use individual
tokenizers for each language. Combined however, this will have less than
4000 x |#languages| as some common English code mixes come in. This
however, makes the MT system robust in some sense to code-mixed inputs.

### 3. Translator

Translator is a wrapper around a
[fairseq](https://github.com/pytorch/fairseq) which we have reused for
some web-interfaces.


