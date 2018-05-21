"""
Provides various utils:
csvwriter for provided filename and fields.
"""
import csv

def get_csv_writer(filename, fields):
    """Returns a csv writer with header."""
    w = csv.DictWriter(open(filename, "w"), fields)
    w.writeheader()
    return w