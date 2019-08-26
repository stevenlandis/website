import re
import os

linkRe = re.compile(r'from (src.*) import|import (src.*)')
emptyRe = re.compile(r'^\s$')

def getLinks(file):
    links = []
    for line in file.lines:
        match = linkRe.match(line)
        if match == None:
            if emptyRe.match(line):
                break
            continue
        imp = match.group(1)
        path = os.path.join(*imp.split('.'))
        links.append(path)
    return links