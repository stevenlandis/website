import bld
import os
import re
from src.parts.MarkdownPage import MarkdownPage
from src.parts.getLinks import getLinks
from src.getFractalPics import getFractalPics
from src.PostsRule import PostsRule
from src.parts.Highlight import getCss
from src.PathGetter import PathGetter
from src.PostsRule import PostsRule

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

    # posts summary page
    PostsRule(bld.DiskDir('src/pages/posts'), buildDir.getFile('postsList.html'), '')

    return resDir

def getPosts():
    postDir = bld.DiskDir('src/pages/posts')
    outDir = bld.VirDir('build')
    outFile = outDir.getFile('posts')
    PostsRule(postDir, outFile)
    outDir.build('.')

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
        elif inFile.type in ['js', 'png', 'jpg', 'gif']:
            outFile = outDir.getFile(inFile.name)
            bld.CopyRule(inFile, outFile)

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

def watch():
    resDir = getResDir()
    resDir.watch('..')

def serve():
    import http.server
    import socketserver
    import os

    PORT = 8000
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.path = 'build' + self.path
            if not os.path.isdir(self.path):
                _, ext = os.path.splitext(self.path)
                if ext == '': self.path += '.html'
            super().do_GET()

    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'serving at port {PORT}')
        httpd.serve_forever()

def main():
    # from os.path import join
    # from src.parser.md import parseMd
    # from src.parts.Markdown import Markdown
    # with open(join('src','pages','posts','bld2.md'), 'r') as f:
    #     txt = f.read()
    # md = Markdown(txt=txt)
    # # print(md)
    # return
    # post = frontmatter.loads(txt)
    # mdText = Markdown(txt=post.content)
    # print(mdText)
    # return
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

def fixDuplicates(d = bld.DiskDir('.')):
    r = re.compile(r'.* \(\d+\)[\.\w]*$')

    for file in d.files:
        if r.match(file.name):
            print(f'deleting {file.path}')
            file.delete()

    for folder in d.dirs:
        if r.match(folder.name):
            print(f'deleting {folder.path}')
            folder.delete()
        else:
            fixDuplicates(folder)

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
