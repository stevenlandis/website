from src.parts.Elem import Elem
from src.parts.DefaultPage import DefaultPage

def build():
    content = [
        Elem('div', 'This is a test page for links'),
        Elem('a', {'href': '/posts/markdownElements'}, 'markdown demo'),
    ]

    return DefaultPage('Test title', content)
