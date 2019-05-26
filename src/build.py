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
            relPath = root[len(self.root):]
            for f in files:
                F = File(root,relPath,f)
                if F.type != 'html': continue
                fPath = os.path.join(self.buildDir,relPath,f)
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
        else: self.type = name[dotI+1:]
    def gen(self, fPath):
        with open(self.path,'r') as f: self.text = f.read()
        startPat = '<gen>'
        endPat = '</gen>'
        startI = 0
        while True:
            startI = self.text.find(startPat, startI)
            if startI == -1: break
            endI = self.text.find(endPat, startI)
            if endI == -1: raise 1
            genTxt = self.text[startI+len(startPat):endI]
            exeTxt = 'from defs import *\n' + cleanStr(genTxt)
            with open('temp.py','w') as f: f.write(exeTxt)
            proc = sp.Popen(['python','temp.py'],stdout=sp.PIPE)
            res = proc.communicate()[0].decode('utf-8')
            if proc.returncode != 0: break
            res = res.replace('\r\n','\n')
            if res[-1] == '\n': res = res[:-1]
            os.remove('temp.py')
            self.text = self.text[:startI] + res + self.text[endI+len(endPat):]
            startI = endI+len(res)-len(genTxt)-len(startPat)
        with open(fPath,'w') as f:f.write(self.text)

main()