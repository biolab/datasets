from collections import OrderedDict
from glob import glob
import json
from os.path import basename, splitext
import re
from sys import exit
from urllib.request import urlopen


MANDATORY = ('name', 'description', 'version',
             'instances', 'variables', 'target')
RE_HREF = """<a href=[^'"]"""

ret = 0
print('Testing:')
for infof in glob('**/*.info', recursive=True):
    print(infof, end=' ... ')
    with open(infof, 'r') as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
        filename = splitext(basename(infof)[:-5])[0]
        assert filename == d['name'], 'Name field does not match the filename'
        location = d['url']
        try:
            remotefile = urlopen(location)
        except:
            print('Cannot open remote file')
            ret = 1
        for key in MANDATORY:
            assert key in d, 'Missing field: {}'.format(key)
        for value in d.values():
            if isinstance(value, str):
                assert re.search(RE_HREF, value) is None, 'Unquoted link'
    print('OK')

exit(ret)
