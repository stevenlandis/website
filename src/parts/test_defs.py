import defs

def testGetAttrStr():
    assert defs.getAttrStr({}) == ''
    assert defs.getAttrStr({'stuff': 'things', 'and': 'stuff'}) == ' stuff="things" and="stuff"'

def testGetFlatList():
    assert defs.getFlatList([]) == []
    assert defs.getFlatList([[]]) == []
    assert defs.getFlatList([1, 2, 3]) == [1, 2, 3]
    assert defs.getFlatList([1, 2, [3]]) == [1, 2, 3]
    assert defs.getFlatList([1, 2, [[3]]]) == [1, 2, 3]
    assert defs.getFlatList([[1, 2], [[3, 4, 5]], 6]) == [1, 2, 3, 4, 5, 6]

def testElem():
    assert defs.Elem('stuff', '') == '<stuff></stuff>'
    assert defs.Elem('stuff', 'content') == '<stuff>content</stuff>'
    assert defs.Elem('stuff', ['stuff', 'and']) == '<stuff>stuffand</stuff>'
    assert defs.Elem('stuff', 'content', {'stuff': 'things', 'and': 'stuff'}) == '<stuff stuff="things" and="stuff">content</stuff>'

def testSingleElem():
    assert defs.SingleElem('stuff') == '<stuff/>'
    assert defs.SingleElem('stuff', {'a': 'b'}) == '<stuff a="b"/>'

def testPage():
    assert defs.Page('title', 'head', 'body') == '<!DOCTYPE html><html><head><title>title</title>head</head><body>body</body></html>'