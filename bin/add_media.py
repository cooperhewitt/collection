#!/usr/bin/env python

"""
Append the URLs for the files in media.csv to individual object JSON files.
"""

import sys
import csv
import json
import utils
import os.path

if __name__ == '__main__' :

    whoami = os.path.abspath(sys.argv[0])
    bindir = os.path.dirname(whoami)
    collection = os.path.dirname(bindir)

    objects = os.path.join(collection, 'objects')

    media_csv = os.path.join(collection, 'media.csv')
    media_fh = open(media_csv, 'r')

    reader = csv.DictReader(media_fh)

    for row in reader:
        
        fname = "%s.json" % row['id']

        root = utils.id2path(row['id'])
        root = os.path.join(objects, root)

        obj_path = os.path.join(root, fname)

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
