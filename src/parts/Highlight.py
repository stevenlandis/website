from src.parts.Elem import Elem
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

formatter = HtmlFormatter(cssclass='code', style='xcode')
def Highlight(language, code):
    print(language)
    if language == None:
        return Elem('div', Elem('pre', code), attrs={'class': 'code'})

    lexer = get_lexer_by_name(language)
    return highlight(code, lexer, formatter)

def getCss():
    return formatter.get_style_defs()