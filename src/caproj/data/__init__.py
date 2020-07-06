"""
caproj.data
~~~~~~~~~~~

This submodule contains the ``DataOps`` class, which aggregates ``caproj.data``
mixin classes and ``BaseData`` functionality.
"""
from .base import BaseData

Mixins = []
"""List of ``mixin`` classes inherited by the :class:`BaseData` class"""


class BaseDataOps(*Mixins, BaseData):
    """
    Inherit core class functionality from the ``BaseData`` parent class
    and act as the core data operations class in which methods of
    specialized mixin classes are combined.
    """
    pass
