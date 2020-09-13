from src.parts.WebPage import WebPage
from src.parts.Elem import Elem, Script

def build():
    head = [
        Elem('title', {}, 'Script Test'),
        Script('/js/pr.js'),
        Script('/js/Wait.js'),
        Script('/js/BaseElem.js'),
        Script('/js/Elem.js'),
        Script('/js/animate.js'),
        Script('/js/test.js'),
        Script('/js/main.js')
    ]

    return WebPage(head)
