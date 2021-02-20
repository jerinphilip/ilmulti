### Installation

`langid` is required for, language-identification. `sentencepiece` is required
for tokenizers and translators using sentencepiece tokenizers to work.

```bash
python3 -m pip install langid 
python3 -m pip install sentencepiece 
```

`nltk@develop` has [a punkt
modification](https://github.com/nltk/nltk/pull/2587) which probably haven't
yet made to a new release, triggered by the experiments around this library.

```bash
python3 -m pip install git+https://github.com/nltk/nltk@develop
```

The following might break your existing environment, as they're outdated. The
models however work with this source. It may be Preferable to install and setup
this library in a virtual enviroment therefore.

```bash
python3 -m pip install torch==1.0.0
python3 -m pip install git+https://github.com/jerinphilip/fairseq-ilmt@lrec-2020
```

These are required for the translation functionality through fairseq models to
work.
