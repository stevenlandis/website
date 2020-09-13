function _Elem(elem, parent) {
  if (typeof elem === 'string') {
    return {
      type: 'string',
      text: elem,
      parent: parent,
      domElem: undefined,
      parent: undefined,
      target: undefined,
    }
  }
  const res = {
    type: 'elem',
    tag: elem.tag,
    attr: elem.attr,
    domElem: undefined,
    parent: undefined,
    target: undefined,
  };
  res.children = elem.children.map(child => _Elem(child, res));
  return res;
}

_Elem.replaceChild = function(parent, i, elem) {
  parent.children[i] = elem;
  elem.parent = parent;
}

function Component() {}

Component.reset = function() {
  Component.stack = [];
  Component.children = [];
  Component.elem = undefined;
  Component.root = undefined;
  Component.dirtyNodes = new Set();
}

Component.place = function(fcn, ...args) {
  if (typeof fcn === 'function') {
    const res = fcn(...args);
    return res;
  } else {
    console.assert(args.length === 0);

  }
}

