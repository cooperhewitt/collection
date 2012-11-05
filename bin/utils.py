import json
import csv
import os
import os.path

import pprint
import string

import logging

# This does what it sounds like - it flattens directory of
# key/value JSON files in to a CSV file. If your data is more
# complicated than that you shouldn't be using this...

def jsondir2csv(datadir, outfile):

    fh = open(outfile, 'w')
    writer = None

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            if not writer:
                keys = data.keys()
                keys.sort()
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()

            try:
                writer.writerow(data)
            except Exception, e:
                logging.error(e)

    logging.info("done");

def dumper(data):
    print pprint.pformat(data)

def id2path(id):

    tmp = str(id)
    parts = []

    while len(tmp) > 3:
        parts.append(tmp[0:3])
        tmp = tmp[3:]

    if len(tmp):
        parts.append(tmp)

    return os.path.join(*parts)

def clean_meta_name(name):

    name = name.strip()
    name = name.lower()

    for p in string.punctuation:
        name = name.replace(p, '')

    name = name.replace("--", "-")
    name = name.replace("..", ".")

    return name

def utf8ify_dict(stuff):
    
    for k, v in stuff.items():

        if v:
            try:
                v = v.encode('utf8')
            except Exception, e:
                v = ''

        stuff[k] = v

    return stuff
