from src.parts.Elem import Elem

class WebPage:
  def __init__(self, head=None, body=None):
    if head == None: head = []
    head = [
      Elem('meta', {'charset': 'UTF-8'}),
    ] + head
    self.elem = Elem('html', {}, [
      Elem('head', {}, head),
      Elem('body', {}, body)])
  def getStr(self):
    return '<!doctype html>' + self.elem.getStr()
  def getLinks(self):
    return self.elem.getLinks();
