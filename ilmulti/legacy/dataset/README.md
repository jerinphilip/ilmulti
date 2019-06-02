
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


