from collections import OrderedDict
from glob import glob
import json
from os.path import basename, splitext
import re
import ssl
from sys import exit
from urllib.request import urlopen, Request


MANDATORY = ('name', 'description', 'version',
             'instances', 'variables', 'target')
RE_UNQUOTED_HREF = """<a href=[^'"]"""
RE_HREF_URL = """<a href=(.*?)>"""

# ssl context to ignore (self-signed) certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


ret = 0
print('Testing:')
for infof in sorted(glob('**/*.info', recursive=True)):
    print(infof, end=' ... ')
    with open(infof, 'r') as f:
        d = json.load(f, object_pairs_hook=OrderedDict)
        filename = basename(infof)[:-5]
        assert (d['name'] and filename.startswith(d['name'])), \
                'Name field does not match the filename'
        location = d['url']
        try:
            req = Request(location, headers={'User-Agent': "Mozilla/5.0 Firefox"})
            remotefile = urlopen(req)
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
                url = link.strip('\'"')
                try:
                    urlopen(url, timeout=10)
                except:
                    try:
                        req = Request(url, headers={'User-Agent': "Mozilla/5.0 Firefox"})
                        con = urlopen(req, context=ctx)
                    except:
                        print('\n X Inaccessible link:', link)
                        ret = 1
    print('OK')

exit(ret)
