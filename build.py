import bld
import os
from src.parts.MarkdownPage import MarkdownPage
from src.parts.getLinks import getLinks
from src.getFractalPics import getFractalPics
from src.parts.Highlight import getCss

def getResDir():
    resources = set()
    pageDir = bld.DiskDir('src/pages')
    resDir = bld.VirDir('website')

    buildDir = resDir.getDir('build')
    getPages(pageDir, buildDir, '')

    # linkDir = resDir.getDir('links')
    # getLinksDir(bld.DiskDir('src'), resDir.getDir('links'))

    # copy resoruce files
    bld.copyDir(bld.DiskDir('rec'), buildDir.getDir('rec'))

    # CNAME
    bld.CopyRule(bld.DiskFile('rec/CNAME'), buildDir.getFile('CNAME'))

    # copy scripts
    bld.copyDir(bld.DiskDir('src/scripts'), buildDir.getDir('scripts'))

    # code highlighting css
    bld.WriteRule(resDir.getFile('build/rec/highlight.css'), getCss())

    return resDir

def getPages(inDir, outDir, basePath):
    for inFile in inDir.files:
        if inFile.name.startswith('_'):
            continue
        elif inFile.type == 'py':
            outFile = outDir.getFile(f'{inFile.title}.html')
            HTMLRule(inFile, outFile, basePath)
        elif inFile.type == 'md':
            outFile = outDir.getFile(f'{inFile.title}.html')
            MarkdownRule(inFile, outFile, basePath)

    for inDir in inDir.dirs:
        if inDir.name.startswith('_'):
            continue

        getPages(
            inDir,
            outDir.getDir(inDir.name),
            f'{basePath}../'
        )

def getLinksDir(inDir, outDir):
    for file in inDir.files:
        if file.type != 'py': continue
        LinkRule(file, outDir.getFile(f'{file.title}.link'))
    for d in inDir.dirs:
        getLinksDir(d, outDir.getDir(d.name))

def fractalPics():
    folder = bld.VirDir('fractalPics')
    getFractalPics(folder)
    folder.build('build')

def site():
    resDir = getResDir()
    resDir.build('..')

def main():
    fractalPics()

    site()

def buildFractalPics():
    resDir = bld.VirDir('fractalPics')


def force():
    resDir = getResDir()
    resDir.rebuild('..')

def clean():
    os.popen('rm -rf build')

def post(name):
    path = os.path.join('src', 'pages', 'posts', name)
    file = bld.DiskFile(path)
    if not file.exists():
        file.write('')

def test(a):
    print(a)

def deploy():
    print('git subtree push --prefix build origin gh-pages')

class PathGetter:
    def __init__(self, basePath):
        self.basePath = basePath

    def getRec(self, path):
        return f'{self.basePath}rec/{path}'

    def getScript(self, path):
        return f'{self.basePath}scripts/{path}'

    def getPage(self, path):
        return f'{self.basePath}{path}'


class HTMLRule(bld.Rule):
    def __init__(self, inFile, outFile, basePath):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
        self.pathGetter = PathGetter(basePath)
    def run(self):
        print(f'making {self.outputs[0].name}')
        txt = self.inputs[0].read()

        tempGlobals = {}
        exec(txt, tempGlobals)

        if 'build' not in tempGlobals:
            raise Exception(f'{self.inputs[0].name} needs a function build()')

        resTxt = tempGlobals['build'](self.pathGetter)

        self.outputs[0].write(resTxt)


class MarkdownRule(bld.Rule):
    def __init__(self, inFile, outFile, basePath):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
        self.pathGetter = PathGetter(basePath)
    def run(self):
        print(f'making {self.outputs[0].name}')
        txt = self.inputs[0].read()

        self.outputs[0].write(MarkdownPage(txt, self.pathGetter))

class LinkRule(bld.Rule):
    def __init__(self, inFile, outFile):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
    def run(self):
        print(f'linking {self.outputs[0].name}')

        links = getLinks(self.inputs[0])
        
        self.outputs[0].write('\n'.join(links))

