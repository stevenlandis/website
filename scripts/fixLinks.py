from html.parser import HTMLParser
import html

def fixLink(link):
  if link.startswith('http://') or link.startswith('https://'):
    return link
  if link.startswith('/'):
    return link

def getAttrStr(attrs):
  res = []
  for key, val in attrs:
    if val == None:
      res.append(key)
    else:
      res.append(f'{key}="{val}"')
  if len(res) == 0: return ''
  return ' ' + ' '.join(res)

class LinkFixer(HTMLParser):
  def __init__(self):<p></p>
    super(LinkFixer, self).__init__()
    self.res = [] # array of strings in resulting file

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      newAttrs = []
      for key, val in attrs:
        if key == 'href':
          print(val)
        newAttrs.append((key, val))
      attrs = newAttrs
    self.res.append(f'<{tag}{getAttrStr(attrs)}>')

  def handle_endtag(self, tag):
    self.res.append(f'</{tag}>')

  def handle_startendtag(self, tag, attrs):
    self.res.append(f'<{tag}{getAttrStr(attrs)}/>')

  def handle_data(self, data):
    self.res.append(data)

def fixLinks(html):
  fixer = LinkFixer()
  fixer.feed(html)
  return ''.join(fixer.res)
