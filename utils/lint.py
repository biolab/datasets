from collections import OrderedDict
from glob import glob
import json
from os.path import basename, splitext
import re
from sys import exit
from urllib.request import urlopen


MANDATORY = ('name', 'description', 'version',
             'instances', 'variables', 'target')
RE_UNQUOTED_HREF = """<a href=[^'"]"""
RE_HREF_URL = """<a href=(.*?)>"""

ret = 0
print('Testing:')
for infof in sorted(glob('**/*.info', recursive=True)):
    print(infof, end=' ... ')
    with open(infof, 'r') as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
        filename = splitext(basename(infof)[:-5])[0]
        assert filename == d['name'], 'Name field does not match the filename'
        location = d['url']
        try:
            remotefile = urlopen(location)
        except:
            print('\n X Cannot open remote file')
            ret = 1
        for key in MANDATORY:
            assert key in d, 'Missing field: {}'.format(key)
        for value in d.values():
            if not isinstance(value, str):
                continue
            assert re.search(RE_UNQUOTED_HREF, value) is None, 'Unquoted link'
            links = re.findall(RE_HREF_URL, value)
            for link in links:
                try:
                    urlopen(link.strip('\'"'), timeout=10)
                except:
                    print('\n X Inaccessible link:', link)
                    ret = 1
    print('OK')

exit(ret)
