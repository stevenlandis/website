from src.parts.Elem import Elem
from src.parts.DefaultPage import DefaultPage

def LinkListPage(title, links):
  links = [
    Elem('div', {'class': 'postLink'}, Elem('a', {'href': href}, name))
    for name,href in links]

  content = [
    links
  ]

  return DefaultPage(title, content)
