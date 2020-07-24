"""
Unit tests for caproj.data submodule
"""
import unittest

import pandas as pd

from caproj.data import BaseData


class BaseDataTests(unittest.TestCase):
    """Tests to ensure caproj.data.BaseData class works properly"""

    def setUp(self):
        """Set up data for tests"""
        self.data = pd.DataFrame(columns=["PID", "a"])

    def test_from_object_df(self):
        """Ensure dataframe object is read and stored to BaseData class"""
        df_read = BaseData.from_object(self.data).df
        self.assertEqual(
            pd.testing.assert_frame_equal(self.data, df_read), None,
        )
