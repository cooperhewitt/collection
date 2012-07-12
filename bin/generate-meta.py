#!/usr/bin/env python

import sys
import os
import os.path
import json
import utils

import logging

object_root = sys.argv[1]

def update_bucket(options, bucket, object_path):

    # sudo put me in utils.py

    bucket = utils.clean_meta_name(bucket)

    object_root = os.path.abspath(options.objects)
    object_path = os.path.abspath(object_path)

    object_path = object_path.replace(object_root + "/", "")
    
    bucket_name = "%s.txt" % bucket
    bucket_path = os.path.join(options.meta, bucket_name)

    logging.debug("%s %s" % (bucket, object_path))

    fh = open(bucket_path, "a")
    fh.write(object_path + "\n")
    fh.close()

def generate_meta(options):

    categories = (
        'culture',
        'dynasty',
        'movement',
        'period',
        'region',
        'school',
        'style'
        )

    index = {}

    for category in categories:
        index[category] = {}

    for root, dirs, files in os.walk(options.objects):

        for f in files:

            if not f.endswith(".json") :
                continue
            
            path = os.path.join(root, f)
            path = os.path.abspath(path)

            logging.debug("generate meta for %s" % path)

            fh = open(path, 'r')
            data = json.load(fh)

            for category in categories:

                if data.get(category, False):

                    subject = data[category]
                    bucket = "%s.%s" % (category, subject)

                    # update_bucket(options, bucket, path)

                    bucket_name = utils.clean_meta_name(bucket) + ".txt"
                    bucket_path = os.path.join(options.meta, bucket_name)

                    index[category][subject] = bucket_path

    if options.index:

        fh = open(options.index, 'w')
        json.dump(index, fh, indent=2)
        fh.close()

        logging.info("created meta data index at %s" % options.index)


if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser(usage="python generate-meta.py --options")

    parser.add_option('--objects', dest='objects',
                        help='The path to your collection objects (folder)',
                        action='store')

    parser.add_option('--meta', dest='meta',
                        help='The path to your meta data (folder)',
                        action='store', default=None)

    parser.add_option('--index', dest='index',
                        help='The path to create an index of the meta files',
                        action='store', default=None)

    parser.add_option('--debug', dest='debug',
                        help='Enable debug logging',
                        action='store_true', default=False)

    options, args = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


    generate_meta(options)
    logging.info("done");

    sys.exit()
