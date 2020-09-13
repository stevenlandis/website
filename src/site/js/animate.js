let animateFcns = []
let animateRequested = false;

function runAnimate() {
  // reset so if fcn() calls animate,
  // it gets put on the next animation frame
  const tmpFcns = animateFcns;
  animateFcns = [];
  animateRequested = false;
  for (const fcn of tmpFcns) {
    fcn();
  }
}

function animate(fcn) {
  animateFcns.push(fcn);
  if (!animateRequested) {
    animateRequested = true;
    window.requestAnimationFrame(runAnimate);
  }
}