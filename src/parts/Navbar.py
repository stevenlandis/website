from src.parts.Elem import Elem

def NavBarLink(name, href, first=False):
    attrs = {}
    if not first: attrs['style'] = 'margin-left:3em;'
    if attrs == None: attrs = {}
    attrs['href'] = href
    return Elem('span', Elem('a', name, attrs=attrs))

def Navbar(pathGetter, links=None):
    if links == None:
        links = [
            ('Home', 'index.html'),
            ('Resume', 'resume.html'),
            ('Posts', 'postsList.html')
        ]
        return Navbar(pathGetter, links)

    linkElems = []
    for i, (label, name) in enumerate(links):
        href = pathGetter.getPage(name)
        linkElems.append(NavBarLink(label, href, i == 0))

    return Elem('div', linkElems, attrs={'class': 'navbar'})