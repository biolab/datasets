from collections import OrderedDict
from glob import glob
import json
from os import chdir, getcwd
from os.path import basename, splitext
from sys import argv, stderr
from urllib.request import urlretrieve, urlopen


for infof in glob('**/*.info', recursive=True):
    print(infof)
    with open(infof, 'r') as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
        filename = splitext(basename(infof)[:-5])[0]
        assert filename == d['name']
        location = d['file']
        remotefile = urlopen(location)
        for key in ('name', 'description', 'instances', 'variables', 'version'):
            assert key in d
