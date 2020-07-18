"""
caproj.data.base
~~~~~~~~~~~~~~~~

This module contains the core :mod:`caproj.data` read and write functionality

**Module classes:**

.. autosummary::

   BaseData

**Module variables:**

.. autosummary::

   log

|
"""
import json
import logging
import math
import os
from typing import Any

import numpy as np
import pandas as pd

from caproj.logger import logfunc

log = logging.getLogger(__name__)
"""``logging.getLogger`` instance for module"""


class BaseData(object):
    """Manage base read/write operations for :py:mod:`caproj.data` module classes

    :cvar df: pandas.DataFrame working copy either read in from
              from file or from an existing object by using ``BaseData``
              initializing class methods :meth:`BaseData.from_file` or
              :meth:`BaseData.from_object`
    :cvar df_input: pandas.DataFrame original input copy, not operated
                    upon by any class methods, and only created if
                    ``copy_input`` parameter set to ``True`` during
                    :meth:`BaseData.from_file` or :meth:`~BaseData.from_object`
                    class creation

    **Class methods:**

    .. autosummary::

       BaseData.from_file
       BaseData.from_object
       BaseData.to_file
       BaseData.log_record_count
       BaseData.lint_colnames
       BaseData.rename_columns
       BaseData.set_dtypes
    """

    def __init__(self, df_input, copy_input):
        if copy_input:
            self.df_input = df_input.copy()  # input df persists for reference
        self.df = df_input  # all basedata changes applied to this df
        self.log = logging.getLogger(self.__class__.__name__)

        try:
            self.log_record_count()
        except Exception as error:
            self.log.exception(
                "During __init__ of {} class, unable to log record count with "
                "exception: {}".format(self.__class__.__name__, error)
            )

    @classmethod
    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def from_file(cls, filename, copy_input=False, **read_kwargs):
        """Invoke BaseData class and read csv into pandas.DataFrame

        :param filename: str filename of .csv file to be read
        :param copy_input: bool to specify whether self.df_input persists
        :param read_kwargs: optional args to pandas.DataFrame.read_csv() or
                            pandas.DataFrame.read_excel()
        :return: pandas.DataFrame and copy_input bool as class attributes
        :raise TypeError: if the ``filename`` is not a .csv filetype
        """
        _, ext = os.path.splitext(filename)
        if ext == ".csv":
            df_input = pd.read_csv(filename, **read_kwargs)
        else:
            raise TypeError("from_file reads only .csv filetypes")
        return cls(df_input, copy_input)

    @classmethod
    @logfunc(
        log=log, funcname=True, docdescr=True, argvals=False, runtime=False
    )
    def from_object(cls, input_object, copy_input=False):
        """Invoke BaseData and read dataframe from in-memory object

        Input objects can be either (a) an existing ``BaseData`` object, in
        which case the ``pandas.DataFrame`` stored within that object will be
        read, or (b) a simple ``pandas.DataFrame`` object.

        :param input_object: object to be read into ``BaseData``
        :param copy_input: bool to specify whether self.df_input persists
        :return: pandas.DataFrame and copy_input bool as class variables
        :raise Exceptions: if the ``input_object`` is neither a
                           pandas.Dataframe nor a ``BaseData`` object with an
                           existing ``BaseData.df`` attribute

        """
        if isinstance(input_object, pd.DataFrame):
            df_input = input_object.copy()
        else:
            try:
                if isinstance(input_object.df, pd.DataFrame):
                    df_input = input_object.df.copy()
            except Exception:
                log.exception(
                    "input_object must be either pandas.DataFrame or "
                    "class object with input_object.df attribute of type "
                    "pandas.DataFrame."
                )
                raise
        return cls(df_input, copy_input)

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def to_file(self, target_filename, **to_csv_kwargs):
        """Save current version of BaseData.df to file in .csv format

        :param target_filename: str filename to which csv should be written
        :param to_csv_kwargs: optional args to pandas.DataFrame.to_csv()
        """
        self.df.to_csv(target_filename, index=False, **to_csv_kwargs)

    def log_record_count(self, id_col="PID"):
        """Log number of records and unique projects in `BaseData.df`
        """
        self.log.info(
            "Number of project change records: {}".format(len(self.df))
        )
        self.log.info(
            "Number of unique projects in dataset: {}".format(
                self.df[id_col].nunique()
            )
        )

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def lint_colnames(self):
        """Normalize column name format using underscore ('_') as a separator
        """
        orig_colnames = self.df.columns
        new_colnames = [
            col.strip().replace(" ", "_").replace("-", "_")
            for col in orig_colnames
        ]
        self.df.columns = new_colnames

        # log changes to colnames
        changed_colnames = [
            (orig_col, new_col)
            for orig_col, new_col in zip(orig_colnames, new_colnames)
            if orig_col != new_col
        ]
        if len(changed_colnames) > 0:
            self.log.info(
                "Column names changed (original, new): {}".format(
                    changed_colnames
                )
            )
        else:
            self.log.info("No column names changed")

    def _read_json(self, filepath):
        """Read json file to dictionary object

        :param filepath: file path to json file
        :type filepath: str
        :return: dictionary object read from json file, if filepath exists
        :rtype: dict
        """
        if os.path.exists(filepath):
            with open(filepath, "rt") as f:
                json_dict = json.load(f)
            return json_dict
        else:
            self.log.warning(
                "JSON filepath {} does not exist. No data loaded.".format(
                    filepath
                )
            )

    def _map_dict_json(
        self, map_dict=None, json_path=None, log_text="Column names"
    ):
        """Handle and log dictionary source for higher-level methods

        [extended_summary]

        :param map_dict: [description], defaults to None
        :type map_dict: [type], optional
        :param json_path: [description], defaults to None
        :type json_path: [type], optional
        :param log_text: [description], defaults to "Column names"
        :type log_text: str, optional
        :return: [description]
        :rtype: [type]
        """
        if map_dict:
            self.log.info(
                "{} mapped using direct map_dict input option".format(
                    log_text.capitalize()
                )
            )
        elif json_path:
            map_dict = self._read_json(filepath=json_path)
            if map_dict:
                self.log.info(
                    "{} mapped using {}".format(
                        log_text.capitalize(), json_path
                    )
                )
            else:
                self.log.info(
                    "JSON failed to load map_dict, no {} changed".format(
                        log_text.lower()
                    )
                )
                return
        else:
            self.log.warning(
                "Neither a map_dict nor json_path was specified, as a result no "
                "{} were changed".format(log_text.lower())
            )
            return

        return map_dict

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def rename_columns(self, map_dict=None, json_path=None):
        """Map existing column names to new names based on input dictionary

        A simple wrapper for the pandas ``DataFrame.rename`` method

        :param map_dict: column name mapping {current_value: new_value},
                         defaults to None
        :type map_dict: dict, optional
        :param json_path: file path to json file storing the desired map_dict,
                          defaults to None
        :type json_path: str, optional
        """
        map_dict = self._map_dict_json(
            map_dict=map_dict, json_path=json_path, log_text="column names"
        )
        if not map_dict:
            return

        self.df.rename(columns=map_dict, inplace=True)

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def set_dtypes(self, map_dict=None, json_path=None, coerce=False):
        """Map and convert columns to specified data types

        Internally, this function uses the ``pandas`` ``.to_*`` data type
        conversion methods.

        Error handling logs information on values that cannot be converted.

        :param map_dict: [description], defaults to None
        :type map_dict: [type], optional
        :param json_path: [description], defaults to None
        :type json_path: [type], optional
        :param coerce: [description], defaults to False
        :type coerce: bool, optional
        """
        map_dict = self._map_dict_json(
            map_dict=map_dict, json_path=json_path, log_text="column dtypes"
        )
        if not map_dict:
            return

        if coerce:
            self.log.warning(
                "All dtype conversion error values will be deleted and left blank"
            )

        dtype_errors_dict = dict()

        for colname, dtype in map_dict.items():

            invalid_dtype = False

            if dtype in ["float", "integer", "signed", "unsigned"]:
                series_ignore = pd.to_numeric(
                    self.df[colname], downcast=dtype, errors="ignore"
                )
                series_coerce = pd.to_numeric(
                    self.df[colname], downcast=dtype, errors="coerce"
                )

            elif dtype == "datetime":
                # datetime is particularly challenging for the desired behavior
                # as a result, the dtype_errors and conversions are handled
                # in a separate function
                series_ignore, series_coerce, dict_errors = self._to_datetime(
                    colname
                )
                # series_ignore = pd.to_datetime(
                #     self.df[colname], errors="ignore"
                # )
                # series_coerce = pd.to_datetime(
                #     self.df[colname], errors="coerce"
                # )

            elif dtype == "string":
                series_ignore = self.df[colname].copy().astype("str")
                series_coerce = self.df[colname].copy().astype("str")

            else:
                invalid_dtype = True

            if not invalid_dtype:
                if dtype == "datetime":
                    dtype_errors_dict[colname] = dict_errors
                    print(series_ignore.astype(str))
                    print(series_coerce.astype(str))
                else:
                    dtype_errors_dict[colname] = series_ignore[
                        series_ignore != series_coerce
                    ].to_dict()
                self.log.info(
                    "column '{0}' dtype conversion to '{1}' encountered {2}".format(
                        colname,
                        dtype,
                        "no errors"
                        if len(dtype_errors_dict[colname]) == 0
                        else "{} errors: {}".format(
                            len(dtype_errors_dict[colname]),
                            dtype_errors_dict[colname],
                        ),
                    )
                )
                self.df[colname] = series_coerce if coerce else series_ignore
            else:
                dtype_errors_dict[
                    colname
                ] = "'{}' dtype is not a valid input".format(dtype)
                self.log.info(
                    "'{}' dtype not converted: {}".format(
                        colname, dtype_errors_dict[colname]
                    )
                )

        self.dtype_errors = dtype_errors_dict

    def _stringify_datetime_col(self):
        """Force datetime column to strings to prevent invalid number conversions"""
        # TODO:
        # 1. return stringified version of datetime column
        raise NotImplementedError

    def _to_datetime(self, colname):
        """Convert column to datetime while protecting against numeric conversions"""
        # TODO:
        # 1. Generate stringified version of column
        # 2. Coerce to_datetime for string version of col
        # 3. Create second version of to_datetime where NaT values are replaced with original pre-strigified values
        # 4. return both versions of converted as series_ignore and series_convert
        string_series = self.df[colname].copy().astype(str)
        series_coerce = pd.to_datetime(string_series, errors="coerce")
        series_ignore = series_coerce.fillna(self.df[colname].copy())
        dict_errors = series_ignore[
            string_series != series_coerce.astype(str)
        ].to_dict()
        dict_errors = {
            key: val for key, val in dict_errors.items() if not math.isnan(val)
        }
        return series_ignore, series_coerce, dict_errors

    def sort_records(self):
        raise NotImplementedError
