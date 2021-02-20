# Mining Parallel Data from PIB

This library is used to mine parallel-sentences for training MT models in
Indian languages. The additional data is then fed-back to the training pipeline
to improve the machine-translation models.



Briefly, the task involves the following, given the articles are stored with
their IDs from the Press Information Bureau website.

1. **Sentence Splitting**: A candidate pair of articles (source, candidate) have to
   split into sentences to be able to extract alignments at a sentence-level.
2. **Tokenization**: Machine-Translation pipelines use vocabulary reduction methods
   like Byte Pair Encoding (BPE) and SentencePiece. Tokenization tokenizes and
   extracts the tokens using these.
3. **Translation**: Alignment for PIB involves BLEUAlign, which internally uses an
   MT model. Before BLEUAlign, we need to obtain a translation of the
   source-document. This is done through `Translator` to have (source,
   translation, candidate).
4. **Alignment**: Finally, once we have the translation from the above step, we can run
   BLEUAlign with (source, translation , candidate) to obtain
   parallel-sentences.

Below find a walkthrough with pseudocode on how to use *ilmulti*'s API to
accomplish this, as an example application.

## Sentence-Splitting

## Tokenization 

## Translation

## Aligning articles

