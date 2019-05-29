import os
import sys
import subprocess as sp
import importlib.util as imp
from defs import *
import shutil

ignoreDirs = {'node_modules', '__pycache__'}

def main():
    Builder(os.getcwd())

class Builder:
    def __init__(self,root):
        self.root = root
        # self.buildDir = os.path.abspath(os.path.join(root,os.pardir,'site'))
        self.buildDir = os.path.join(root,'site')
        self.srcDir = os.path.join(root,'src')
        self.recDir = os.path.join(root,'rec')
        self.copyResources()
        self.buildFiles()
    def buildFiles(self):
        global resourceDepth
        for root, dirs, files in os.walk(self.srcDir):
            dirs[:] = [d for d in dirs if d not in ignoreDirs]
            relPath = root[len(self.srcDir)+1:]
            resourceDepth = getDirDepth(relPath)
            for f in files:
                F = File(root,relPath,f)
                if F.type != 'ppy': continue
                fPath = os.path.join(self.buildDir,relPath,f'{F.name}.html')
                F.gen(fPath)
    def copyResources(self):
        try: shutil.rmtree(self.buildDir)
        except: pass
        shutil.copytree(self.recDir, self.buildDir)

def cleanStr(txt):
    txt = txt.replace('\r\n','\n')
    if txt[0] == '\n':
        i = 1
        while txt[i] == ' ' or txt[i] == '\t': i+=1
        txt = txt.replace(txt[1:i],'')
    return txt

def getDirDepth(relPath):
    res = 0
    while relPath != '':
        relPath, _ = os.path.split(relPath)
        res+=1
    return res

class File:
    def __init__(self,root,relPath,name):
        self.root = root
        self.relPath = relPath
        self.name = name
        self.path = os.path.join(root,name)
        dotI = name.find('.')
        if dotI == -1: self.type = ''
        else:
            self.type = name[dotI+1:]
            self.name = name[:dotI]
    def gen(self, fPath):
        print(f'building {os.path.join(self.relPath,self.name)}.html')
        dirPath = os.path.dirname(self.path)
        cwd = os.getcwd()
        os.chdir(dirPath)
        with open(self.path,'r') as f:
            ldict = {}
            exec(f.read(),globals(),ldict)
            p = ldict['p']
        os.chdir(cwd)
        os.makedirs(os.path.dirname(fPath), exist_ok=True)
        with open(fPath,'w') as f: f.write(str(p))

resourceDepth = None
def resource(name):
    return '../'*resourceDepth + name
def getBasePath(): return '../'*resourceDepth

main()