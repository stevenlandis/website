import markdown2 as md
import re
from src.parts.Highlight import Highlight

extras = {
    'fenced-code-blocks': {'cssclass': 'code'}
}

convert = md.Markdown(extras=extras).convert

codeRegex = re.compile(r'<pre><code(?: class="(.*)")?>([\s\S]*?)<\/code><\/pre>')

def highlightMatch(match):
    language = match.group(1)
    code = match.group(2)
    return Highlight(language, code)

def Markdown(txt=None, path=None):
    if path != None:
        with open(path, 'r') as f:
            txt = f.read()
    mdTxt = convert(txt)
    # print(mdTxt)
    # mdTxt = codeRegex.sub(highlightMatch, mdTxt)
    return mdTxt