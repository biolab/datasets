from glob import glob
import json

info = []
for infof in glob('*.info'):
    print(infof)
    with open(infof, 'r') as f:
        d = json.load(f)
        #d = eval(f.read())
        print(d)
    info.append([['.', infof[:-5]], d])

with open('__INFO__', 'w') as out:
    json.dump(info, out)
