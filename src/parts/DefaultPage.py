from src.parts.Elem import Elem, Favicon, StyleSheet
from src.parts.WebPage import WebPage
from src.parts.Navbar import Navbar

def DefaultPage(title, content):
  head = [
    Elem('meta', {'charset': 'UTF-8'}),
    Elem('meta', {
      'name': 'viewport',
      'content': 'width=device-width',
      'initial-scale': '1.0'}),
      Favicon(16, 16),
      Favicon(32, 32),
      Favicon(96, 96),
      StyleSheet('/css/styles.css'),
      StyleSheet('/css/highlight.css'),
    Elem('title', title),
  ]

  body = [
    Elem('div', {'class': 'title'}, title),
    Elem('div', {'class': 'main'}, [
      Navbar(),
      content
    ])
  ]

  # body = Elem('div', {'class': 'main'}, [
  #   Elem('div', {'class': 'title'}, title),
  #   Navbar(),
  #   content])

  return WebPage(head, body)
