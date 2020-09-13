from html.parser import HTMLParser
import html
from src.parts.Elem import Elem
import re

class HtmlEvent:
  def __init__(self, typ, tag=None, attrs=None, data=None):
    self.type = typ
    self.tag = tag
    self.attrs = attrs
    self.data = data

class HTMLSerializer(HTMLParser):
  def __init__(self):
    super(HTMLSerializer, self).__init__()
    self.events = []

  def handle_starttag(self, tag, attrs):
    attrs = {key: val for key,val in attrs}
    if tag == 'doctype!': return
    self.events.append(HtmlEvent('starttag', tag=tag, attrs=attrs))
    if tag in Elem.singleElems:
      self.events.append(HtmlEvent('endtag', tag=tag))

  def handle_endtag(self, tag):
    self.events.append(HtmlEvent('endtag', tag=tag))

  def handle_startendtag(self, tag, attrs):
    attrs = {key: val for key,val in attrs}
    self.events.append(HtmlEvent('starttag', tag=tag, attrs=attrs))
    self.events.append(HtmlEvent('endtag', tag=tag))

  def handle_data(self, data):
    # data = re.sub(r'\s+', ' ', data)
    # if data.strip() == '': return
    data = html.escape(data)
    self.events.append(HtmlEvent('data', data=data))

def parseHTML(text):
  parser = HTMLSerializer()
  parser.feed(text)
  events = parser.events
  stack = []
  for event in events:
    if event.type == 'starttag':
      stack.append(Elem(event.tag, event.attrs, []))
    elif event.type == 'data':
      stack[-1].children.append(event.data)
    elif event.type == 'endtag':
      assert stack[-1].tag == event.tag
      top = stack.pop()
      if len(stack) == 0:
        return top
      else:
        stack[-1].children.append(top)
  assert False
