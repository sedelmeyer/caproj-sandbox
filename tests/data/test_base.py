"""
Unit tests for caproj.data.base submodule
"""
import os
from unittest import TestCase
from tempfile import TemporaryDirectory

import pandas as pd

from caproj.data.base import BaseData


class BaseDataTests(TestCase):
    """Tests to ensure class caproj.data.BaseData functions properly"""

    def setUp(self):
        """Set up data for tests"""
        self.x = [0, 1, 1, 0]
        self.data = pd.DataFrame(
            {
                'x': self.x,
                'y': [2, 3, 4, 5]
            }
        )
        return super().setUp()

    def test_from_file_csv(self):
        """Ensure csv is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            self.data.to_csv(fp, index=False)
            df_read = BaseData.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(self.data, df_read),
                None,
            )

    def test_from_file_fail(self):
        """Ensure from_file fails elegantly with wrong filetype read"""
        fp = "test.txt"
        with self.assertRaises(TypeError):
            BaseData.from_file(fp)

    def test_from_file_inputdf_persists(self):
        """Ensure input_df persist only when specified"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            self.data.to_csv(fp, index=False)
            df_read = BaseData.from_file(fp, copy_input=True).input_df
            self.assertEqual(
                pd.testing.assert_frame_equal(self.data, df_read),
                None,
            )

    def test_from_file_inputdf_not_created(self):
        """Ensure input_df persist only when specified"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            self.data.to_csv(fp, index=False)
            with self.assertRaises(AttributeError):
                BaseData.from_file(fp).input_df

    def test_from_object_df(self):
        """Ensure dataframe object is read and stored to BaseDataClass class"""
        df_read = BaseData.from_object(self.data).df
        self.assertEqual(
            pd.testing.assert_frame_equal(self.data, df_read),
            None,
        )

    def test_from_object_class(self):
        """Ensure class.df object is read and stored to BaseDataClass class"""
        Base_object = BaseData.from_object(self.data)
        df_read = BaseData.from_object(Base_object).df
        self.assertEqual(
            pd.testing.assert_frame_equal(self.data, df_read),
            None,
        )

    def test_from_object_fail(self):
        """Ensure from_object fails elegantly with invalid object"""
        class InvalidClass(object):
            pass
        Invalid_object = InvalidClass()
        with self.assertRaises(TypeError):
            BaseData.from_object(Invalid_object)

    def test_to_file(self):
        """Ensure to_file saves self.df to disk"""
        with TemporaryDirectory() as tmp:
            Base = BaseData.from_object(self.data)
            fp_save = os.path.join(tmp, "test_save.csv")
            Base.to_file(fp_save)
            assert os.path.exists(fp_save)

    def test_log_record_count(self):
        """Ensure log_record_count returns log"""
        Base_object = BaseData.from_object(self.data)
        with self.assertLogs('caproj.data.base', level='INFO') as log:
            Base_object.log_record_count(id_col='x')
