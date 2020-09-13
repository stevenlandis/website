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
        Script('fractal_resources/color.js'),
        Script('fractal_resources/fractal.js'),
        Script('fractal_resources/page.js'),
    ]

    content = ['loading javascript']

    # copy the webworker
    bld.copy(
        bld.File('fractal_resources/fractalWorker.js'),
        buildDir.getFile('fractal_resources/fractalWorker.js'))
    # print(bld.File('fractal_resources/fractalWorker.js'))
    # print(buildDir.abspath)

    return WebPage(head, content)
