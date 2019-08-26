import bld
import os
from src.parts.MarkdownPage import MarkdownPage
from src.parts.getLinks import getLinks
from src.getDragonPics import getDragonPics

def getResDir():
    resources = set()
    pageDir = bld.DiskDir('src/pages')
    resDir = bld.VirDir('website')

    buildDir = resDir.getDir('build')
    for inFile in pageDir.files:
        if inFile.name.startswith('__'):
            continue
        elif inFile.type == 'py':
            path = f'src/pages/{inFile.name}'
            outFile = buildDir.getFile(f'{inFile.title}.html')
            HTMLRule(inFile, outFile, '.')
        elif inFile.type == 'md':
            path = f'src/pages/{inFile.name}'
            outFile = buildDir.getFile(f'{inFile.title}.html')
            MarkdownRule(inFile, outFile, '.')

    # linkDir = resDir.getDir('links')
    # getLinksDir(bld.DiskDir('src'), resDir.getDir('links'))

    getDragonPics(resDir.getDir('build/rec'))

    # copy resoruce files
    bld.copyDir(bld.DiskDir('rec'), buildDir.getDir('rec'))

    # CNAME
    bld.CopyRule(bld.DiskFile('rec/CNAME'), buildDir.getFile('CNAME'))

    # copy scripts
    bld.copyDir(bld.DiskDir('src/scripts'), buildDir.getDir('scripts'))

    return resDir

def getLinksDir(inDir, outDir):
    for file in inDir.files:
        if file.type != 'py': continue
        LinkRule(file, outDir.getFile(f'{file.title}.link'))
    for d in inDir.dirs:
        getLinksDir(d, outDir.getDir(d.name))

def main():
    resDir = getResDir()
    resDir.build('..')

def force():
    resDir = getResDir()
    resDir.rebuild('..')

def clean():
    os.popen('rm -rf build')
    os.popen('rm -rf links')

def test():
    testDir = bld.DiskDir('src')
    for file in testDir.allFiles:
        print(file.path)

class HTMLRule(bld.Rule):
    def __init__(self, inFile, outFile, basePath):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
        self.basePath = basePath
    def run(self):
        print(f'making {self.outputs[0].name}')
        txt = self.inputs[0].read()

        tempGlobals = {}
        exec(txt, tempGlobals)

        if 'build' not in tempGlobals:
            raise Exception(f'{self.inputs[0].name} needs a function build()')

        resTxt = tempGlobals['build'](self)

        self.outputs[0].write(resTxt)

    def getRec(self, path):
        return f'{self.basePath}/rec/{path}'
    def getScript(self, path):
        return f'{self.basePath}/scripts/{path}'

class MarkdownRule(bld.Rule):
    def __init__(self, inFile, outFile, basePath):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
        self.basePath = basePath
    def run(self):
        print(f'making {self.outputs[0].name}')
        txt = self.inputs[0].read()

        self.outputs[0].write(MarkdownPage(txt, self))

    def getRec(self, path):
        return f'{self.basePath}/rec/{path}'
    def getScript(self, path):
        return f'{self.basePath}/scripts/{path}'

class LinkRule(bld.Rule):
    def __init__(self, inFile, outFile):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
    def run(self):
        print(f'linking {self.outputs[0].name}')

        links = getLinks(self.inputs[0])
        
        self.outputs[0].write('\n'.join(links))

