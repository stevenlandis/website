import bld
from src.parts.Elem import Elem
from src.parts.defs import MainPage
import frontmatter
from src.PathGetter import PathGetter

def PostsPage(posts, builder):
    content = []

    postInfo = []
    for file in posts:
        href = f'posts/{file.title}.html'
        label = 'generic label'
        if file.type == 'md':
            txt = file.read()
            post = frontmatter.loads(txt)
            label = post['title'] if 'title' in post else file.title
        else:
            label = file.title

        postInfo.append((label, href))

    # sort by label
    postInfo.sort(key = lambda a: a[0].lower())

    content = []
    for label, href in postInfo:
        content.append(Elem(
            'div',
            Elem('a', label, {'href': href}),
            {'class': 'postLink'}
        ))

    return MainPage('Posts', builder, content)

class PostsRule(bld.Rule):
    def __init__(self, postDir, outFile, basePath):
        self.init()
        for file in postDir.files:
            if file.name.startswith('_'):
                continue
            self.addIn(file)
        self.addOut(outFile)
        self.pathGetter = PathGetter(basePath)
    def run(self):
        content = PostsPage(self.inputs, self.pathGetter)
        [outFile] = self.outputs
        outFile.write(content)
