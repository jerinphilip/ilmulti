Caveat Emptor
=============

* The source is an assortment of things the author found of constant reuse in
  machine-translation pipelines for Indian languages. The API is subject to
  change for improvements until a ``v1.0.0``.
* Imports are usually made at the point of call. This simplifies not having to
  load heavy libraries (*e.g.*: ``torch``) which are used in translation. This
  implies that your code might fail a few hours into training with an
  ``ImportError``.
* Throughout the library, methods attempt to detect the language and warn the
  user in case of language-mismatch. You can potentially speed this up with
  passing a language parameter. This is set to alert the user existence of such
  in noisy Indian language datasets, which often end up code-mixed.
