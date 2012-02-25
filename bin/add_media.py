#!/usr/bin/env python

# THIS IS NOT FINISHED. IT WORKS BUT IS UGLY.
# (20120225/straup)

"""
Append the URLs for the files in media.csv to individual object JSON files.
"""

import csv
import json
import utils
import os.path

if __name__ == '__main__' :


    path = '../media.csv'
    fh = open(path, 'r')

    reader = csv.DictReader(fh)

    for row in reader:

        root = "../objects/" + utils.id2path(row['id']) + "/"
        fname = "%s.json" % row['id']

        obj_path = root + fname

        if not os.path.exists(obj_path):
            continue

        obj_fh = open(obj_path, 'r')
        obj_data = json.load(obj_fh)
        obj_fh.close()

        obj_data['thumbnail'] = 'https://d2lp2xklsr2xgg.cloudfront.net/media/350/' + row['filename']

        obj_fh = open(obj_path, 'w')
        json.dump(obj_data, obj_fh, indent=2)
        obj_fh.close()

        print obj_path
