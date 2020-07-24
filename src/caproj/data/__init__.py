"""
caproj.data
~~~~~~~~~~~

This submodule contains the ``BaseData`` class, which aggregates ``caproj.data``
mixin classes and ``BaseDataOps`` class instantiation functionality.
"""
from .base import BaseDataOps
from .clean import CleanMixin

Mixins = [CleanMixin]
"""List of ``mixin`` classes inherited by the :class:`BaseData` class"""


class BaseData(*Mixins, BaseDataOps):
    """
    Inherit core class functionality from the ``BaseDataOps`` parent class
    and act as the core data operations class in which methods of
    specialized mixin classes are combined.
    """

    pass
