from src.parts.Elem import Elem, SingleElem
from src.parts.defs import MainPage
import bld

def build(builder):
    content = [
    ]

    for file in bld.DiskDir('build/rec/fractalPics').files:
        content.append(Elem('h2', file.title))
        content.append(SingleElem('img', attrs={
            'src': f'rec/fractalPics/{file.name}'
        }))

    return MainPage('Fractals', builder, content)