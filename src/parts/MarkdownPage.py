from src.parts.Markdown import Markdown
from src.parts.defs import MainPage
import frontmatter

def MarkdownPage(txt, builder):
    post = frontmatter.loads(txt)
    title = post['title'] if 'title' in post else 'Title'
    content = Markdown(txt=post.content)

    return MainPage(title, builder, content)
