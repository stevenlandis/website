const log = console.log;

function Elem(tag, attr, children) {
  if (attr === undefined) {
    attr = {};
  }
  if (!('style' in attr)) {
    attr.style = {};
  }
  if (children === undefined) {
    children = [];
  }
  return {tag, attr, children};
}

Elem.diffAttr = function(oldAttr, newAttr) {
  let del = [];
  let styleDel = [];
  let set = [];
  let styleSet = [];
  for (let key in oldAttr) {
    if (key === 'style') {
      for (let styleKey in oldAttr.style) {
        if (!(styleKey in newAttr.style)) {
          styleDel.push(styleKey);
        }
      }
    } else {
      if (!(key in newAttr)) {
        del.push(key);
      }
    }
  }
  for (let key in newAttr) {
    if (key === 'style') {
      for (let styleKey in newAttr.style) {
        if (!(styleKey in oldAttr.style) || oldAttr.style[styleKey] !== newAttr.style[styleKey]) {
          styleSet.push([styleKey, newAttr.style[styleKey]]);
        }
      }
    } else {
      if (!(key in oldAttr) || oldAttr[key] !== newAttr[key]) {
        set.push([key, newAttr[key]]);
      }
    }
  }

  return [del, styleDel, set, styleSet];
}

// log(Elem.diffAttr(
//   {a: 5, b: 6, c: 7, style: {sa: 5, sb: 6, sc: 7}},
//   {b: 6, c: 8, d: 9, style: {sb: 6, sc: 8, sd: 9}},
// ));

Elem.applyDiffAttr = function(diff, domElem) {
  let [del, styleDel, set, styleSet] = diff;
  for (let key of del) {
    domElem[key] = null;
  }
  for (let key of styleDel) {
    domElem.style[key] = null;
  }
  for (let [key, val] of set) {
    domElem[key] = val;
  }
  for (let [key, val] of styleSet) {
    domElem.style[key] = val;
  }
}

Elem.getMergedDomElem = function(oldElem, newElem, domElem) {
  if (typeof oldElem === 'string' && typeof newElem === 'string') {
    if (oldElem === newElem) {
      return domElem;
    }
    return Elem.create(newElem);
  }
  if (typeof oldElem === 'string' || typeof newElem === 'string') {
    return Elem.create(newElem);
  }

  if (oldElem.tag !== newElem.tag) {
    return Elem.create(newElem);
  }

  const diff = Elem.diffAttr(oldElem.attr, newElem.attr);
  Elem.applyDiffAttr(diff, domElem);

  // remove excess nodes
  for (let i = 0; i < oldElem.children.length - newElem.children.length; i++) {
    domElem.removeChild(domElem.lastChild);
  }

  for (let i = 0; i < Math.min(oldElem.children.length, newElem.children.length); i++) {
    const child = Elem.getMergedDomElem(
      oldElem.children[i],
      newElem.children[i],
      domElem.childNodes[i]
    );
    if (child !== domElem.childNodes[i]) {
      domElem.replaceChild(domElem.children[i], child);
    }
  }

  for (let i = oldElem.children.length; i < newElem.children.length; i++) {
    domElem.appendChild(Elem.create(newElem.children[i]));
  }

  return domElem;
}

Elem.create = function(elem) {
  if (typeof elem === 'string') {
    return document.createTextNode(elem);
  }
  let domElem = document.createElement(elem.tag);
  for (let key in elem.attr) {
    if (key === 'style') {
      for (let styleKey in elem.attr.style) {
        domElem.style[styleKey] = elem.attr.style[styleKey];
      }
    } else {
      domElem[key] = elem.attr[key];
    }
  }
  for (let child of elem.children) {
    domElem.appendChild(Elem.create(child));
  }
  return domElem;
}

Elem.merge = function(list, oldElem, newElem) {
  if (oldElem.tag !== newElem.tag) {
    list.push({cmd: 'replaceElem', elem: oldElem, tag: newElem.tag});
    oldElem = new ElemNode()
    list.push({cmd: 'createElem', elem: dest, tag: dest.tag});
    for (let key in dest) {
      if (!(key in src)) {
        list.push({cmd: 'delAttr', name: key});
      }
    }
    for (let key in src) {
      if (!(key in dest) || dest[key] !== src[key]) {
        list.push({cmd: 'setAttr', name: key, val: src[key]});
      }
    }

    // replace src with new element
  }
}
