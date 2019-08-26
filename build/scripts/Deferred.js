class Deferred {
  constructor() {
    this._promise = new Promise((_resolve, reject) => {
      this._resolve = _resolve;
      this.reject = reject;
    });
    
    this.then = this._promise.then.bind(this._promise);
    this.catch = this._promise.catch.bind(this._promise);
    this[Symbol.toStringTag] = 'Promise';
  }

  resolve(val) {
    this.value = val;
    this._resolve(val);
  }
}