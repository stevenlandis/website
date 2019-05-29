from os.path import isfile, isdir, abspath, join, split
from os import listdir, remove, rmdir
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep

# class observerHandler(FileSystemEventHandler):
#     def on_any_event(self,event):
#         print(event)

# oberver = Observer()
# oberver.schedule(observerHandler(),abspath('website'),recursive=True)
# oberver.start()
# try:
#     while True: sleep(100)
# except:
#     oberver.stop()
#     oberver.join()

def main():
    d = Dir('.')
    for f in d.files: print(f.name)
    # for f in d.files: print(f.name)

# def filesGen(path):
#     paths = [join(path,f) for f in listdir(path)]
#     yield from [File(p) for p in paths if isfile(p)]

class filesGen:
    def __init__(self,path):
        paths = [join(path,f) for f in listdir(path)]
        self.paths = [f for f in paths if isfile(f)]
        self.i = 0
    def __iter__(self): return self
    def __next__(self):
        if self.i < len(self.paths):
            res = File(self.paths[self.i])
            self.i += 1
            return res
        else:
            self.i = 0
            raise StopIteration()

class dirsGen:
    def __init__(self,path):
        self.i = 0
    def reset(self):
        paths = [join(path,f) for f in listdir(path)]
        self.paths = [f for f in paths if isdir(f)]
        self.i = 0
    def __iter__(self): return self
    def __next__(self):
        if self.i == 0: self.reset()
        if self.i < len(self.paths):
            res = Dir(self.paths[self.i])
            self.i += 1
            return res
        else:
            self.i = 0
            raise StopIteration()

class Dir:
    def __init__(self,path):
        path = abspath(path)
        self.path = path
        self.files = filesGen(path)
        self.dirs = dirsGen(path)
    def __getitem__(self,key):
        path = join(self.path,key)
        if isfile(path): return File(path)
        elif isdir(path): return Dir(path)
        else: raise
    def __contains__(self,key):
        path = join(self.path,key)
        return isfile(path) or isdir(path)
    def delete(self):
        for f in self.files: f.delete()
        for d in self.dirs: d.delete()
        rmdir(self.path)

def splitFName(name):
    dotI = name.find('.')
    if dotI == -1: return (name, '')
    else: return (name[:dotI], name[dotI+1:])

class File:
    def __init__(self,path):
        self.path = path
        _,self.name = split(path)
        self.title,self.type = splitFName(self.name)
        # print(f'file: {self.title}.{self.type}')
    def read(self):
        with open(self.path,'r') as f: return f.read()
    def write(self,txt):
        with open(self.path,'w') as f: f.write(txt)
    def delete(self): remove(self.path)

class VirtualDir:
    def __init__(self):
        self.files = []
        self.dirs = []

class VirtualFile:
    def __init__(self,name):
        self.name = name
        self.title,self.type = splitFName(name)
    def place(self,path):
        self.path = path
        self.bld()
    def bld(self): pass

if __name__ == '__main__': main()