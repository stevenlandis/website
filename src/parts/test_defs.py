import defs

def testPage():
    assert defs.Page('title', 'head', 'body') == '<!DOCTYPE html><html lang="en"><head><title>title</title>head</head><body>body</body></html>'
