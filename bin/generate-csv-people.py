#!/usr/bin/env python

import sys
import json
import csv
import os
import os.path
import types

import utils

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    datadir = os.path.join(rootdir, 'people')
    metadir = os.path.join(rootdir, 'meta')

    outfile_people = os.path.join(metadir, 'people.csv')
    outfile_roles = os.path.join(metadir, 'people_roles.csv')

    fh_people = open(outfile_people, 'w')
    fh_roles = open(outfile_roles, 'w')

    writer_people = None
    writer_roles = None

    concordances = []

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            if type(data.get('concordances', None)) == types.DictType:

                for k, v in data['concordances'].items():

                    if k not in concordances:
                        concordances.append(k)

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            if type(data.get('concordances', None)) == types.DictType:

                for k, v in data['concordances'].items():
                    data[k] = v
            
                del(data['concordances'])

            #

            roles = data.get('roles', [])

            if data.get('roles', False):
                del(data['roles'])

            #

            if not writer_people:

                keys = data.keys()

                for c in concordances:
                    if c not in keys:
                        keys.append(c)

                keys.sort()

                writer_people = csv.DictWriter(fh_people, fieldnames=keys)
                writer_people.writeheader()

            data = utils.utf8ify_dict(data)
            writer_people.writerow(data)

            #

            if not writer_roles:
                writer_roles = csv.DictWriter(fh_roles, fieldnames=('person_id', 'person_name', 'id', 'name', 'count_objects'))
                writer_roles.writeheader()

            for details in roles:
                details['person_id'] = data['id']
                details['person_name'] = data['name']

                details = utils.utf8ify_dict(details)
                writer_roles.writerow(details)

    logging.info("done");
            
