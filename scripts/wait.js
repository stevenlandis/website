const waitMap = new Map();

function wait(valObjs, fcn) {
  if (!(valObjs instanceof Array)) {
    valObjs = [valObjs];
  }

  const fcnObj = { count: 0, fcn };

  for (const valObj of valObjs) {
    if (valObj.value === undefined) {
      fcnObj.count++;
      if (waitMap.has(valObj)) {
        waitMap.get(valObj).push(fcnObj);
      } else {
        waitMap.set(valObj, [fcnObj]);
      }
    }
  }

  // run immediately if no dependencies
  if (fcnObj.count === 0) {
    fcn();
  }
}

function updateWait(valueObj, val) {
  if (!waitMap.has(valueObj)) {
    return;
  }

  valueObj.value = val;

  const fcnObjList = waitMap.get(valueObj);
  waitMap.delete(valueObj);

  for (const fcnObj of fcnObjList) {
    fcnObj.count--;
    if (fcnObj.count === 0) {
      fcnObj.fcn();
    }
  }
}
