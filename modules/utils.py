"""
Provides various utils:
csvwriter for provided filename and fields.
"""
import csv


def get_csv_writer(filename, fields):
    """Returns a csv DictWriter with provided filename and header already write with provided fields."""
    w = csv.DictWriter(open(filename, "w"), fields)
    w.writeheader()
    return w
