from src.parts.Elem import Elem, SingleElem, Meta
from src.parts.Navbar import Navbar

def file(fName):
    with open(fName,'r') as f: print(f.read(),end='')

def code(fName, syntax):
    res = f'<pre><code class="{syntax}">'
    with open(fName,'r') as f: res += f.read()
    res += '</code></pre>'
    print(res)

def Page(title, head, body):
    head = Elem('head', [Elem('title', title), head])
    body = Elem('body', body)
    elem = Elem('html', [head, body], attrs={'lang': 'en'})
    return '<!DOCTYPE html>' + elem

def Favicon(size):
    attrs = {
        'rel': 'icon',
        'type': 'image',
        'href': f'favicon/{size}.png',
        'sizes': size
    }
    return SingleElem('link', attrs)

def StyleSheet(path):
    attrs = {
        'rel': 'stylesheet',
        'href': path
    }
    return SingleElem('link', attrs)

def Script(path):
    attrs = {
        'type': 'text/javascript',
        'src': path
    }
    return Elem('script', '', attrs=attrs)

def Title(title):
    return Elem('div', title, attrs={'class': 'title'})

def MainPage(title, content):
    head = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        Favicon('16x16'),
        Favicon('32x32'),
        Favicon('96x96'),
        StyleSheet('styles.css'),
        StyleSheet('highlight.css')
    ]

    body = Elem('div', [
        Title(title),
        Navbar(),
        content
    ], attrs={'class': 'main'})

    return Page(title, head, body)
