#!/usr/bin/env python

# THIS IS NOT FINISHED. IT WORKS BUT IS UGLY.
# (20120225/straup)

"""
Export the contents of objects.csv in to individual JSON files.
"""

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

    path = '../objects.csv'
    fh = open(path, 'r')

    r = UnicodeDictReader(fh)

    for row in r:

        root = "../objects/" + utils.id2path(row['id']) + "/"
        fname = "%s.json" % row['id']

        out = root + fname

        if not os.path.exists(root):
            os.makedirs(root)

        out_fh = open(out, 'w')
        json.dump(row, out_fh, indent=2)

        
        print out
