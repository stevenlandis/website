import bld
from os.path import join, isdir, isfile
from os import chdir, getcwd
from src.parts.Highlight import getCss
from src.parts.LinkListPage import LinkListPage
from src.parts.MarkdownPage import MarkdownPage

baseDir = getcwd()
allLinks = {}
def addLink(link, source):
  if link not in allLinks:
    allLinks[link] = []
  allLinks[link].append(source)

def main():
  bld.copy('src/config/CNAME', 'build/CNAME')
  bld.File('build/css/highlight.css').write(getCss())
  buildFractalPics() # has to happen before buildSite
  buildSite()
  buildPostsList()
  buildSecretSite()
  buildWebapp()
  buildCookbook()
  verifyLinks()
  # bld.syncFiles('builtFiles')

def clean():
  bld.Dir('build').delete()
  bld.File('builtFiles').delete()

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

# recursively traverse src/site to build the site
def buildSite(dirObj = None, relPath = None):
  if dirObj == None:
    dirObj = bld.Dir('src/site')
    relPath = ''
  for file in dirObj.files():
    if file.name.startswith('_'):
      continue
    elif file.type == 'py':
      buildPyPage(file, bld.File(join('build' + relPath, file.title) + '.html'), relPath)
    elif file.type == 'md':
      buildMdPage(file, bld.File(join('build' + relPath, file.title) + '.html'), relPath)
  for d in dirObj.dirs():
    if d.name.startswith('_'): continue
    buildSite(d, relPath + '/' + d.name)

def checkPage(page, relPath, path):
  links = page.getLinks()
  for link in links:
    if link.startswith('/'):
      addLink(link, path)
    elif link.startswith('http://') or link.startswith('https://'):
      pass
    else:
      addLink((f'{relPath}/{link}'), path)

def getPageInfo(file):
  if file.type == 'md':
    txt = file.read()
    info = frontmatter.loads(txt)
    title = post['title'] if 'title' in post else file.title
    content = DefaultPage(title, Markdown(txt=post.content))
  elif file.type == 'py':
    tempGlobals = {'__file__': file.path}
    chdir(file.parent().abspath)
    exec(txt, tempGlobals)
    if 'build' not in tempGlobals:
      raise Exception(f'"{file.path}"" needs a function build()')
    title = tempGlobals['title'] if 'title' in tempGlobals else file.title
    content = tempGlobals['build']()
    chdir(baseDir)
  return (title, content)

def buildPyPage(file, outFile, relPath):
  if bld.needsUpdate(file, outFile, alwaysUpdate=True):
    print(f'making "{file.path}"')
    txt = file.read()
    tempGlobals = {'__file__': file.path}
    tempGlobals['buildDir'] = bld.Dir('build')
    tempGlobals['relDir'] = outFile.parent()
    chdir(file.parent().abspath)
    exec(txt, tempGlobals)
    if 'build' not in tempGlobals:
      raise Exception(f'"{file.path}"" needs a function build()')
    if 'title' in tempGlobals:
      print(tempGlobals['title'])
    page = tempGlobals['build']()
    chdir(baseDir)
    checkPage(page, relPath, file.path)
    outFile.write(page.getStr())

def buildMdPage(file, outFile, relPath):
  if True or bld.needsUpdate(file, outFile):
    print(f'making "{file.path}"')
    page = MarkdownPage(file.read())
    checkPage(page, relPath, file.path)
    outFile.write(page.getStr())

def buildPostsList():
  links = []
  for folder in bld.Dir('build/posts').dirs():
    for file in folder.files():
      if file.name == 'index.html':
        links.append((folder.name, f'/posts/{folder.name}'))
  page = LinkListPage('Blog Posts', links)
  checkPage(page, '', 'post list')
  bld.File('build/posts/index.html').write(page.getStr())

def buildSecretSite():
  bld.copy(bld.Dir('../encryptWebsite/out'), bld.Dir('build/secret'))

def buildFractalPics():
  sourceDir = bld.Dir('../cppFractal/pics/color path');
  outDir = bld.Dir('build/fractalPics');
  outDir.make()
  for file in sourceDir.files():
    outFile = outDir.getFile(f'{file.title}.jpg');
    if bld.needsUpdate(file, outFile):
      cmd = f'magick convert "{file.path}" "{outFile.path}"'
      bld.call(cmd)

def buildWebapp():
  sourceDir = bld.Dir('../js-app-framework/dist')
  outDir = bld.Dir('build/webapp');
  outDir.make()
  bld.copy(sourceDir, outDir)

def buildCookbook():
  sourceDir = bld.Dir('../Pickens_Cookbook/html')
  outDir = bld.Dir('build/cookbook')
  outDir.make()
  bld.copy(sourceDir, outDir)

def verifyLinks():
  for link in allLinks:
    path = 'build' + link

    # try to copy the file
    if any(link.endswith(typ) for typ in ['.png', '.js', '.css', '.gif', '.jpg', '.svg']):
      fromPath = 'src/site' + link
      if isfile(fromPath):
        bld.copy(fromPath, path)
        continue

    if isdir(path) and isfile(path + '/index.html'):
      continue
    if isfile(path): continue
    # if isfile(path + '.html'): continue

    print(f'Error: unable to resolve "{link}"')
    for refFile in allLinks[link]:
      print(f'  {refFile}')
    # print(f'Error: unable to resolve link "{link}" referenced by {allLinks[link]}')

if __name__ == '__main__':
  main()
