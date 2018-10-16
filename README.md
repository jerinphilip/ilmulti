# parallel-filtering

This repository started out as a set of scripts to filter training data
based on a few values (perplexity, language-detection etc.)

Further, it has been extended with primitives to create training data
for Multiway translation models following Johnson et Al.

## Installation

```bash
pip3 install --user sentencepiece langdetect
python3 setup.py install --user # user is optional
```

## Usage

A script which uses most parts is `pf/compile.py`. You may take a look
at it, if you need further details.


### `SentencePieceTokenizer`

4K vocab sized [sentencepiece](https://github.com/google/sentencepiece)
models are trained and prepared for the following languages.

1. English
2. Hindi
3. Malayalam
4. Bengali
5. Telugu
6. Tamil
7. Urdu


```py
from pf.sentencepiece import SentencePieceTokenizer
tokenizer = SentencePieceTokenizer()
sequence = "Hello world!"
tokenizer(sequence, lang='en') 
```

If `lang` is not supplied, `langdetect` is used to detect language.
If model doesn't exist for the said language, it defaults to english.

### `ParallelDataset`

```py
from pf.dataset import ParallelDataset
prefix = path/to/dataset/train
exts = (<src>, <tgt>)
parallel = ParallelDataset(prefix, exts)
for src, tgt in parallel:
    print('>', src)
    print('<', tgt)
```

### `MultilingualDataset`

```py
from pf.dataset import ParallelDataset, MultilingualDataset
pair1 = ParallelDataset(prefix1, exts1)
pair2 = ParallelDataset(prefix2, exts2)
multi = MultilingualDataset([prefix1, prefix2])
for src, tgt in multi:
    print('>', src)
    print('<', tgt)

```

### `AgnosticTokenizedDataset`

This is additionally supplied with a language agnostic tokenizer enabled
by sentencepiece + langdetect, and gives a dataset for multiway
training.

```py
from pf.dataset import AgnosticTokenizedDataset
pairs = <list of ParallelDatasets>
tokenizer = SentencePieceTokenizer()
multi = AgnosticTokenizedDataset(pairs, tokenizer)
for src, tgt in multi:
    print('>', src)
    print('<', tgt)
```

### `ParallelWriter`

This is to convert a collection of parallel datasets to a multi-way trainable
dataset.

```
from pf.dataset import ParallelWriter
writer = ParallelWriter('dump', 'test', 'src', 'tgt')
for src, tgt in multi:
    writer.write(src, tgt)
```


