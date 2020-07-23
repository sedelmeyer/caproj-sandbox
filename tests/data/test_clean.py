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


class ConcatValuesTests(unittest.TestCase):
    """Tests to ensure CleanMixin concat_values method function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": [1, 2, 3],
            "b": [1, 2, np.nan],
            "PID": ["test", "test", "test"],
        }
        self.to_colname = "test"
        self.Base = CleanMixin()
        self.Base.df = pd.DataFrame().from_dict(self.colvalues_dict)

    def test_concat_values_numbers_concat(self):
        """Ensure concat_values concatenates numeric values instead of adds"""
        self.Base.concat_values(columns=["a", "b"], to_colname=self.to_colname)
        self.assertListEqual(
            list(self.Base.df[self.to_colname].values), ["11.0", "22.0", "3nan"]
        )

    def test_concat_values_single_col(self):
        """Ensure concat_values works with single column input string"""
        self.Base.concat_values(columns="a", to_colname=self.to_colname)
        self.assertListEqual(
            list(self.Base.df[self.to_colname].values), ["1", "2", "3"]
        )

    def test_concat_values_multi_col(self):
        """Ensure concat_values works with multi-column input list"""
        self.Base.concat_values(
            columns=["a", "b", "PID"], to_colname=self.to_colname
        )
        self.assertListEqual(
            list(self.Base.df[self.to_colname].values),
            ["11.0test", "22.0test", "3nantest"],
        )

    def test_concat_values_log(self):
        """Ensure concat_values generates log"""
        with self.assertLogs("caproj.data.clean", level="INFO") as logmsg:
            self.Base.concat_values(columns="a", to_colname=self.to_colname)
            self.assertTrue(len(logmsg.output) == 3)
