""" persons is a module for keeping records of people,
and consists of two classes

Record - a namedtuple expecting (name, address, phone)
Records - a class that stores Records, and supports iteration, loading saving and filtering records

dependencies - pandas, openpyxl (if exporting to .xlsl is desired)

"""
from .api import Records, Record
