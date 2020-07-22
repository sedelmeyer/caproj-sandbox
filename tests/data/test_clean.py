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
    """Tests to ensure caproj.data.CleanMixin methods function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": [1, 2, np.nan],
            "PID": [np.nan, "test", "test"],
        }
        self.Base = CleanMixin()
        self.Base.df = pd.DataFrame().from_dict(self.colvalues_dict)

    def test_remove_missing_records_single_col(self):
        """Ensure remove_missing_records works with single column input string"""
        self.Base.remove_missing_records(columns="a")
        self.assertEqual(len(self.Base.df), 2)

    def test_remove_missing_records_multi_col(self):
        """Ensure remove_missing_records works with multi-column input list"""
        self.Base.remove_missing_records(columns=["a", "PID"])
        self.assertEqual(len(self.Base.df), 1)

    def test_remove_missing_records_log(self):
        """Ensure remove_missing_records generates log"""
        with self.assertLogs("caproj.data.clean", level="INFO") as logmsg:
            self.Base.remove_missing_records(columns="a")
            self.assertTrue(len(logmsg.output) == 3)


class MakeIdTests(unittest.TestCase):
    """Tests to ensure CleanMixin make_record_keys method function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": [1, 2, 3],
            "a": [1, 2, np.nan],
            "PID": ["test", "test", "test"],
        }
        self.Base = CleanMixin()
        self.Base.df = pd.DataFrame().from_dict(self.colvalues_dict)

    def test_make_record_keys_numbers_concat(self):
        """Ensure make_record_keys concatenates numeric values instead of adds"""
        raise NotImplementedError

    def test_make_record_keys_single_col(self):
        """Ensure make_record_keys works with single column input string"""
        raise NotImplementedError

    def test_make_record_keys_multi_col(self):
        """Ensure make_record_keys works with multi-column input list"""
        raise NotImplementedError

    def test_make_record_keys_log(self):
        """Ensure make_record_keys generates log"""
        raise NotImplementedError
