import subprocess as sp
import markdown2

markdown = markdown2.Markdown()

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