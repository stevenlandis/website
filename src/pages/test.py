from src.parts.Elem import Elem
from src.parts.defs import MainPage

def build(getResource):
    content = [
        Elem('div', 'This is a test page for links')
    ]

    return MainPage('My Title', getResource, content)