"""
Unit tests for caproj.data.clean submodule
"""
import contextlib
import json
import math
import os
import unittest
import tempfile

import pandas as pd
import numpy as np

from caproj.data.clean import CleanMixin


class CleanMixinTests(unittest.TestCase):
    """Tests to ensure caproj.data.BaseData IO ops function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": [1, 2, np.nan],
            "PID": [np.nan, "test", "test"],
        }
        self.Base = CleanMixin()
        self.Base.df = pd.DataFrame().from_dict(self.colvalues_dict)
        )

    def test_remove_missing_records_single_col(self):
        """Ensure remove_missing_records works with single column input string"""
        raise NotImplementedError

    def test_remove_missing_records_multi_col(self):
        """Ensure remove_missing_records works with multi-column input list"""
        raise NotImplementedError

    def test_remove_missing_records_log(self):
        """Ensure remove_missing_records generates log"""
        raise NotImplementedError
