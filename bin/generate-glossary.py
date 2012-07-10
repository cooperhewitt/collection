#!/usr/bin/env python

import sys
import os
import os.path
import json
import types
import utils

def crawl(root) :

    glossary = {}

    for root, dirs, files in os.walk(root):

        for f in files:

            if not f.endswith(".json") :
                continue

            path = os.path.join(root, f)
            path = os.path.abspath(path)
            
            fh = open(path, 'r')
            data = json.load(fh)

            munge(glossary, data)

    return glossary

def munge(glossary, thing, prefix=None):

    if type(thing) == types.DictType:

        for k, v in thing.items():

            label = k

            if prefix:
                label = "%s.%s" % (prefix, label)

            if type(v) == types.DictType:

                add_key(glossary, label)
                munge(glossary, v, label)

            elif type(v) == types.ListType:

                add_key(glossary, label)
                munge(glossary, v, label)

            else:

                add_key(glossary, label)

    elif type(thing) == types.ListType:

        for stuff in thing:
            munge(glossary, stuff, prefix)

    else:
        pass

def add_key(glossary, key):

    if glossary.get(key, False):
        return

    glossary[key] = {
        "description": "",
        "notes": [],
        "sameas": []
        }

if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser(usage="python generate-glossary.py --options")

    parser.add_option('--objects', dest='objects',
                        help='The path to your collection objects',
                        action='store')

    parser.add_option('--glossary', dest='glossary',
                        help='The path where your new glossary file should be written',
                        action='store')

    options, args = parser.parse_args()

    #

    old_glossary = None

    if os.path.exists(options.glossary):
        fh = open(options.glossary, 'r')
        old_glossary = json.load(fh)
        fh.close()

    #

    new_glossary = crawl(options.objects)

    if old_glossary:
        new_glossary = dict(new_glossary.items() + old_glossary.items())

    #

    fh = open(options.glossary, 'w')
    json.dump(new_glossary, fh, indent=2)
    fh.close()
    
