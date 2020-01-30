from src.parts.Elem import Elem
from src.parts.defs import Page, Favicon, StyleSheet, Script

def build(pathGetter):
    head = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        Favicon('16x16', pathGetter),
        Favicon('32x32', pathGetter),
        Favicon('96x96', pathGetter),
        StyleSheet('resumeStyles.css', pathGetter),
        StyleSheet('highlight.css', pathGetter),
        '<style type="text/css" media="print">@page {size: auto;margin: 0;}</style>',
        Script('pr.js', pathGetter),
        Script('Elem.js', pathGetter),
        '<script type="text/javascript" src="color.js"></script>',
        '<script type="text/javascript" src="fractal.js"></script>',
        '<script type="text/javascript" src="page.js"></script>',
    ]

    content = ['content']

    return Page('Fractal Generator', head, content)
