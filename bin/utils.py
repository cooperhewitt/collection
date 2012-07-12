import os.path
import pprint

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

    # sudo make me better

    name = name.strip()
    name = name.replace(" ", "-")
    name = name.replace("?", "")
    name = name.replace("&", "")
    name = name.replace(":", "")
    name = name.replace("/", "-")
    name = name.replace(",", "-")
    name = name.replace("'", "-")
    name = name.replace("(", "-")
    name = name.replace(")", "")
    name = name.replace("`", "")
    name = name.replace("--", "-")
    name = name.replace("..", ".")
    name = name.lower()

    return name
