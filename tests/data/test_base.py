"""
Unit tests for caproj.data.base submodule
"""
import os
from unittest import TestCase
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from caproj.data.base import BaseData


class BaseDataClassTests(TestCase):
    """Tests to ensure class data.BaseDataClass functions properly"""

    def test_from_file_csv(self):
        """ensure csv is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.csv')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_xls(self):
        """ensure xls is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xls')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_xlsx(self):
        """ensure xlsx is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xlsx')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_fail(self):
        """ensure from_file fails elegantly with wrong filetype read"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "test.txt")
            open(fp, 'a').close()
            assert os.path.exists(fp)
            with self.assertRaises(TypeError):
                BaseDataClass.from_file(fp)

    def test_from_file_inputdf_persists(self):
        """ensure input_df persist only when specified"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xlsx')
            df_read = BaseDataClass.from_file(fp, copy_input=True).input_df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )
            with self.assertRaises(AttributeError):
                BaseDataClass.from_file(fp).input_df

    def test_from_object_df(self):
        """ensure dataframe object is read and stored to BaseDataClass class"""
        df_test = make_simple_dataframe()
        df_read = BaseDataClass.from_object(df_test).df
        self.assertEqual(
            pd.testing.assert_frame_equal(df_test, df_read),
            None,
        )

    def test_from_object_class(self):
        """ensure class.df object is read and stored to BaseDataClass class"""
        df_test = make_simple_dataframe()
        Base_object = BaseDataClass.from_object(df_test)
        df_read = BaseDataClass.from_object(Base_object).df
        self.assertEqual(
            pd.testing.assert_frame_equal(df_test, df_read),
            None,
        )

    def test_from_object_fail(self):
        """ensure from_object fails elegantly with invalid object"""
        class InvalidClass(object):
            pass
        Invalid_object = InvalidClass()
        with self.assertRaises(TypeError):
            BaseDataClass.from_object(Invalid_object)

    def test_to_file(self):
        """ensure to_file saves self.df to disk"""
        with TemporaryDirectory() as tmp:
            df_test = make_simple_dataframe()
            Base = BaseDataClass.from_object(df_test)
            fp_save = os.path.join(tmp, "test_save.csv")
            Base.to_file(fp_save)
            assert os.path.exists(fp_save)
