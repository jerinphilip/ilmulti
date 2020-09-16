# ilmulti

This repository houses tooling used to create the models on the
leaderboard of WAT-Tasks. We provide wrappers to models which are
trained via [pytorch/fairseq](http://github.com/pytorch/fairseq) to
translate. Installation and usage intructions are provided below.

* **Training**: We use a separate fork of
  [pytorch/fairseq](http://github.com/pytorch/fairseq) at
  [jerinphilip/fairseq-ilmt](http://github.com/jerinphilip/fairseq-ilmt) for
  training to optimize for our cluster and to plug and play data
  easily.

* **Pretrained Models and Other Resources**: 
  [preon.iiit.ac.in/~jerin/bhasha](http://preon.iiit.ac.in/~jerin/bhasha)


## Installation

The code is tested to work with the fairseq-fork which is branched from v0.8.0 and torch version 1.0.0.

```bash
# --user is optional

# Check requirements.txt, packages for translation:
# fairseq-ilmt@lrec-2020 and torch  are not enabled by default.
python3 -m pip install -r requirements.txt --user  

# Once requirements are installed, you can install ilmulti into library.

python3 setup.py install --user 

```

**Downloading Models**: The script
[`scripts/download-and-setup-models.sh`](./scripts/download-and-setup-models.sh)
downloads the model and dictionary files required for running
[`examples/mm_all.py`](./examples/mm_all.py). Which models to download can be
configured in the script.

A working example using the wrappers in this code can be found in [this](https://colab.research.google.com/drive/1KOvjawhzPXOQ6RLlFBFeInkuuR0QAWTK?usp=sharing) colab notebook. Thanks @Nimishasri.

## Usage

```python3
from ilmulti.translator import from_pretrained

translator = from_pretrained(tag='mm-all')
sample = translator("The quick brown fox jumps over the lazy dog", tgt_lang='hi')
```

The code works with three main components:

### 1. Segmenter

Also sentence-tokenizer. To handle segmenting a block of text into sentences,
accounting for some Indian Language delimiters. 

1. PatternSegmenter: There  is a bit crude and rule based implementation
   contributed by [Binu Jasim](https://github.com/bnjasim).
2. PunktSegmenter: changed this to an unsupervised learnt PunktTokenizer

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
some web-interfaces and demos.

