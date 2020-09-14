const print = console.log;

var data = {
  width: '700',
  height: '500',
  fractalString: '1 90 1',
  iterations: '14',
  mirrored: true,
  backgroundColor: 0,
  lineColor: 6,
  message: 'Idle',
};

const backgroundColors = [
  '#000000',
  '#9e9c95',
  '#ffffff',
  '#eb0c0c',
  '#100ceb',
  '#2dd921',
];

const lineColors = [
  '#000000',
  '#9e9c95',
  '#ffffff',
  '#eb0c0c',
  '#100ceb',
  '#2dd921',
  'rainbow',
];

function verifyFractalString(errors) {
  numbers = data.fractalString.split(' ').map(n => parseFloat(n));
  if (numbers.some(isNaN)) {
    errors.push(
      'Fractal string must be space separated numbers. Example: "1 90 1"'
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

  if (errors.length > 0) return;

  return {
    width,
    height,
    iterations,
    angles: base.angles,
    lengths: base.lengths,
    mirrored: data.mirrored,
    turns: Fractal.getTurns(base.angles.length, iterations),
  };
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

function LabeledInt(label, varName) {
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
    }),
    Elem('button', '-', {onClick: event => {
      data[varName] = Math.max(0, data[varName]-1);
      render();
    }}),
    Elem('button', '+', {onClick: event => {
      data[varName]++;
      render();
    }}),
  ]);
}

function LabeledCheckbox(label, varName) {
  return Elem('div', [
    Elem('div', label, {
      style: {
        display: 'inline'
      }
    }),
    Elem('input', '', {
      type: 'checkbox',
      checked: data[varName],
      oninput: event => {
        data[varName] = !data[varName];
        render();
      }
    })
  ]);
}

function LabeledColor(label, varName, colors) {
  const colorElems = colors.map((color, i) => Elem('div', Elem('div', '', {
    style: {
      width: '1.5em',
      height: '1.5em',
      ...(color === 'rainbow'
        ? {backgroundImage: 'linear-gradient(to right, red,orange,yellow,green,blue,indigo,violet)'}
        : {background: color}
      )
    }
  }), {
    style: {
      display: 'inline-block',
      verticalAlign: 'middle',
      marginRight: '1em',
      padding: '0.2em',
      border: i === data[varName]
        ? 'solid black 2px'
        : 'dotted black 2px',
    },
    onClick: event => {
      data[varName] = i;
      render();
    },
  }));

  return Elem('div', [
    Elem('div', label, {
      style: {
        display: 'inline',
        verticalAlign: 'middle',
      }
    }),
    ...colorElems,
  ], {
    style: {
      marginTop: '0.5em',
    }
  });
}

function Message(txt) {
  return Elem('div', txt);
}

function SaveButton() {
  return Elem('div', Elem('button', 'Save as image', {
      onClick: () => {
        print('clicked');
        const canvas = document.body.getElementsByTagName('canvas')[0];
        const image = canvas
          .toDataURL('image/png')
          .replace('image/png', 'image/octet-stream');

        const link = document.createElement('a');
        link.setAttribute('download', 'image.png');
        link.setAttribute('href', image);
        link.click();
      }
    }));
}

function addSummary(data, content) {
  const elems = [];
  elems.push(Elem('div',
    `Angles(deg): ${data.angles.join(', ')}`
  ));
  elems.push(Elem('div',
    `Lengths: ${data.lengths.join(', ')}`
  ));
  elems.push(Elem('div',
    `Iterations: ${data.iterations}`
  ));
  elems.push(Elem('div',
    `Size: (${data.width} x ${data.height})`
  ));
  elems.push(Elem('div',
    `Mirrored: ${data.mirrored}`
  ));
  elems.push(Elem('span', 'Turns: '));
  elems.push(Elem('span', `${data.turns}`, {style: {
    color: data.turns > 10000000 ? 'red' : 'black'
  }}));

  content.push(Elem('div', elems, {style: {fontWeight: 'bold', margin: '1em'}}))
}

let worker = undefined;
function render() {
  pageElem = document.getElementsByTagName('body')[0];

  errors = [];
  var processedData = verifyData(errors);

  var content = [];

  content.push(Elem('div', Elem('a', 'Back to home', {href: '/'}), {style: {paddingBottom: '1em'}}));
  content.push(LabeledInput('Fractal String: ', 'fractalString'));
  content.push(LabeledInt('Iterations: ', 'iterations'));
  content.push(LabeledInput('width: ', 'width'));
  content.push(LabeledInput('height: ', 'height'));
  content.push(LabeledCheckbox('mirrored: ', 'mirrored'));
  content.push(LabeledColor('Background: ', 'backgroundColor', backgroundColors));
  content.push(LabeledColor('Line: ', 'lineColor', lineColors));

  if (errors.length === 0) {
    addSummary(processedData, content);

    content.push(Elem('div', data.message, {id: 'message'}));

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

    content.push(SaveButton());
  } else {
    content.push(
      Elem('div', errors.map(e => Elem('div', e)), { style: { color: 'red' } })
    );
  }

  var page = Elem('body', Elem('div', content), { style: { margin: '1em' } });

  page.merge(pageElem);

  if (errors.length === 0) {
    const canvas = document.body.getElementsByTagName('canvas')[0];
    const ctx = canvas.getContext('2d');

    // use web worker to do fractal calculation
    if (worker !== undefined) worker.terminate();
    worker = new Worker('fractal_resources/fractalWorker.js');
    ctx.beginPath();
    ctx.rect(0,0,processedData.width, processedData.height);
    ctx.fillStyle = backgroundColors[data.backgroundColor];
    ctx.fill();

    let turnI = 0;

    worker.addEventListener('message', event => {
      switch(event.data.type) {
      case 'points':
        const scaledPoints = event.data.points;
        if (lineColors[data.lineColor] === 'rainbow') {
          for (let i = 1;  i < scaledPoints.length; i++) {
            ctx.beginPath();
            ctx.moveTo(scaledPoints[i-1][0], scaledPoints[i-1][1]);
            ctx.lineTo(scaledPoints[i][0], scaledPoints[i][1]);
            const color = Color.getPrimaryColor(turnI/processedData.turns);
            ctx.strokeStyle = Color.rgbToHex(color);
            ctx.stroke();
            turnI++;
          }
        } else {
          ctx.beginPath();
          ctx.moveTo(scaledPoints[0][0], scaledPoints[0][1]);
          for (let i = 1;  i < scaledPoints.length; i++) {
            ctx.lineTo(scaledPoints[i][0], scaledPoints[i][1]);
          }
          ctx.strokeStyle = lineColors[data.lineColor];
          ctx.stroke();
        }
        break;
      case 'message':
        data.message = event.data.message;
        const message = Message(data.message);
        message.merge(document.getElementById('message'));
        break;
      }

    });
    worker.addEventListener('messageerror', event => {
      print('message error:');
      print(event);
    });
    worker.addEventListener('error', event => {
      print('error:');
      print(event);
    });
    worker.postMessage(processedData);
  }
}

window.addEventListener('load', () => {
  render();
});
