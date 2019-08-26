def getAttrStr(attrs):
    return ''.join([f' {key}="{attrs[key]}"' for key in attrs])

def getFlatList(lst):
    res = []
    for elem in lst:
        if isinstance(elem, list):
            res.extend(getFlatList(elem))
        else:
            res.append(elem)
    return res

def Elem(tag, content, attrs=None):
    if attrs == None: attrs = {}
    
    if isinstance(content, str): content = [content]
    content = getFlatList(content)

    attrStr = getAttrStr(attrs)
    contentStr = ''.join(content)

    return f'<{tag}{attrStr}>{contentStr}</{tag}>'

def SingleElem(tag, attrs=None):
    if attrs == None: attrs = {}

    attrStr = getAttrStr(attrs)
    return f'<{tag}{attrStr}/>'