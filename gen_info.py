from collections import OrderedDict
from glob import glob
import json
from os import chdir, getcwd
from os.path import basename, getsize, isfile, join, normpath
from sys import argv, stderr
from urllib.request import urlretrieve


URL = 'http://butler.fri.uni-lj.si/datasets'


start_dir = getcwd()
info = []
for root in argv[1:]:
    chdir(join(start_dir, root))
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
                    d['url'] = '{}/{}/{}'.format(URL, normpath(root), filename)
                    d['size'] = getsize(filename)
                    changed = True
                except:
                    print('failed to get file', filename, location, file=stderr)
        if changed:
            with open(infof, 'w') as f:
                json.dump(d, f, indent=4)
        info.append([[root, filename], d])

info.sort()
print(json.dumps(info, indent=4))
