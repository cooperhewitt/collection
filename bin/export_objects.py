#!/usr/bin/env python

# I think there might still be some weirdness in the UTF-8 wrangling
# (20120225/straup)

"""
Export the contents of objects.csv in to individual JSON files.
"""

import sys
import json
import csv
import utils
import os
import os.path

class UnicodeCsvReader(object):
    def __init__(self, f, encoding="utf-8", **kwargs):
        self.csv_reader = csv.reader(f, **kwargs)
        self.encoding = encoding

    def __iter__(self):
        return self

    def next(self):
        # read and split the csv row into fields
        row = self.csv_reader.next() 
        # now decode

        try:
            return [unicode(cell, self.encoding) for cell in row]
        except Exception, e:
            return []

    @property
    def line_num(self):
        return self.csv_reader.line_num

class UnicodeDictReader(csv.DictReader):
    def __init__(self, f, encoding="utf-8", fieldnames=None, **kwds):
        csv.DictReader.__init__(self, f, fieldnames=fieldnames, **kwds)
        self.reader = UnicodeCsvReader(f, encoding=encoding, **kwds)


if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])
    bindir = os.path.dirname(whoami)
    collection = os.path.dirname(bindir)

    objects = os.path.join(collection, 'objects')

    obj_csv = os.path.join(collection, 'objects.csv')
    obj_fh = open(obj_csv, 'r')

    reader = UnicodeDictReader(obj_fh)

    for row in reader:

        fname = "%s.json" % row['id']

        root = utils.id2path(row['id'])
        root = os.path.join(objects, root)

        out = os.path.join(root, fname)
        print out
        continue

        if not os.path.exists(root):
            os.makedirs(root)

        out_fh = open(out, 'w')
        json.dump(row, out_fh, indent=2)

        print out
