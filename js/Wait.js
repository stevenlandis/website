class Wait {
  static map = new Map();

  static wait(valObjs, fcn) {
    if (!(valObjs instanceof Array)) {
      valObjs = [valObjs];
    }

    const fcnObj = { count: 0, fcn };

    for (const valObj of valObjs) {
      if (valObj.value === undefined) {
        fcnObj.count++;
        if (Wait.map.has(valObj)) {
          Wait.map.get(valObj).push(fcnObj);
        } else {
          Wait.map.set(valObj, [fcnObj]);
        }
      }
    }

    // run immediately if no dependencies
    if (fcnObj.count === 0) {
      fcn();
    }
  }

  static update(valueObj, val) {
    if (!Wait.map.has(valueObj)) {
      return;
    }

    valueObj.value = val;

    const fcnObjList = Wait.map.get(valueObj);
    Wait.map.delete(valueObj);

    for (const fcnObj of fcnObjList) {
      fcnObj.count--;
      if (fcnObj.count === 0) {
        fcnObj.fcn();
      }
    }
  }
}
