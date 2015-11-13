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

    datadir = os.path.join(rootdir, 'objects')
    metadir = os.path.join(rootdir, 'meta')

    outfile_objects = os.path.join(metadir, 'objects.csv')
    outfile_images = os.path.join(metadir, 'objects-images.csv')
    outfile_participants = os.path.join(metadir, 'objects-participants.csv')
    outfile_exhibitions = os.path.join(metadir, 'objects-exhibitions.csv')

    fh_objects = open(outfile_objects, 'w')
    fh_images = open(outfile_images, 'w')
    fh_participants = open(outfile_participants, 'w')
    fh_exhibitions = open(outfile_exhibitions, 'w')

    writer_objects = None
    writer_images = None
    writer_participants = None
    writer_exhibitions = None

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            images = data.get('images', [])
            primary_image = None

            if len(images):

                for img in images:

                    # huh? why...

                    if type(img) != types.DictType:
                        continue

                    for sz, details in img.items():

                        if sz != 'z':
                            continue

                        if int(details['is_primary']) != 1:
                            continue

                        primary_image = details['url']
                        break
                    
                    if primary_image:
                        break

            data['primary_image'] = primary_image

            participants = data.get('participants', [])
            exhibitions = data.get('exhibitions', [])

            #

            for prop in ('images', 'colors', 'participants', 'exhibitions'):
                if data.has_key(prop):
                    del(data[prop])

            #

            if not writer_objects:
                keys = data.keys()

                keys.extend(['primary_image','is_active','woe:country_name'])

                keys.sort()
                writer_objects = csv.DictWriter(fh_objects, fieldnames=keys)
                writer_objects.writeheader()

            try:
                data = utils.utf8ify_dict(data)
                writer_objects.writerow(data)
            except Exception, e:
                import pprint
                print pprint.pformat(data)
                raise Exception, e

            #

            if not writer_images:
                writer_images = csv.DictWriter(fh_images, fieldnames=('object_id', 'size', 'url', 'width', 'height', 'is_primary', 'image_id'))
                writer_images.writeheader()

            for i in images:

                if not type(i) == types.DictType:
                    continue


                for sz, details in i.items():

                    details['size'] = sz
                    details['object_id'] = data['id']
                    writer_images.writerow(details);

            #

            if not writer_participants:
                writer_participants = csv.DictWriter(fh_participants, fieldnames=('object_id', 'person_id', 'person_name', 'person_url', 'role_id', 'role_name', 'role_url', 'person_date', 'role_display_name'))
                writer_participants.writeheader()

            for details in participants:
                details['object_id'] = data['id']
                details = utils.utf8ify_dict(details)
                writer_participants.writerow(details)

            #

            if not writer_exhibitions:
                writer_exhibitions = csv.DictWriter(fh_exhibitions, fieldnames=('object_id', 'id', 'title', 'date_start', 'date_end'))
                writer_exhibitions.writeheader()

            for details in exhibitions:
                details['object_id'] = data['id']
                del(details['url'])
                details = utils.utf8ify_dict(details)
                writer_exhibitions.writerow(details)

    logging.info("done");
            
