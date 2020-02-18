from src.parts.Elem import Elem
from pygments.formatters import HtmlFormatter

formatter = HtmlFormatter(cssclass='code', style='tango')

def getCss():
    return formatter.get_style_defs()
