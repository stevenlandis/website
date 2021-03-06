function getNode(elem) {
  if (typeof elem === 'string' || typeof elem === 'number') {
    return document.createTextNode(elem);
  } else if (elem instanceof BaseElem) {
    return elem.get();
  } else if (elem instanceof Array) {
    return elem.map(getNode);
  }
  return undefined;
}

function appendNode(elem, node) {
  if (node === undefined) {
  } else if (node instanceof Array) {
    for (const n of node) {
      appendNode(elem, n);
    }
  } else {
    elem.appendChild(getNode(node));
  }
}

function mergeNode(dest, src) {
  if (typeof src === 'number') {
    src = src.toString();
  }
  if (src === undefined) {
    dest.parentElement.removeChild(dest);
  } else if (typeof src === 'string') {
    if (dest instanceof Text) {
      if (dest.textContent !== src) {
        dest.textContent = src;
      }
    } else {
      const text = document.createTextNode(src);
      dest.parentElement.replaceChild(text, dest);
    }
  } else if (src instanceof BaseElem) {
    src.merge(dest);
  }
}

function mergeChildren(dest, children) {
  while (dest.childNodes.length > children.length) {
    dest.removeChild(dest.lastChild);
  }
  for (let i = 0; i < dest.childNodes.length; i++) {
    mergeNode(dest.childNodes[i], children[i]);
  }
  for (let i = dest.childNodes.length; i < children.length; i++) {
    dest.appendChild(getNode(children[i]));
  }
}

function mergeAttrs(dest, attrs) {
  if (attrs.style !== undefined) {
    for (const key of Object.keys(attrs.style)) {
      if (
        dest.style[key] !== undefined &&
        dest.style[key] !== attrs.style[key]
      ) {
        dest.style[key] = attrs.style[key];
      }
    }
  }
  if (attrs.onClick !== undefined && dest.onclick !== attrs.onClick) {
    dest.onclick = attrs.onClick;
  }
}

class BaseElem {
  constructor(tag, content, attrs = {}) {
    this.tag = tag.toUpperCase();
    if (typeof content === 'number') {
      this.content = content.toString();
    } else {
      this.content = content;
    }
    this.attrs = attrs;
  }

  get() {
    let elem = document.createElement(this.tag);
    appendNode(elem, this.content);
    mergeAttrs(elem, this.attrs);
    return elem;
  }

  merge(dest) {
    if (dest.tagName !== this.tag) {
      dest.parentElement.replaceChild(this.get(), dest);
    } else if (this.content instanceof Array) {
      mergeChildren(dest, this.content);
      mergeAttrs(dest, this.attrs);
    } else {
      if (dest.childNodes.length === 0) {
        appendNode(dest, this.content);
      } else {
        while (dest.childNodes.length !== 1) {
          dest.removeChild(dest.lastChild);
        }
        mergeNode(dest.firstChild, this.content);
      }
      mergeAttrs(dest, this.attrs);
    }
  }
}
