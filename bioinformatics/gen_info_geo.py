import json

from collections import OrderedDict
from glob import glob
from os import chdir, getcwd
from os.path import basename, getsize, isfile, join, normpath
from sys import argv, stderr
from urllib.request import urlretrieve


# set the base url without trailing slash!
URL = 'http://datasets.orange.biolab.si/bioinformatics/geo'


start_dir = getcwd()
info = []

chdir(start_dir)
for infof in glob('**/*.info', recursive=True):
    changed = False
    with open(infof, 'r') as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
        filename = infof[:-5]
        location = d.get('url', '')
        if location and (not location.startswith(URL) or
                            basename(location) != basename(filename)):
            try:
                urlretrieve(location, filename)
                d['url'] = '{}/{}/{}'.format(URL, filename)
                d['size'] = getsize(filename)
                changed = True
            except:
                print('failed to get file', filename, location, file=stderr)
        ref = d.get('references', None)
        if isinstance(ref, str):
            d['references'] = [ref]
            changed = True
    if changed:
        with open(infof, 'w') as f:
            json.dump(d, f, indent=4)
    file_path = [filename]
    info.append([file_path, d])

info.sort()
print(json.dumps(info, indent=4))