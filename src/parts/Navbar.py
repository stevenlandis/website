from src.parts.Elem import Elem

def NavBarLink(name, href, first=False):
    attrs = {}
    if not first: attrs['style'] = 'margin-left:3em;'
    attrs['href'] = href
    return Elem('span', {}, Elem('a', attrs, name))

def Navbar(links=None):
    if links == None:
        links = [
            ('Home', '/'),
            ('Resume', '/resume'),
            ('Posts', '/posts/list'),
            ('Fractal Generator', '/fractal')
        ]
        return Navbar(links)

    linkElems = []
    for i, (label, link) in enumerate(links):
        linkElems.append(NavBarLink(label, link, i == 0))

    return Elem('div', {'class': 'navbar'}, linkElems)
