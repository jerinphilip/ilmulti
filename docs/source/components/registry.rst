Registry
========

While components provide an API to contruct the individual components, not all
of the components are compatible with each other. For example, a tokenizer from
``ilmulti-v1`` model will not be compatible with an ``ilmulti-v2`` translation
model due to a breaking change.

To prevent this, the library provides methods to build systems on the basis of
tags, ensuring the components constructed are compatible with each other.


Populating Registry
^^^^^^^^^^^^^^^^^^^
General Register
################
.. autofunction:: ilmulti.registry.register

Specialized Register
####################

.. autofunction:: ilmulti.registry.register_tokenizer
.. autofunction:: ilmulti.registry.register_splitter
.. autofunction:: ilmulti.registry.register_translator

Using Registry
^^^^^^^^^^^^^^
.. autofunction:: ilmulti.registry.build
.. autofunction:: ilmulti.registry.registry
