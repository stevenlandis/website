def getFlatList(lst):
  res = []
  for elem in lst:
    if isinstance(elem, list):
      res.extend(getFlatList(elem))
    else:
      res.append(elem)
  return res

class Elem:
  singleElems = {
    'area', 'frame', 'link', 'base', 'hr', 'meta',
    'basefont', 'img', 'param', 'br', 'input', 'col', 'isindex'}
  def __init__(self, *argv):
    if len(argv) == 1:
      tag = argv[0]
      attrs = None
      children = None
    elif len(argv) == 2 and type(argv[0]) == str and type(argv[1]) == dict:
      tag = argv[0]
      attrs = argv[1]
      children = None
    elif len(argv) == 2 and type(argv[0]) == str:
      tag = argv[0]
      attrs = None
      children = [argv[1]]
    elif len(argv) == 3:
      tag = argv[0]
      attrs = argv[1]
      children = argv[2]
    else: raise Exception(f'Invalid Elem signature: {argv}')
    self.tag = tag
    if attrs == None: attrs = {}
    assert type(attrs) == dict
    self.attrs = {key: val for key, val in attrs.items() if val == True or type(val) == str}
    if children == None: children = []
    if type(children) != list: children = [children]
    children = getFlatList(children)
    for child in children:
      assert type(child) == str or callable(child.getStr)
    self.children = children
  def getStr(self):
    attrStr = ''.join([
      f' {key}' if val == True or not type(val) == str else f' {key}="{val}"'
      for key, val in self.attrs.items()])
    if self.tag in Elem.singleElems:
      return f'<{self.tag}{attrStr}>'
    childrenStr = ''.join([
      child if type(child) == str else child.getStr()
      for child in self.children])
    return f'<{self.tag}{attrStr}>{childrenStr}</{self.tag}>'
  def getLinks(self, linkList=None):
    if linkList == None: linkList = set()
    if 'href' in self.attrs: linkList.add(self.attrs['href'])
    if 'src' in self.attrs: linkList.add(self.attrs['src'])
    for child in self.children:
      if type(child) == Elem:
        child.getLinks(linkList)
    return linkList

def Favicon(width, height):
  sizeStr = f'{width}x{height}'
  attrs = {
    'rel': 'icon',
    'type': 'image',
    'href': f'/favicon/{sizeStr}.png',
    'sizes': sizeStr
  }
  return Elem('link', attrs)

def StyleSheet(path):
  attrs = {
    'rel': 'stylesheet',
    'href': path
  }
  return Elem('link', attrs)

def Script(path):
  attrs = {
    'type': 'text/javascript',
    'src': path
  }
  return Elem('script', attrs)

e = Elem('p')
assert e.getStr() == '<p></p>'
e = Elem('p', {'key': True, 'rel': 'stuff.html'}, 'stuff and things')
assert e.getStr() == '<p key rel="stuff.html">stuff and things</p>'
e = Elem('link', {'stuff': True}, ['stuff', 'and', 'things'])
assert e.getStr() == '<link stuff>'
e = Favicon(12, 42)
assert e.getStr() == '<link rel="icon" type="image" href="/favicon/12x42.png" sizes="12x42">'
assert e.getLinks() == {'/favicon/12x42.png'}
e = Elem('p', 'stuff')
assert e.getStr() == '<p>stuff</p>'
assert Elem('p', {'stuff': 'things'}).getStr() == '<p stuff="things"></p>'

# def Elem(tag, content, attrs=None):
#     if attrs == None: attrs = {}

#     if isinstance(content, str): content = [content]
#     content = getFlatList(content)

#     attrStr = getAttrStr(attrs)
#     contentStr = ''.join(content)

#     return f'<{tag}{attrStr}>{contentStr}</{tag}>'

# def SingleElem(tag, attrs=None):
#     if attrs == None: attrs = {}

#     attrStr = getAttrStr(attrs)
#     return f'<{tag}{attrStr}/>'

# def Meta(attrs):
#     attrStr = getAttrStr(attrs)
#     return f'<{attrStr}>'
