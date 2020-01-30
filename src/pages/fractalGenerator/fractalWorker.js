importScripts('fractal.js');
console.log('starting worker');

self.addEventListener('message', event => {
  console.log('Starting fractal calc:');
  // console.log(event.data);

  // do the fractal calculation
  const angles = event.data.angles;
  const lengths = event.data.lengths;
  const iterations = event.data.iterations;
  const mirrored = event.data.mirrored;
  const width = event.data.width;
  const height = event.data.height;
  const nTurns = Fractal.getTurns(angles.length, iterations);
  postMessage({
    type: 'message',
    message: 'Getting points.'
  });
  const points = Fractal.getPoints(
    angles,
    lengths,
    mirrored,
    0,
    nTurns
  );
  postMessage({
    type: 'message',
    message: 'Finding best angle.'
  });
  let bestAngle = Fractal.getOptimalAngleOffset(points);
  if (height > width) bestAngle += Math.PI/2;
  postMessage({
    type: 'message',
    message: 'Rotating points to best angle.'
  });
  const rotatedPoints = Fractal.getRotatedPoints(points, bestAngle);
  // print(rotatedPoints);
  postMessage({
    type: 'message',
    message: 'Scaling points to fit image.'
  });
  const scaledPoints = Fractal.getScaledPoints(rotatedPoints, width, height, 0.1);
  // print(scaledPoints);

  // send points in blocks of size
  const size = 1000;
  let i = 0;
  let maxI = Math.ceil(scaledPoints.length / size);
  function sendPoints() {
    if (i < maxI) {
      const start = i*size;
      const end = Math.min((i+1)*size, scaledPoints.length);
      postMessage({
        type: 'points',
        points: scaledPoints.slice(start, end)
      });
      i++;
      setTimeout(sendPoints, 1);
    } else {
      postMessage({
        type: 'message',
        message: 'Idle.'
      });
    }
  }
  postMessage({
    type: 'message',
    message: 'Sending points to main thread.'
  });
  sendPoints();

});
