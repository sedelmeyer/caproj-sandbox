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
