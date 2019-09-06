function Elem(...args) {
  if (args.length === 0) {
    throw Error('Elem must have at least one argument');
  }
  if (typeof args[0] === 'string') {
    return new BaseElem(...args);
  }
}
