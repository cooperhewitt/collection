import pprint
import os.path
import string
import unicodedata

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

def clean_meta_name(name, allow_punctuation=[]):

    name = name.strip()
    name = name.lower()
    
    name = remove_accents(name)

    for c in string.punctuation:

        if c in allow_punctuation:
            continue

        name = name.replace(c, "")

    name = name.replace(" ", "-")
    name = name.replace("--", "-")
        
    return name

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii
