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

def Favicon(size, builder):
    attrs = {
        'rel': 'icon',
        'type': 'image',
        'href': builder.getRec(f'favicon/{size}.png'),
        'sizes': size
    }
    return SingleElem('link', attrs)

def StyleSheet(path, builder):
    attrs = {
        'rel': 'stylesheet',
        'href': builder.getRec(path)
    }
    return SingleElem('link', attrs)

def Script(path, builder):
    attrs = {
        'type': 'text/javascript',
        'src': builder.getScript(path)
    }
    return Elem('script', '', attrs=attrs)

def Title(title):
    return Elem('div', title, attrs={'class': 'title'})

def MainPage(title, builder, content):
    head = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        Favicon('16x16', builder),
        Favicon('32x32', builder),
        Favicon('96x96', builder),
        StyleSheet('styles.css', builder),
        StyleSheet('highlight.css', builder)
    ]

    body = Elem('div', [
        Title(title),
        Navbar(builder),
        content
    ], attrs={'class': 'main'})

    return Page(title, head, body)
