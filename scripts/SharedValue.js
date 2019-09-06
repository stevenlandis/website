class SharedValue {
  constructor() {
    this.watchers = new Set();
  }

  watch(fcn) {
    this.watchers.add(fcn);
  }

  unwatch(fcn) {
    this.watchers.delete(fcn);
  }

  update(value) {
    for (const fcn of this.watchers) {
      fcn(value);
    }
  }
}