async function clickTextArea() {
  const speculateTime = 500;
  const sampleTime = 10000;

  const setup = document.getElementById('setup').value;
  const code = document.getElementById('text-area').value;
  const output = document.getElementById('results');
  while (output.firstChild) {
    output.removeChild(output.firstChild);
  }
  const [info, maxIterations] = runUntil(
    (iterations) => runCode(setup, code, iterations),
    (info) => info.duration,
    speculateTime
  );
  addText(output, `Ran ${maxIterations} iterations in ${Math.round(info.duration)}ms`);

  const [canvas, ctx] = addPlot(output);
  await waitForScreenUpdate();

  // loop through intermediate iterations
  const data = [{N: maxIterations, t: info.duration}];
  const t0 = performance.now();
  for (const iterations of subdivide(0, maxIterations)) {
  // for (const iterations of random(0, maxIterations)) {
    const t1 = performance.now();
    if (t1 - t0 > sampleTime) {
      break;
    }
    const {duration} = runCode(setup, code, iterations);
    data.push({N: iterations, t: duration});
    drawPoints(canvas, ctx, data.map(({N, t}) => ({x: N, y: t})));
    await waitForScreenUpdate();
  }

  addText(output, 'Done');
}

async function waitForScreenUpdate() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    })
  })
}

function* subdivide(min, max) {
  let level = 0;
  while (true) {
    const stepSize = (max - min) / (1<<level);
    if (stepSize < 2) break;
    for (let i = 0; i < 1<<level; i++) {
      yield Math.round(stepSize/2 + i*stepSize);
    }
    level++;
  }
}

function* random(min, max) {
  while (true) {
    yield Math.round(min + (max - min) * Math.random());
  }
}

function addText(elem, text) {
  const e = document.createElement('div');
  e.textContent = text;
  elem.appendChild(e);
}

function addPlot(elem) {
  const canvas = document.createElement('canvas');
  canvas.width = 700;
  canvas.height = 500;
  elem.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  return [canvas, ctx];
}

function drawPoints(canvas, ctx, points) {
  const w = canvas.width;
  const h = canvas.height;
  const minX = Math.min(...points.map(point => point.x));
  const maxX = Math.max(...points.map(point => point.x));
  const minY = Math.min(...points.map(point => point.y));
  const maxY = Math.max(...points.map(point => point.y));

  const scaledPoints = points.map(point => ({
    x: point.x / maxX * w,
    y: h - point.y / maxY * h
  }))

  ctx.fillStyle = '#e3e3e3';
  ctx.fillRect(0,0,w,h);
  ctx.fillStyle = 'black';
  for (const {x,y} of scaledPoints) {
    ctx.fillRect(x-2.5,y-2.5,5,5);
  }
}

function runUntil(fcn, getN, N) {
  let i = 1;
  while (true) {
    const info = fcn(i);
    if (getN(info) > N) {
      return [info, i];
    }
    i *= 2;
  }
}

function runCode(setup, code, N) {
  let t0, t1;
  const fragment = `
      ${setup}
      t0 = performance.now();
      ${code}
      t1 = performance.now();
  `;
  eval(fragment);
  return {
    duration: t1 - t0
  };
}
