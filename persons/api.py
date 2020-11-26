import pandas as pd
from fnmatch import fnmatch
from collections import namedtuple
import os.path
import uuid


Record = namedtuple('Record', ['name','address','phone'])

def open_buffer(df, filepath):
    with open(filepath, 'w+') as f:
        df.to_csv(f)

class Records(object):
    """An object to store, filter and export records.
    The supported load and save types can be queried by acessing the
    _load_types and _save_types attributes.
    """    
    _load_types = {
        '.csv' : pd.read_csv
    }

    _save_types = {
        '.json': pd.DataFrame.to_json,
        '.csv' : pd.DataFrame.to_csv,
        '.xlsl': pd.DataFrame.to_excel,
        '.html': pd.DataFrame.to_html
    }

    def __init__(self, records=[]):
        self.records = pd.DataFrame(columns = Record._fields)
        for record in records:
            self.add_record(record)

    def __iter__(self):
        for record in self.records.values:
            yield Record(*record)
    
    @classmethod
    def from_file(cls, filepath = None):
        """Generates a Records object from a file

        Args:
            filepath (str, optional): path to a file (only csv currently supported). Defaults to None.

        Raises:
            ValueError: if the file is not csv

        Returns:
            Records: A records object with the contents of the file
        """        
        _, ext = os.path.splitext(filepath)

        if ext not in cls._save_types:
            raise ValueError('Loading from {} is not yet supported'.format(ext))

        with open(filepath, 'r') as f:
            records_df = cls._load_types[ext](f, index_col=0)

        inst = cls()
        inst.records = records_df
        return inst


    def export(self, filepath):
        """Saves this set of records as a file

        Args:
            filepath (str): the path to a file to save, the format is automatically detected from the extension

        Raises:
            ValueError: If the format is not supported
        """        
        _, ext = os.path.splitext(filepath)

        if ext not in self._save_types:
            raise ValueError('Export to {} is not yet supported'.format(ext))

        with open(filepath, 'w+') as f:
            self._save_types[ext](self.records, f)


    def add_record(self, record):
        """Adds a new record, generating a uid

        Args:
            record (Record or seq): A record object or any sequence with name, address, phone
        """        
        self.records.loc[uuid.uuid4()] = record


    def update_record(self, uid, record):
        """Updates a record with new information

        Args:
            uid ([type]): [description]
            record (Record): The new information

        Raises:
            KeyError: if the uid is not found
        """
        if uid not in self.records:
            raise KeyError('Uid {} not found'.format(uid))

        self.records.loc[uid] = record


    def delete_record(self, uid):
        """Deletes an existing record

        Args:
            uid ([type]): The uid of the record to be deleted
        """        
        self.records.drop(uid)


    def display(self):
        """Prints the entire set of records
        """        
        print(self.records.to_string())
        

    def filter_records(self, name=None, address=None, phone=None):
        """Returns a new Records object with Records that match all patterns

        Args:
            name (str, optional): a glob-like pattern to match with names. Defaults to None.
            address (str, optional): a glob-like pattern to match addresses. Defaults to None.
            phone (str, optional): a glob-like pattern to match phone numbers. Defaults to None.
        """        
        def filt(attrs):
            return all(
                pat is None or fnmatch(str(attr),pat) 
                for attr, pat 
                in zip(attrs, (name, address, phone))
            )

        new_records = Records()
        new_records.records = self.records[self.records.apply(filt, axis=1)]

        return new_records