"""
caproj.data.clean
~~~~~~~~~~~~~~~~~

This module contains BaseData mixin class to clean the NYC Capital Projects dataset

**Module classes:**

.. autosummary::

   CleanMixin

**Module variables:**

.. autosummary::

   log

|
"""
import json
import logging
import math
import os

import pandas as pd

from caproj.logger import logfunc

log = logging.getLogger(__name__)
"""``logging.getLogger`` instance for module"""


class CleanMixin(object):
    """``BaseData`` mixin class methods for cleansing the NYC capital projects dataset
    """

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def remove_missing_records(self, columns):
        """Delete records with missing values in specified columns
        """
        columns = list(columns) if type(columns) != list else columns
        self.df.dropna(subset=columns, axis=0, inplace=True)
