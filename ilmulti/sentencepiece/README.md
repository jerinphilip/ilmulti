
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

If `lang` is not supplied, `langid` is used to detect language.
If model doesn't exist for the said language, it defaults to english.
