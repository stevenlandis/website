class NodeContext {
  constructor(parent) {
    this.parent = parent;
    this.startElem = null;
    this.endElem = null;
    this.children = [];
    this.placedNodes = [];
    this.states = [];
  }
}

let placedNodes = [];
function place(node, ...args) {
  if (node instanceof BaseElem) {
    const deferred = {};
    placedNodes.push([node, deferred]);
    return deferred;
  } else {
    return node(...args);
  }
}

let renderFcn;
let mountElem;

let states = [];
let stateI = 0;
function useState(init) {
  if (stateI >= states.length) {
    if (typeof init === 'function') {
      states.push(init());
    } else {
      states.push(init);
    }
  }
  const state = states[stateI];
  const tempRenderFcn = renderFcn;
  const tempStateI = stateI;
  function setState(nextState) {
    states[tempStateI] = nextState;
    placedNodes = [];
    stateI = 0;
    tempRenderFcn();
    const nodes = placedNodes.map(n => n[0]);
    mergeChildren(mountElem, nodes);
    for (let i = 0; i < placedNodes.length; i++) {
      placedNodes[i][1].resolve(mountElem.childNodes[i]);
    }
  }
  stateI++;
  return [state, setState];
}

function mount(elem, fcn) {
  animate(() => {
    placedNodes = [];
    stateI = 0;
    renderFcn = fcn;
    mountElem = elem;
    fcn();
    const nodes = placedNodes.map(n => n[0]);
    mergeChildren(elem, nodes);
    for (let i = 0; i < placedNodes.length; i++) {
      updateWait(placedNodes[i][1], elem.childNodes[i]);
    }
  });
}
