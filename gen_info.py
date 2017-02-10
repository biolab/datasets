from glob import glob
import json
import os.path
from sys import argv


start_dir = os.getcwd()
info = []
for root in argv[1:]:
    os.chdir(os.path.join(start_dir, root))
    for infof in glob('**/*.info', recursive=True):
        with open(infof, 'r') as f:
            d = json.load(f)
        info.append([[root, infof[:-5]], d])

info.sort()
print(json.dumps(info))
