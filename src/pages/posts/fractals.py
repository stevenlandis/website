from src.parts.Elem import Elem, SingleElem
from src.parts.defs import MainPage
import bld

def build(builder):
    content = [
        Elem('p', [
            'Read more about the ',
            Elem('a', 'dragon curve', attrs = {'href': 'dragonCurve.html'}),
            ', the fractal that started it all.'
        ])
    ]

    for file in bld.DiskDir('build/fractalPics').files:
        content.append(Elem('h2', file.title))
        content.append(SingleElem('img', attrs={
            'src': f'../fractalPics/{file.name}'
        }))

    return MainPage('Fractals', builder, content)