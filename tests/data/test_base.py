"""
Unit tests for caproj.data.base submodule
"""
import contextlib
import json
import os
from unittest import mock, TestCase
import tempfile

import pandas as pd

from caproj.data.base import BaseData


class BaseDataIOTests(TestCase):
    """Tests to ensure caproj.data.BaseData IO ops function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.x = [0, 1, 1, 0]
        self.data = pd.DataFrame(
            {
                'PID': self.x,
                'y': [2, 3, 4, 5]
            }
        )
        return super().setUp()

    def test_from_file_csv(self):
        """Ensure csv is read and stored to BaseDataClass class"""
        with tempfile.TemporaryDirectory() as tmp:
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
        with tempfile.TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            self.data.to_csv(fp, index=False)
            df_read = BaseData.from_file(fp, copy_input=True).input_df
            self.assertEqual(
                pd.testing.assert_frame_equal(self.data, df_read),
                None,
            )

    def test_from_file_inputdf_not_created(self):
        """Ensure input_df persist only when specified"""
        with tempfile.TemporaryDirectory() as tmp:
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
        with self.assertRaises(Exception):
            BaseData.from_object(Invalid_object)

    def test_to_file(self):
        """Ensure to_file saves self.df to disk"""
        with tempfile.TemporaryDirectory() as tmp:
            Base = BaseData.from_object(self.data)
            fp_save = os.path.join(tmp, "test_save.csv")
            Base.to_file(fp_save)
            self.assertTrue(os.path.exists(fp_save))

    def test_log_record_count(self):
        """Ensure log_record_count returns log"""
        Base_object = BaseData.from_object(self.data)
        with self.assertLogs('BaseData', level='INFO') as logmsg:
            Base_object.log_record_count(id_col='PID')
            self.assertTrue(len(logmsg) > 0)

    def test_log_record_count_init(self):
        """Ensure BaseData init triggers log_record_count"""
        raise NotImplementedError

    def test_log_record_count_init_fails(self):
        """Ensure BaseData init log_record_count fails elegantly"""
        raise NotImplementedError


class BaseDataReadJsonTests(TestCase):
    """Tests to ensure ``BaseData`` _read_json method functions properly"""

    def setUp(self):
        """Set up data for tests"""
        # define dict for saving to json
        self.json_dict = {'a': 1, 'b': 2}
        # initialize BaseData class for use in tests
        self.Base = BaseData(pd.DataFrame(columns=['PID']), copy_input=False)
        # use ExitStack for opening a temp directory for use in tests
        with contextlib.ExitStack() as stack:
            # open temp directory context manager
            self.tmpdir = stack.enter_context(
                tempfile.TemporaryDirectory()
            )
            self.filepath = os.path.join(self.tmpdir, 'foo.json')
            # save json to temp dir
            with open(self.filepath, 'w') as fp:
                json.dump(self.json_dict, fp)
            self.assertTrue(os.path.exists(self.filepath))
            # ensure context manager closes after tests
            self.addCleanup(stack.pop_all().close)

    def test_read_json(self):
        """Ensure _read_json returns json dict from file"""
        read_dict = self.Base._read_json(self.filepath)
        self.assertDictEqual(self.json_dict, read_dict)

    def test_read_json_no_file_exists_log(self):
        """Ensure _read_json returns warning log msg when path doesn't exist"""
        with self.assertLogs('BaseData', level='WARNING') as logmsg:
            read_dict = self.Base._read_json('nonexistent path')
            self.assertEqual(read_dict, None)
            self.assertTrue("No data loaded" in logmsg.output[0])


class BaseDataColLintTests(TestCase):
    """Tests to ensure ``BaseData`` column linting functions properly"""

    def setUp(self):
        """Set up data for tests"""
        self.orig_colnames = ['test1', 'test_2', 'test 3', 'test-4']
        self.linted_colnames = ['test1', 'test_2', 'test_3', 'test_4']
        self.Base = BaseData(
            pd.DataFrame(columns=self.orig_colnames), copy_input=False
        )
        self.Base_nolint = BaseData(
            pd.DataFrame(columns=self.linted_colnames), copy_input=False
        )

    def test_lint_colnames(self):
        """Ensure lint_colnames fixes column name strings"""
        self.Base.lint_colnames()
        self.assertListEqual(
            list(self.Base.df.columns), self.linted_colnames
        )

    def test_lint_colnames_log_changed(self):
        """Ensure lint_colnames method logging works"""
        with self.assertLogs('BaseData', level='INFO') as logmsg:
            self.Base.lint_colnames()
            self.assertTrue("Column names changed" in logmsg.output[0])

    def test_lint_colnames_log_not_changed(self):
        """Ensure lint_colnames method logging works"""
        with self.assertLogs('BaseData', level='INFO') as logmsg:
            self.Base_nolint.lint_colnames()
            self.assertTrue("No column names changed" in logmsg.output[0])


class BaseDataColNameTests(TestCase):
    """Tests to ensure ``BaseData`` column renaming function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.orig_colnames = ['a', 'b', 'c', 'PID']
        self.new_colnames = ['1', '2', '3', 'PID']
        self.map_dict = dict(
            zip(self.orig_colnames[:3], self.new_colnames[:3])
        )
        self.Base = BaseData(
            pd.DataFrame(columns=self.orig_colnames), copy_input=False
        )

    def test_rename_columns_only_specified(self):
        """Ensure rename_columns only renames specified columns"""
        self.Base.rename_columns(map_dict=self.map_dict)
        print(self.Base.df.columns)
        self.assertListEqual(list(self.Base.df.columns), self.new_colnames)

    def test_rename_columns_json(self):
        """Ensure rename_columns converts json input to dict"""
        raise NotImplementedError

    def test_rename_columns_json_fails_no_file_exists(self):
        """Ensure rename_columns converts json input to dict"""
        raise NotImplementedError

    def test_rename_columns_log(self):
        """Ensure rename_columns logging works"""
        raise NotImplementedError

    def test_set_dtypes_json(self):
        """Ensure set_dtypes converts json input to dict"""
        raise NotImplementedError

    def test_set_dtypes_dict(self):
        """Ensure set_dtypes converts column dtypes using dict as input"""
        raise NotImplementedError

    def test_set_dtypes_log(self):
        """Ensure set_dtypes logging works"""
        raise NotImplementedError
