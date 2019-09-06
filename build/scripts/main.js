window.addEventListener('load', () => {
  function Div(txt) {
    place(Elem('div', txt));
  }

  function Counter(name) {
    const [count, setCount] = useState(0);
    Div(count);
    return Elem('button', name, {
      onClick: () => {
        setCount(count + 1);
      }
    });
  }

  function ToggleColor(colors) {
    const [colorI, setColorI] = useState(0);

    const style = {
      color: colors[colorI],
      backgroundColor: 'white'
    };

    function onClick() {
      setColorI((colorI + 1) % colors.length);
    }

    return Elem('button', 'Click to change color', { style, onClick });
  }

  mount(document.body, () => {
    place(Elem('div', 'stuff'));
    // const testDiv = place(
    //   Elem('div', 'stuff', { style: { position: 'absolute' } })
    // );
    // const andDiv = place(Elem('div', 'and'));
    // place(Elem('div', 'things', { style: { color: 'red' } }));
    // place(Div('things'));
    // place(Div('and'));
    // place(Div('stuff'));

    // place(Div(Div('deep div')));

    // place(Counter('counter 1'));
    // place(Counter('counter 2'));
    // place(Counter('counter 3'));

    // place(ToggleColor(['red', 'green', 'blue', 'yellow', 'purple']));

    // wait([testDiv, andDiv], () => {
    //   const testElem = testDiv.value;
    //   const andElem = andDiv.value;

    //   const testRect = testElem.getBoundingClientRect();
    //   andElem.style.marginTop = `${testRect.height}px`;
    // });

    // wait(testDiv, () => {
    //   const elem = testDiv.value;
    //   function resize() {
    //     const rect = elem.getBoundingClientRect();
    //     const width = window.innerWidth;
    //     elem.style.left = `${(width - rect.width) / 2}px`;
    //   }
    //   resize();
    //   window.addEventListener('resize', resize);
    // });
  });
});
