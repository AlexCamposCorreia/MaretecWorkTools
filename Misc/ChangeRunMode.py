#!/bin/python
import sys
import os
import shutil
from pprint import pprint

main_dir = sys.argv[1]
mode_dir = sys.argv[2]

dirs = []
for a,b,c in os.walk(main_dir):
    if a.endswith('data'):
        dirs.append(a)

for d in dirs:
    try:
        files = list(os.walk(os.path.join(d,mode_dir)))[0][2]
        for f in files:
            print(os.path.join(d,mode_dir,f))
            print(os.path.join(d,f))
            shutil.copy2(os.path.join(d,mode_dir,f), os.path.join(d,f))
    except IndexError:
        continue
