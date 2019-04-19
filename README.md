# ilmulti

This repository houses tooling used to create the models on the leaderboard of
WAT-Tasks.

## Installation

```bash
# --user is optional
python3 -m pip install -r requirements.txt --user  
python3 setup.py install --user 

```


## Usage

```python3
from ilmulti.translator.pretrained import mm_all

translator = mm_all()
sample = translator("The most accurate translation of this sentence", tgt_lang='hi')
```
