import re
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os.path
from src.parts.Elem import Elem
from src.parts.parseHTML import parseHTML
from os import getcwd
from os.path import abspath, commonprefix, relpath
import bld

def escape_html(txt):
  if txt == None: return None
  return mistune.escape_html(txt)

class CustomRenderer(mistune.AstRenderer):
  def text(self, text):
    return escape_html(text)

  def link(self, link, children=None, title=None):
    title = escape_html(title)
    return Elem('a', {'href': link,}, children)

  def image(self, src, alt=None, title=None):
    alt = escape_html(alt)
    title = escape_html(title)
    return Elem('img', {'src': src, 'alt': alt, 'title': title})

  def emphasis(self, text):
    return Elem('em', {}, text)

  def strong(self, text):
    return Elem('strong', {}, text)

  def codespan(self, text):
    return Elem('code', {}, escape_html(text))

  def linebreak(self):
    return Elem('br')

  def inline_html(self, html):
    return html

  def paragraph(self, text):
    return Elem('p', {}, text)

  def heading(self, children, level):
    if level == 1:
      img = Elem('img', {'src': '/svg/logo.svg', 'class': 'h1-img'})
      return Elem(f'h{level}', {}, [img, children])
    return Elem(f'h{level}', {}, children)

  def newline(self):
    return ''

  def thematic_break(self):
    return Elem('hr')

  def block_text(self, text):
    return text

  def block_code(self, code, lang='text'):
    try:
      lexer = get_lexer_by_name(lang)
    except:
      lexer = get_lexer_by_name('text')
    formatter = HtmlFormatter()
    htmlStr = highlight(code, lexer, formatter)
    return parseHTML(htmlStr)
    # return highlight(code, lexer, HtmlFormatter())
    #   return code
    # except:
    #   code = escape_html(code)
    # return Elem('div', {'class': 'codeblock'}, Elem('pre', {'class': 'code'}, code))
    # return Elem('pre', {'class': 'codeblock'}, Elem('code', {}, escape_html(code)))

  def block_quote(self, text):
    return Elem('blockquote', {}, text)

  def block_html(self, children):
    return children

  def list(self, children, ordered, level, start=None):
    if ordered:
      if start: return Elem('ol', {'start': str(start)}, children)
      else: return Elem('ol', {}, children)
    else:
      return Elem('ul', {}, children)

  def list_item(self, children, level):
    return Elem('li', {}, children)

convert = mistune.Markdown(renderer=CustomRenderer())
def Markdown(txt=None, path=None):
  if path != None:
    with open(path, 'r') as f:
      txt = f.read()
  return convert(txt)
