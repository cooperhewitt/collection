#!/usr/bin/env python

import sys
import os.path
import logging

import utils

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    datadir = os.path.join(rootdir, 'roles')
    metadir = os.path.join(rootdir, 'meta')

    outfile = os.path.join(metadir, 'roles.csv')

    utils.jsondir2csv(datadir, outfile)
