import subprocess as sp
import markdown as md

markdowner = md.Markdown(extensions=['fenced_code'])

def markdown(fPath):
    with open(fPath,'r') as f:
        return markdowner.convert(f.read())

def file(fName):
    with open(fName,'r') as f: print(f.read(),end='')

def code(fName, syntax):
    res = f'<pre><code class="{syntax}">'
    with open(fName,'r') as f: res += f.read()
    res += '</code></pre>'
    print(res)

class Page:
    def __init__(self,title):
        self.title = title
        self.head = Elem('head', Elem('title',title))
        self.body = Elem('body', [])
        self.elem = Elem('html', [self.head, self.body])
    def __repr__(self):
        return '<!DOCTYPE html>' + str(self.elem)

class MainPage:
    def __init__(self,title,basePath,pageTitle=None):
        if pageTitle == None: pageTitle = title
        self.page = Page(title)
        self.head = self.page.head
        self.head.push('<meta charset="UTF-8">')
        self.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/16x16.png"}" sizes="16x16">')
        self.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/32x32.png"}" sizes="32x32">')
        self.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/96x96.png"}" sizes="96x96">')
        self.head.push(f'<link rel="stylesheet" href="{basePath+"styles.css"}">')
        self.head.push(f'<link rel="stylesheet" href="{basePath+"highlight/styles/xcode.css"}">')
        self.head.push(f'<script src="{basePath+"highlight/highlight.pack.js"}"></script>')
        self.head.push('<script>hljs.initHighlightingOnLoad();</script>')

        self.page.body.push(Elem('div',pageTitle,attrs={'class':'title'}))
        navBar = Elem('div',[],attrs={'class':'navbar'})
        navBar.push(Elem('span',Elem('a','Stuff',attrs={'href':'test.html'})))
        navBar.push(Elem('span',Elem('a','And',attrs={'href':'test.html'})))
        navBar.push(Elem('span',Elem('a','Things',attrs={'href':'test.html'})))
        self.page.body.push(navBar)
        self.body = Elem('div',[],attrs={'class':'main'})
        self.page.body.push(self.body)
    def __repr__(self): return str(self.page)

def getMainPage(title, basePath):
    p = Page(title)
    p.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/16x16.png"}" sizes="16x16">')
    p.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/32x32.png"}" sizes="32x32">')
    p.head.push(f'<link rel="icon" type="image/png" href="{basePath+"favicon/96x96.png"}" sizes="96x96">')
    p.head.push(f'<link rel="stylesheet" href="{basePath+"styles.css"}">')
    p.head.push(f'<link rel="stylesheet" href="{basePath+"highlight/styles/xcode.css"}">')
    p.head.push(f'<script src="{basePath+"highlight/highlight.pack.js"}"></script>')
    p.head.push('<script>hljs.initHighlightingOnLoad();</script>')

    p.body.push(Elem('div',[],attrs={'class':'main'}))

class Elem:
    def __init__(self,tag, content, attrs=None):
        self.tag = tag
        if attrs == None: self.attrs = {}
        else: self.attrs = attrs
        if isinstance(content, list): self.content = content
        elif content == '': self.content = []
        else: self.content = [content]
    def push(self,elem): self.content.append(elem)
    def __contains__(self,key): return key in self.attrs
    def __getitem__(self,key): return self.attrs[key]
    def __setitem__(self,key,value): self.attrs[key] = value
    def __delitem__(self,key): del self.attrs[key]
    def getAttrs(self):
        return ''.join([f' {key}="{self.attrs[key]}"' for key in self.attrs])
    def getContent(self):
        return ''.join([str(e) for e in self.content])
    def __repr__(self):
        return f'<{self.tag}{self.getAttrs()}>{self.getContent()}</{self.tag}>'

class SingleElem:
    def __init__(self,tag, attrs=None):
        self.tag = tag
        if attrs == None: self.attrs = {}
        else: self.attrs = attrs
    def __contains__(self,key): return key in self.attrs
    def __getitem__(self,key): return self.attrs[key]
    def __setitem__(self,key,value): self.attrs[key] = value
    def __delitem__(self,key): del self.attrs[key]
    def getAttrs(self):
        return ''.join([f' {key}="{self.attrs[key]}"' for key in self.attrs])
    def __repr__(self):
        return f'<{self.tag}{self.getAttrs()}>'