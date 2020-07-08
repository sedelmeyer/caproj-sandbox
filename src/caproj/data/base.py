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
import os

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
    :cvar input_df: pandas.DataFrame original input copy, not operated
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
    """

    def __init__(self, input_df, copy_input):
        if copy_input:
            self.input_df = input_df.copy()  # input df persists for reference
        self.df = input_df  # all basedata changes applied to this df
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
        :param copy_input: bool to specify whether self.input_df persists
        :param read_kwargs: optional args to pandas.DataFrame.read_csv() or
                            pandas.DataFrame.read_excel()
        :return: pandas.DataFrame and copy_input bool as class attributes
        :raise TypeError: if the ``filename`` is not a .csv filetype
        """
        _, ext = os.path.splitext(filename)
        if ext == ".csv":
            input_df = pd.read_csv(filename, **read_kwargs)
        else:
            raise TypeError("from_file reads only .csv filetypes")
        return cls(input_df, copy_input)

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
        :param copy_input: bool to specify whether self.input_df persists
        :return: pandas.DataFrame and copy_input bool as class variables
        :raise Exceptions: if the ``input_object`` is neither a
                           pandas.Dataframe nor a ``BaseData`` object with an
                           existing ``BaseData.df`` attribute

        """
        if isinstance(input_object, pd.DataFrame):
            input_df = input_object.copy()
        else:
            try:
                if isinstance(input_object.df, pd.DataFrame):
                    input_df = input_object.df.copy()
            except Exception:
                log.exception(
                    "input_object must be either pandas.DataFrame or "
                    "class object with input_object.df attribute of type "
                    "pandas.DataFrame."
                )
                raise
        return cls(input_df, copy_input)

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

    @logfunc(log=log, funcname=True, docdescr=True, argvals=True, runtime=False)
    def rename_columns(self, map_dict=None, json_path=None):
        """Map existing column names to new names based on input dictionary

        A simple wrapper for the pandas ``DataFrame.rename`` method

        :param map_dict: column name mapping {current_value: new_value}
        """
        if map_dict:
            self.log.info(
                "Column names mapped using direct map_dict input option"
            )
        elif json_path:
            map_dict = self._read_json(filepath=json_path)
            if map_dict:
                self.log.info("Column names mapped using {}".format(json_path))
            else:
                self.log.info(
                    "JSON failed to load map_dict, no column names changed"
                )
                return
        else:
            self.log.warning(
                "Neither a map_dict nor json_path was specified, as a result no"
                "column names were changed"
            )
            return

        self.df.rename(columns=map_dict, inplace=True)

    def set_dtypes(self):
        raise NotImplementedError

    def sort_records(self):
        raise NotImplementedError
