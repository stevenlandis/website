import subprocess as sp

from src.parts.Elem import Elem
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

ltRe = re.compile(r'&amp;lt;')
gtRe = re.compile(r'&amp;gt;')
ampRe = re.compile(r'&amp;amp;')

formatter = HtmlFormatter(cssclass='code', style='xcode')

def oldHighlight(language, code):
    with open('src\\parts\\temp.txt', 'w', newline='\n') as f:
        f.write(f'{language}\n')
        f.write(code)
    sp.call(['node', 'src\\parts\\highlight.js'])
    with open('src\\parts\\temp.txt', 'r') as f:
        hlText = f.read()

    # hlText = ltRe.sub('<', hlText)
    # hlText = gtRe.sub('>', hlText)
    # hlText = ampRe.sub('&', hlText)

    return Elem('div', Elem('pre', Elem('code', hlText)), attrs={'class': 'code'})

def Highlight(language, code):
    if language == None:
        return Elem('div', Elem('pre', code), attrs={'class': 'code'})

    lexer = get_lexer_by_name(language)
    return highlight(code, lexer, formatter)

def getCss():
    return formatter.get_style_defs()