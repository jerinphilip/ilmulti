Meta
====

This document summarizes the classes that pop-up around the documentation as
being inherited.

Functors
^^^^^^^^

.. autoclass:: ilmulti.meta.ForwardFunctor
.. autoclass:: ilmulti.meta.InvertibleFunctor

MultiFunctors
^^^^^^^^^^^^^

Multiway / multi-lang nature of the models are captured and interface unified
with these abstract classes. Adhering to the constraints laid out by these API
provides certain functions for free.

A :class:`MultiFunctor` denotes an operation which takes in a language argument
and switches the underlying functor. This is useful when one wants to load each
individual language's :class:`Functor` for a system that operates with a
combination of languages.

.. autoclass:: ilmulti.meta.MultiFunctor

A :class:`PseudoMultiFunctor` allows the properties to be used for something
that isn't a combination of systems but can handle multiple languages
internally. For example a single many-to-many translation model translating
amongst languages, or a SentencePiece model using a joint vocabulary.

.. autoclass:: ilmulti.meta.PseudoMultiFunctor

ConfigBuildable
^^^^^^^^^^^^^^^
.. autoclass:: ilmulti.meta.ConfigBuildable

Filters
^^^^^^^

.. autoclass:: ilmulti.meta.Filter

