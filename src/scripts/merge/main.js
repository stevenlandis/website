const e1 = Elem('div',
  {
    style: {color: 'red'},
    onclick: () => {log('clicked!!!!!');}
  },
  [
    'stuff and things',
    'things and stuff',
    Elem('button',
      {
        style: {color: 'green'},
        onclick: () => {log('clicked the button');}
      },
      ['Button to click']
    )
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
