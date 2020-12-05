from src.parts.Elem import Elem, Favicon, StyleSheet, Script
from src.parts.WebPage import WebPage

def build():
  head = [
    Elem('title', 'JS Timer'),
    Favicon(16, 16),
    Favicon(32, 32),
    Favicon(96, 96),
    Script('main.js')
  ]

  body = [
    Elem('div', 'Setup:'),
    Elem('div', Elem('textarea', {'id': 'setup', 'style': 'width:500px;height:150px'})),
    Elem('div', 'Body:'),
    Elem('div', Elem('textarea', {'id': 'text-area', 'style': 'width:500px;height:300px'})),
    Elem('div', Elem('button', {'onClick': 'clickTextArea()'}, 'Run')),
    Elem('div', {'id': 'results'})
  ]

  return WebPage(head, body)
