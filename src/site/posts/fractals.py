from src.parts.Elem import Elem
from src.parts.DefaultPage import DefaultPage
import bld

def build():
  content = [
    Elem('p', {}, [
      'Read more about the ',
      Elem('a', {'href': 'dragonCurve'}, 'dragon curve'),
      ' the fractal that started it all.'])
  ]

  for file in buildDir.getDir('fractalPics').files():
    content.append(Elem('h2', file.title))
    content.append(Elem('img', {
      'src': f'../fractalPics/{file.name}'
    }))

  return DefaultPage('Fractals', content)
