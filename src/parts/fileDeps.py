import re

class DependencyStore:
  def __init__(self):
    self.map = {} # string -> set(string)
    self.allMap = {}
  def getImmDeps(self, file):
    if file.abspath in self.map:
      return self.map[file.abspath]
    if file.type == 'py':
      deps = getPythonDeps(file.lines())
    elif file.type == ''

def getPythonDeps(lines):
  deps = set()
  for line in lines:
    match = re.match(r'^import (.*?)\s*$', line)
    if match:
      deps.add(match.group(1).replace('.', '/'))
  return deps

def getHtmlTreeDeps(tree):
  return tree.getLinks()

def getJsDeps(lines):
  deps = set()
  for line in lines:
    match = re.search(r'new\s+Worker\s*\(\'(.*?)\'\)', line)
    if match:
      deps.add(match.group(1))
  return deps
