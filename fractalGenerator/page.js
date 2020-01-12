var data = {
  width: '700',
  height: '500',
  fractalString: '1 90 1',
  iterations: '5'
};

function verifyFractalString(errors) {
  numbers = data.fractalString.split(' ').map(n => parseInt(n));
  if (numbers.some(isNaN)) {
    errors.push(
      'Fractal string must be space separated integers. Example: "1 90 1"'
    );
    return;
  }

  if (numbers.length < 3) {
    errors.push('Fractal string must have at least 3 numbers.');
    return;
  }

  if (numbers.length % 2 === 0) {
    errors.push('Fractal string must have an odd number of numbers.');

    return;
  }

  const lengths = [];
  const angles = [];

  for (let i = 0; i < numbers.length; i++) {
    if (i % 2 === 0) {
      lengths.push(numbers[i]);
    } else {
      angles.push(numbers[i]);
    }
  }

  return { lengths, angles };
}

function verifyData(errors) {
  const width = parseInt(data.width);
  if (isNaN(width)) {
    errors.push('Width must be an int.');
  }

  const height = parseInt(data.height);
  if (isNaN(height)) {
    errors.push('Height must be an int.');
  }

  const base = verifyFractalString(errors);

  const iterations = parseInt(data.iterations);
  if (isNaN(iterations)) {
    errors.push('Iterations must be an int.');
  }

  return { width, height, base, iterations };
}

function LabeledInput(label, varName) {
  return Elem('div', [
    Elem('div', label, {
      style: {
        display: 'inline'
      }
    }),
    Elem('input', '', {
      value: data[varName],
      oninput: event => {
        data[varName] = event.target.value;
        render();
      }
    })
  ]);
}

function render() {
  pageElem = document.getElementsByTagName('body')[0];

  errors = [];
  var processedData = verifyData(errors);

  var content = [];

  content.push(LabeledInput('Fractal String: ', 'fractalString'));
  if (processedData.base !== undefined) {
    content.push(Elem('div', 'render'));
  }

  content.push(LabeledInput('Iterations: ', 'iterations'));
  content.push(LabeledInput('width: ', 'width'));
  content.push(LabeledInput('height: ', 'height'));

  if (errors.length === 0) {
    content.push(Elem('div', Elem('button', 'Draw!')));

    content.push(
      Elem('canvas', '', {
        width: processedData.width,
        height: processedData.height,
        style: {
          marginTop: '1em',
          border: '1px solid black'
        }
      })
    );
  } else {
    content.push(
      Elem('div', errors.map(e => Elem('div', e)), { style: { color: 'red' } })
    );
  }

  var page = Elem('body', Elem('div', content), { style: { margin: '1em' } });

  page.merge(pageElem);
}

window.addEventListener('load', () => {
  render();
});
