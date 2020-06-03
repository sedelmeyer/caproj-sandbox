import os

import pandas as pd


class BaseData(object):
    """
    Manage base read/write operations and instantiates
    ``self.df`` for child classes across ``data`` submodule classes
    """

    def __init__(self, input_df, copy_input):
        if copy_input:
            self.input_df = input_df.copy()  # input df persists for reference
        self.df = input_df  # all basedata changes applied to this df

    @classmethod
    def from_file(cls, filename, copy_input=False, **read_kwargs):
        """Invoke ``BaseData`` and read csv or excel into pandas.DataFrame

        :param filename: str filename of .csv, .xls, or .xlsx file to be read
        :param copy_input: bool to specify whether self.input_df persists
        :param read_kwargs: optional args to pandas.DataFrame.read_csv() or
                            pandas.DataFrame.read_excel()
        :return: pandas.DataFrame and copy_input bool as class variables
        """
        _, ext = os.path.splitext(filename)
        if ext == '.csv':
            input_df = pd.read_csv(filename, **read_kwargs)
        elif ext in ('.xls', '.xlsx'):
            input_df = pd.read_excel(filename, **read_kwargs)
        else:
            raise TypeError(
                'from_file reads only .csv, .xls, or .xlsx filetypes'
            )
        return cls(input_df, copy_input)

    @classmethod
    def from_object(cls, input_object, copy_input=False):
        """Invoke ``BaseData`` and read dataframe from in-memory object

        Input objects can be either (a) an existing ``BaseData`` object, in
        which case the ``pandas.DataFrame`` stored within that object will be
        read, or (b) a simple ``pandas.DataFrame`` object.

        :param input_object: object to be read into ``BaseData``
        :param copy_input: bool to specify whether self.input_df persists
        :return: pandas.DataFrame and copy_input bool as class variables
        """
        if isinstance(input_object, pd.DataFrame):
            input_df = input_object.copy()
        else:
            try:
                if isinstance(input_object.df, pd.DataFrame):
                    input_df = input_object.df.copy()
                    # TODO implement self.log = input_object.log.copy()
            except:
                raise TypeError(
                    'input_object must be either pandas.DataFrame or '
                    'class object with input_object.df attribute of type '
                    'pandas.DataFrame.'
                )
        return cls(input_df, copy_input)

    def to_file(self, target_filename, **to_csv_kwargs):
        """Save current version of ``self.df`` to file in .csv format

        :param target_filename: str filename to which csv should be written
        :param to_csv_kwargs: optional args to pandas.DataFrame.to_csv()
        """
        # TODO: to_file saves will need trigger log file in future versions
        self.df.to_csv(target_filename, index=False, **to_csv_kwargs)
