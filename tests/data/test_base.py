"""
Unit tests for caproj.data.base submodule
"""
import contextlib
import json
import math
import os
import unittest
import tempfile

import pandas as pd
import numpy as np

from caproj.data.base import BaseData


class BaseDataIOTests(unittest.TestCase):
    """Tests to ensure caproj.data.BaseData IO ops function properly"""

    def setUp(self):
        """Set up data for tests"""
        self.x = [0, 1, 1, 0]
        self.data = pd.DataFrame({"PID": self.x, "y": [2, 3, 4, 5]})
        return super().setUp()

    def test_from_file_csv(self):
        """Ensure csv is read and stored to BaseDataClass class"""
        with tempfile.TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "test.csv")
            self.data.to_csv(fp, index=False)
            df_read = BaseData.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(self.data, df_read), None,
            )

    def test_from_file_fail(self):
        """Ensure from_file fails elegantly with wrong filetype read"""
        fp = "test.txt"
        with self.assertRaises(TypeError):
            BaseData.from_file(fp)

    def test_from_file_inputdf_persists(self):
        """Ensure df_input persist only when specified"""
        with tempfile.TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "test.csv")
            self.data.to_csv(fp, index=False)
            df_read = BaseData.from_file(fp, copy_input=True).df_input
            self.assertEqual(
                pd.testing.assert_frame_equal(self.data, df_read), None,
            )

    def test_from_file_inputdf_not_created(self):
        """Ensure df_input persist only when specified"""
        with tempfile.TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "test.csv")
            self.data.to_csv(fp, index=False)
            with self.assertRaises(AttributeError):
                BaseData.from_file(fp).df_input

    def test_from_object_df(self):
        """Ensure dataframe object is read and stored to BaseDataClass class"""
        df_read = BaseData.from_object(self.data).df
        self.assertEqual(
            pd.testing.assert_frame_equal(self.data, df_read), None,
        )

    def test_from_object_class(self):
        """Ensure class.df object is read and stored to BaseDataClass class"""
        Base_object = BaseData.from_object(self.data)
        df_read = BaseData.from_object(Base_object).df
        self.assertEqual(
            pd.testing.assert_frame_equal(self.data, df_read), None,
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
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            Base_object.log_record_count(id_col="PID")
            self.assertTrue(len(logmsg) > 0)

    def test_log_record_count_init(self):
        """Ensure BaseData init triggers log_record_count"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            BaseData(self.data, copy_input=False)
            self.assertTrue(
                "Number of project change records" in "".join(logmsg.output)
            )

    def test_log_record_count_init_fails(self):
        """Ensure BaseData init log_record_count fails elegantly"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            Base = BaseData(pd.DataFrame(columns=["a", "b"]), copy_input=False)
            self.assertListEqual(["a", "b"], list(Base.df.columns))
            self.assertTrue(
                "unable to log record count" in "".join(logmsg.output)
            )


class BaseDataReadJsonMapDictTests(unittest.TestCase):
    """Tests to ensure ``BaseData`` _read_json method functions properly"""

    def setUp(self):
        """Set up data for tests"""
        # define dict for saving to json
        self.json_dict = self.map_dict = {"a": 1, "b": 2}
        # initialize BaseData class for use in tests
        self.Base = BaseData(pd.DataFrame(columns=["PID"]), copy_input=False)
        # use ExitStack for opening a temp directory for use in tests
        with contextlib.ExitStack() as stack:
            # open temp directory context manager
            self.tmpdir = stack.enter_context(tempfile.TemporaryDirectory())
            self.filepath = os.path.join(self.tmpdir, "foo.json")
            # save json to temp dir
            with open(self.filepath, "w") as fp:
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
        with self.assertLogs("BaseData", level="WARNING") as logmsg:
            read_dict = self.Base._read_json("nonexistent path")
            self.assertEqual(read_dict, None)
            self.assertTrue("No data loaded" in logmsg.output[0])

    def test_map_dict_json_return_input_dict(self):
        """Ensure _map_dict_json returns input map_dict"""
        return_dict = self.Base._map_dict_json(map_dict=self.map_dict)
        self.assertDictEqual(return_dict, self.map_dict)

    def test_map_dict_json_log_input_dict(self):
        """Ensure _map_dict_json logs input map_dict action"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            _ = self.Base._map_dict_json(
                map_dict=self.map_dict, log_text="test"
            )
            self.assertTrue("map_dict" and "test" in logmsg.output[0].lower())

    def test_map_dict_json_return_input_json(self):
        """Ensure _map_dict_json reads json and returns map_dict"""
        return_dict = self.Base._map_dict_json(json_path=self.filepath)
        self.assertDictEqual(return_dict, self.json_dict)

    def test_map_dict_json_log_input_json(self):
        """Ensure _map_dict_json logs json input action"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            _ = self.Base._map_dict_json(
                json_path=self.filepath, log_text="test"
            )
            self.assertTrue(
                self.filepath and "test" in logmsg.output[0].lower()
            )

    def test_map_dict_json_fail_input_json(self):
        """Ensure _map_dict_json fails elegantly with nonexistent json path"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            return_dict = self.Base._map_dict_json(
                json_path="nonexistent path", log_text="test"
            )
            self.assertEqual(return_dict, None)
            self.assertTrue("JSON failed" and "test" in "".join(logmsg.output))

    def test_map_dict_json_log_neither_dict_nor_json(self):
        """Ensure _map_dict_json logs when neither map_dict nor json given"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            return_dict = self.Base._map_dict_json(
                map_dict=None, json_path=None, log_text="test"
            )
            self.assertEqual(return_dict, None)
            self.assertTrue(
                "Neither a map_dict nor json_path"
                and "test" in "".join(logmsg.output)
            )


class BaseDataColLintTests(unittest.TestCase):
    """Tests to ensure ``BaseData`` column linting functions properly"""

    def setUp(self):
        """Set up data for tests"""
        self.orig_colnames = ["test1", "test_2", "test 3", "test-4"]
        self.linted_colnames = ["test1", "test_2", "test_3", "test_4"]
        self.Base = BaseData(
            pd.DataFrame(columns=self.orig_colnames), copy_input=False
        )
        self.Base_nolint = BaseData(
            pd.DataFrame(columns=self.linted_colnames), copy_input=False
        )

    def test_lint_colnames(self):
        """Ensure lint_colnames fixes column name strings"""
        self.Base.lint_colnames()
        self.assertListEqual(list(self.Base.df.columns), self.linted_colnames)

    def test_lint_colnames_log_changed(self):
        """Ensure lint_colnames method logging works"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.lint_colnames()
            self.assertTrue("Column names changed" in logmsg.output[0])

    def test_lint_colnames_log_not_changed(self):
        """Ensure lint_colnames method logging works"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base_nolint.lint_colnames()
            self.assertTrue("No column names changed" in logmsg.output[0])


class BaseDataColNameTests(unittest.TestCase):
    """Tests to ensure ``BaseData`` column renaming function properly"""

    # TODO: Refactor to remove _map_dict_json logic from rename_columns tests

    def setUp(self):
        """Set up data for tests"""
        self.orig_colnames = ["a", "b", "c", "PID"]
        self.new_colnames = ["1", "2", "3", "PID"]
        self.map_dict = dict(zip(self.orig_colnames[:3], self.new_colnames[:3]))
        self.Base = BaseData(
            pd.DataFrame(columns=self.orig_colnames), copy_input=False
        )

    def test_rename_columns_only_specified(self):
        """Ensure rename_columns only renames specified columns"""
        self.Base.rename_columns(map_dict=self.map_dict)
        self.assertListEqual(list(self.Base.df.columns), self.new_colnames)

    def test_rename_columns_json(self):
        """Ensure rename_columns renames columns using json dict"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "foo.json")
            with open(filepath, "w") as fp:
                json.dump(self.map_dict, fp)
            with self.assertLogs("BaseData", level="INFO") as logmsg:
                self.Base.rename_columns(json_path=filepath)
                self.assertListEqual(
                    list(self.Base.df.columns), self.new_colnames
                )
                self.assertTrue("Column names mapped" in logmsg.output[0])

    def test_rename_columns_json_fails_no_file_exists(self):
        """Ensure rename_columns fails elegantly when json does not exist"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.rename_columns(json_path="nonexistent path")
            self.assertListEqual(list(self.Base.df.columns), self.orig_colnames)
            self.assertTrue("JSON failed" in "".join(logmsg.output))

    def test_rename_columns_log(self):
        """Ensure rename_columns logging works"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.rename_columns()
            self.assertListEqual(list(self.Base.df.columns), self.orig_colnames)
            self.assertTrue(
                "Neither a map_dict nor json_path" in "".join(logmsg.output)
            )


class BaseDataColDtypeTests(unittest.TestCase):
    """Tests to ensure ``BaseData`` column dtype conversion functions properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": ["1", "2", "3"],
            "b": [1, 2, "test"],
            "c": [1, 2, "2020-01-01"],
            "PID": ["test", "test", "test"],
        }
        self.map_dict = {
            "a": "integer",
            "b": "float",
            "c": "datetime",
            "PID": "unsigned",
        }
        self.expected_error_counts = [0, 1, 2, 3]
        self.Base = BaseData(
            pd.DataFrame().from_dict(self.colvalues_dict), copy_input=False
        )

    def test_to_datetime_ignore(self):
        """Ensure _to_datetime generates ignore series with expected behavior"""
        series_ignore, _, _ = self.Base._to_datetime(colname="c")
        self.assertTrue(1 and 2 in series_ignore.values)

    def test_to_datetime_coerce(self):
        """Ensure _to_datetime generates coerced series values"""
        _, series_coerce, _ = self.Base._to_datetime(colname="c")
        self.assertEqual(sum(series_coerce.isnull()), 2)
        for val in series_coerce.values:
            self.assertTrue(isinstance(val, np.datetime64))

    def test_to_datetime_errors(self):
        """Ensure _to_datetime returns error dict of correct length"""
        _, _, error_dict = self.Base._to_datetime(colname="c")
        self.assertEqual(len(error_dict), 2)

    def test_to_datetime_errors_no_nan(self):
        """Ensure _to_datetime does not included NaN values in error_dict"""
        Base = BaseData(
            pd.DataFrame().from_dict({"c": [1, np.nan, "2020-01-01"]}),
            copy_input=False,
        )
        _, _, error_dict = Base._to_datetime(colname="c")
        print(error_dict)
        self.assertEqual(len(error_dict), 1)
        for val in error_dict.values():
            self.assertFalse(math.isnan(val))

    def test_set_dtypes_dict_failure(self):
        """Ensure set_dtypes fails to set dtype_errors when no map_dict returned"""
        self.Base.set_dtypes(json_path="nonexistent path")
        with self.assertRaises(AttributeError):
            self.dtype_errors

    def test_set_dtypes_json(self):
        """Ensure set_dtypes converts json input to dict"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "foo.json")
            with open(filepath, "w") as fp:
                json.dump(self.map_dict, fp)
            with self.assertLogs("BaseData", level="INFO") as logmsg:
                self.Base.set_dtypes(json_path=filepath)
                log_output = "".join(logmsg.output)
                self.assertTrue(
                    "mapped using {}".format(filepath) in log_output
                )
                self.assertTrue("dtype conversion" in log_output)

    def test_set_dtypes_error_dict_stored(self):
        """Ensure set_dtypes stores dtype_errors dict as attribute"""
        self.Base.set_dtypes(map_dict=self.map_dict)
        self.assertTrue(hasattr(self.Base, "dtype_errors"))
        self.assertListEqual(
            list(self.colvalues_dict.keys()),
            list(self.Base.dtype_errors.keys()),
        )

    def test_set_dtypes_to_numeric_int_values(self):
        """Ensure set_dtype 'integer' dtype logic works"""
        for dtype in ["integer", "signed", "unsigned"]:
            self.Base.set_dtypes(map_dict={"a": dtype})
            for val in self.Base.df["a"]:
                self.assertTrue(isinstance(val, int))

    def test_set_dtypes_to_numeric_float_values(self):
        """Ensure set_dtype 'float' dtype logic works"""
        self.Base.set_dtypes(map_dict={"a": "float"})
        for val in self.Base.df["a"]:
            self.assertTrue(isinstance(val, float))

    def test_set_dtypes_to_datetime_values_coerced(self):
        """Ensure set_dtype 'datetime' dtype logic works"""
        self.Base.set_dtypes(map_dict={"c": "datetime"}, coerce=True)
        self.assertTrue(
            np.datetime64 in [type(val) for val in self.Base.df["c"].values]
        )

    def test_set_dtypes_to_string_values(self):
        """Ensure set_dtype 'string' dtype logic works"""
        self.Base.set_dtypes(map_dict={"b": "string"})
        for val in self.Base.df["b"]:
            self.assertTrue(isinstance(val, str))

    def test_set_dtypes_invalid_dtype_values(self):
        """Ensure set_dtype invalid dtype logic works"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.set_dtypes(map_dict={"a": "invalid dtype"})
            self.assertTrue(
                "dtype is not a valid input" in "".join(logmsg.output)
            )

    def test_set_dtypes_coerce_log(self):
        """Ensure set_dtype 'coerce' option generates special log"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.set_dtypes(map_dict={"a": "integer"}, coerce=True)
            self.assertTrue(
                "All dtype conversion error values will be deleted and left blank"
                in "".join(logmsg.output)
            )

    def test_set_dtypes_log_no_errors(self):
        """Ensure set_dtype 'coerce' option generates special log"""
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.set_dtypes(map_dict={"a": "string"})
            self.assertTrue("encountered no errors" in "".join(logmsg.output))

    def test_set_dtypes_log_change_errors(self):
        with self.assertLogs("BaseData", level="INFO") as logmsg:
            self.Base.set_dtypes(map_dict=self.map_dict)
            print(self.Base.df)
            for (col, dtype), num in zip(
                self.map_dict.items(), self.expected_error_counts
            ):
                print(f"{col}, {dtype}, {num}")
                is_log = "'{0}' dtype conversion to '{1}' encountered {2} errors".format(
                    col, dtype, "no" if num == 0 else num
                )
                print(is_log)
                print(logmsg.output)
                self.assertTrue(is_log in "".join(logmsg.output))

    def test_set_dtypes_ignore_changes_df(self):
        """Ensure resulting dataframe has no NaN values if coerce set to False"""
        self.Base.set_dtypes(map_dict=self.map_dict, coerce=False)
        self.assertListEqual([1, 2, "test"], list(self.Base.df["b"].values))

    def test_set_dtypes_coerce_changes_df(self):
        """Ensure resulting dataframe has NaN values if coerce set to True"""
        self.Base.set_dtypes(map_dict=self.map_dict, coerce=True)
        self.assertTrue(
            True in [math.isnan(val) for val in list(self.Base.df["b"])]
        )


class BaseDataSortRecordsTests(unittest.TestCase):
    """Tests to ensure ``BaseData.sort_records`` functions properly"""

    def setUp(self):
        """Set up data for tests"""
        self.colvalues_dict = {
            "a": [3, 2, 1],
            "PID": [3, 2, 1],
        }
        self.Base = BaseData(
            pd.DataFrame().from_dict(self.colvalues_dict), copy_input=False
        )

    def test_sort_values_single_column(self):
        """Ensure sort_values sorts with individual column string as input"""
        self.Base.sort_values(by="a")
        self.assertListEqual([1, 2, 3], list(self.Base.df["a"].values))
        self.assertListEqual([1, 2, 3], list(self.Base.df["PID"].values))

    def test_sort_values_multi_column(self):
        """Ensure sort_values sorts with column name list as input"""
        self.Base.sort_values(by=["PID", "a"])
        self.assertListEqual([1, 2, 3], list(self.Base.df["a"].values))
        self.assertListEqual([1, 2, 3], list(self.Base.df["PID"].values))

    def test_sort_values_log(self):
        """Ensure sort_values generates log as expected"""
        with self.assertLogs("caproj.data.base", level="INFO") as logmsg:
            self.Base.sort_values(by="PID")
            self.assertTrue(len(logmsg.output) == 3)
