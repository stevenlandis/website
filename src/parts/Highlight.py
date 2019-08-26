import subprocess as sp
from src.parts.Elem import Elem
import re

ltRe = re.compile(r'&amp;lt;')
gtRe = re.compile(r'&amp;gt;')
ampRe = re.compile(r'&amp;amp;')

def Highlight(language, code):
    with open('src\\parts\\temp.txt', 'w', newline='\n') as f:
        f.write(f'{language}\n')
        f.write(code)
    sp.call(['node', 'src\\parts\\highlight.js'])
    with open('src\\parts\\temp.txt', 'r') as f:
        hlText = f.read()

    hlText = ltRe.sub('<', hlText)
    hlText = gtRe.sub('>', hlText)
    hlText = ampRe.sub('&', hlText)

    return Elem('div', Elem('pre', Elem('code', hlText)), attrs={'class': 'code'})