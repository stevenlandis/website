from src.parts.Elem import Elem
from src.parts.defs import MainPage

def PostsPage(posts, builder):
    content = []

    for file in posts:
        href = f'posts/{file.name}'
        label = 'generic label'
        if file.type == 'md':
            txt = file.read()
            post = frontmatter.loads(txt)
            label = post['title'] if 'title' in post else file.title
        else:
            label = file.title

        content.append(Elem('a', label, {'href': href}))

    return MainPage('Posts', builder, content)