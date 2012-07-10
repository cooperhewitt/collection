#!/usr/bin/env python

import sys
import json

if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser(usage="python generate-glossary.py --options")

    parser.add_option('--glossary', dest='glossary',
                        help='The path where your new glossary file should be written',
                        action='store')

    parser.add_option('--markdown', dest='markdown',
                        help='The path to your collection objects',
                        action='store', default=None)

    options, args = parser.parse_args()

    fh = open(options.glossary, 'r')
    glossary = json.load(fh)
    fh.close()

    keys = glossary.keys()
    keys.sort()

    if options.markdown:
        fh = open(options.markdown, 'w')
    else:
        fh = sys.stdout

    fh.write("_This file was generated programmatically using the `%s` document._\n" % options.glossary)
    fh.write("\n")

    for k in keys:

        details = glossary[k]

        fh.write("%s\n" % k)
        fh.write("==\n")
        fh.write("\n")

        if details['description'] != '':
            fh.write("_%s_\n" % details['description'])
            fh.write("\n")

        if len(details['notes']):

            fh.write("notes\n")
            fh.write("--\n")
        
            for n in details['notes']:
                fh.write("* %s\n" % n)
                fh.write("\n")

        if len(details['sameas']):

            fh.write("same as\n")
            fh.write("--\n")
        
            for other in details['sameas']:
                fh.write("* %s\n" % other)
                fh.write("\n")

    if options.markdown:
        fh.close()

    sys.exit()
