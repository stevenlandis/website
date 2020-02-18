import re
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
import os.path

class HighlightRenderer(mistune.Renderer):
  def block_code(self, code, lang=None):
    if lang == None:
      return (
        '<pre class="code codeblock"><code>' +
        mistune.escape(code) +
        '</code></pre>'
      )
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = html.HtmlFormatter()
    fCode = highlight(code, lexer, formatter)
    fCode = fCode[len('<div class="highlight"><pre>'):-len('</pre></div>')-1]
    return (
        '<pre class="code codeblock"><code>' +
        fCode +
        '</code></pre>'
      )
  def codespan(self, text):
    return (
      '<code class="code codespan">' +
      mistune.escape(text) +
      '</code>'
    )
  def link(self, link, text=None, title=None):
    if not link.startswith('http'):
      tempLink, ext = os.path.splitext(link)
      if ext == '.html': link = tempLink

    if title == None and text == None:
      text = link
    elif text == None:
      text = title

    s = '<a href="' + link + '"'
    if title:
        s += ' title="' + mistune.escape(title) + '"'
    return s + '>' + text + '</a>'

convert = mistune.Markdown(renderer=HighlightRenderer())
def Markdown(txt=None, path=None):
    if path != None:
        with open(path, 'r') as f:
            txt = f.read()
    return convert(txt)
