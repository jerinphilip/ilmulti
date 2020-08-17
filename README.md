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

The code is tested to work with the fairseq-fork which is branched from v0.7.2 and torch version 1.0.0.

```bash
# --user is optional
python3 -m pip install -r requirements.txt --user  
python3 setup.py install --user 

```

**Downloading Models**: The script
[`scripts/download-and-setup-models.sh`](./scripts/download-and-setup-models.sh)
downloads the model and dictionary files required for running
[`examples/mm_all.py`](./examples/mm_all.py). Which models to download
can be configured in the script.

A working example using the wrappers in this code can be found in this [Colab Notebook](https://colab.research.google.com/drive/1KOvjawhzPXOQ6RLlFBFeInkuuR0QAWTK?usp=sharing).

## Usage

```python3
from ilmulti.translator import from_pretrained

translator = from_pretrained(tag='mm-all')
sample = translator("The quick brown fox jumps over the lazy dog", tgt_lang='hi')
```
