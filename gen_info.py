from collections import OrderedDict
from glob import glob
import json
from os import chdir, getcwd
from os.path import getsize, isfile, join, normpath
from sys import argv, stderr
from urllib.request import urlretrieve


start_dir = getcwd()
info = []
for root in argv[1:]:
    chdir(join(start_dir, root))
    for infof in glob('**/*.info', recursive=True):
        changed = False
        with open(infof, 'r') as f:
            d = json.load(f, object_pairs_hook=OrderedDict)
            filename = infof[:-5]
            location = d.get('file', '')
            if not isfile(filename) and location:
                try:
                    urlretrieve(location, filename)
                    d['file'] = 'http://butler.fri.uni-lj.si/datasets/{}/{}'.format(normpath(root), filename)
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
