from src.parts.Elem import Elem
from src.parts.defs import MainPage
from src.parts.Highlight import Highlight
from src.parts.Markdown import Markdown
from src.parts.MarkdownPage import MarkdownPage

def build(builder):
    content = [
        Markdown(path='src/pages/_index.md')
    ]

    return MainPage('Steven Landis', builder, content)