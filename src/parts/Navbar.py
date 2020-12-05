from src.parts.Elem import Elem

def Navbar(links=None):
    if links == None:
        links = [
            ('Home', '/'),
            ('Resume', '/resume'),
            ('Posts', '/posts/list'),
            ('Fractal Generator', '/fractal'),
            ('Webapp', '/webapp'),
            ("Picken's Family Cookbook", '/cookbook')
        ]
        return Navbar(links)

    linkElems = []
    for i, (label, link) in enumerate(links):
        linkElems.append(NavBarLink(label, link, i == 0))

    return Elem('div', {'class': 'navbar'}, linkElems)

def NavBarLink(name, href, first=False):
    return Elem('a', {
        'class': 'navbar-link',
        'href': href,
    }, name)
