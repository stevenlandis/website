from src.parts.Elem import Elem

def NavBarLink(name, href, first=False):
    attrs = {}
    if not first: attrs['style'] = 'margin-left:3em;'
    if attrs == None: attrs = {}
    attrs['href'] = href
    return Elem('span', Elem('a', name, attrs=attrs))

def Navbar(links=None):
    if links == None:
        links = [
            ('Home', 'index.html'),
            ('bld.py', 'bld.html'),
            ('Dragon Curve', 'dragonCurve.html'),
            ('Site Elements', 'siteElements.html'),
            ('Software', 'software.html'),
            ('Scope', 'scope.html')
        ]
        return Navbar(links)

    linkElems = []
    for i, (name, href) in enumerate(links):
        linkElems.append(NavBarLink(name, href, i == 0))

    return Elem('div', linkElems, attrs={'class': 'navbar'})