import os
import subprocess as sp

ignoreDirs = {'node_modules', '__pycache__'}

def main():
    Builder(os.getcwd())

class Builder:
    def __init__(self,root):
        self.root = root
        self.buildDir = os.path.abspath(os.path.join(root,os.pardir))
        self.setFiles()
    def setFiles(self):
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in ignoreDirs]
            relPath = root[len(self.root)+1:]
            for f in files:
                F = File(root,relPath,f)
                if F.type != 'ppy': continue
                fPath = os.path.join(self.buildDir,relPath,f)
                print(self.buildDir)
                print(relPath)
                print(f)
                F.gen(fPath)

def cleanStr(txt):
    txt = txt.replace('\r\n','\n')
    if txt[0] == '\n':
        i = 1
        while txt[i] == ' ' or txt[i] == '\t': i+=1
        txt = txt.replace(txt[1:i],'')
    return txt

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
        print(f'genning {fPath}')
        # with open(fPath,'w') as f:f.write(self.text)

main()