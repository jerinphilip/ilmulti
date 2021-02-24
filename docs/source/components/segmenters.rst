Sentence Splitters
------------------

There are three classes of sentence-splitters provided. These include 

* a naive splitter which assumes each line in input text is a sentence and
  returns sentences split by lines.
* A regular expression based sentence-splitter which separates on the basis of
  known end of sentence markers.
* The above two cannot cover cases like decimals (e.g 9.2) or abbreviations
  (Mr. X, Dr. X). To accomodate these, a punkt tokenizer and trained models are
  provided.

These are available in two variations, one where the models are loaded for the
individual language and the other handling multiple languages.


Naive
^^^^^

.. autoclass:: ilmulti.ssplit.SimpleSplitter

Regular Expression Based
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: ilmulti.ssplit.PatternSplitter
.. autoclass:: ilmulti.ssplit.MultiPatternSplitter


Punkt Based 
^^^^^^^^^^^

.. autoclass:: ilmulti.ssplit.PunktSplitter
.. autoclass:: ilmulti.ssplit.MultiPunktSplitter




