from src.parts.Markdown import Markdown
from src.parts.DefaultPage import DefaultPage
import frontmatter

def MarkdownPage(txt):
  post = frontmatter.loads(txt)
  title = post['title'] if 'title' in post else 'Title'
  content = Markdown(txt=post.content)

  return DefaultPage(title, content)
