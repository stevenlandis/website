const e1 = Elem(
  'div',
  {
    style: {color: 'red'},
    onclick: () => {log('clicked!!!!!');}
  },
  [
    'stuff and things',
    'things and stuff',
  ]
);

let e;
window.onload = function() {
  e = Elem.create(e1);
  document.body.appendChild(e);
}

function Button(title, onclick) {
  return Elem('button', {onclick}, title);
}

function Doc(title) {
  countRef = ref(0);
  const count = countRef.get();
  const setCount = countRef.set;

  function b1Pressed() {
    print('pressed b1');
    setCount(count+1);
  }

  function b2Pressed() {
    print('pressed b2');
    setCount(count+1);
  }

  return Elem('body', {}, [
    Elem('div', {}, title),
    Elem('div', {}, `Count: ${count}`),
    place(Button, 'button 1', b1Pressed),
    place(Button, 'button 2', b2Pressed),
  ]);
}

place(Doc, 'my title');
