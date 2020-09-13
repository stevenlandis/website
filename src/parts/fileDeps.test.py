from src.parts.Elem import Elem
from src.parts.fileDeps import *

lines = [
  'import src.stuff.things',
  'import stuff',
  'import things  ',
]
assert getPythonDeps(lines) == {'src/stuff/things', 'stuff', 'things'}

tree = Elem('a', {'href': 'my/link.png'}, [
  Elem('div', 'ignore/me'),
  Elem('img', {'src': 'other/link.gif'})
])
assert getHtmlTreeDeps(tree) == {'my/link.png', 'other/link.gif'}

lines = [
  '    worker = new Worker(\'fractalWorker.js\');',
]
assert getJsDeps(lines) == {'fractalWorker.js'}
