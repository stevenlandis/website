from src.parts.Elem import Elem, Favicon, StyleSheet, Script
from src.parts.WebPage import WebPage
import bld

def build():
    head = [
        Elem('title', {}, 'Fractal Generator'),
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        Favicon(16, 16),
        Favicon(32, 32),
        Favicon(96, 96),
        '<style type="text/css" media="print">@page {size: auto;margin: 0;}</style>',
        Script('/js/pr.js'),
        Script('/js/Elem.js'),
        Script('color.js'),
        Script('fractal.js'),
        Script('page.js'),
    ]

    content = ['loading javascript']

    # copy the webworker
    bld.copy(
        bld.File('fractalWorker.js'),
        relDir.getFile('fractalWorker.js'))
    # print(bld.File('fractal_resources/fractalWorker.js'))
    # print(relDir.abspath)

    return WebPage(head, content)
