window.addEventListener('load', () => {
  const assert = console.assert;

  // ---------
  //  getNode
  // ---------
  (() => {
    let node;

    node = getNode(undefined);
    assert(node === undefined);

    node = getNode('stuff');
    assert(node instanceof Text);
    assert(node.textContent === 'stuff');
    assert(node.childNodes.length === 0);

    node = getNode(101);
    assert(node instanceof Text);
    assert(node.textContent === '101');
    assert(node.childNodes.length === 0);

    node = getNode(Elem('a', 'stuff'));
    assert(node instanceof HTMLAnchorElement);
    assert(node.textContent === 'stuff');
    assert(node.childNodes.length === 1);

    node = getNode(['stuff', 'and']);
    assert(node instanceof Array);
    assert(node.length === 2);
    assert(node[0] instanceof Text);
    assert(node[0].textContent === 'stuff');
    assert(node[1] instanceof Text);
    assert(node[1].textContent === 'and');
  })();

  // ------------
  //  appendNode
  // ------------
  (() => {
    let elem;

    elem = Elem('a').get();
    appendNode(elem, undefined);
    assert(elem.childNodes.length === 0);

    elem = Elem('a').get();
    appendNode(elem, 'stuff');
    assert(elem.childNodes.length === 1);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.textContent === 'stuff');

    elem = Elem('a').get();
    appendNode(elem, ['stuff', 'and']);
    assert(elem.childNodes.length === 2);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.childNodes[0].textContent === 'stuff');
    assert(elem.childNodes[1] instanceof Text);
    assert(elem.childNodes[1].textContent === 'and');

    elem = Elem('a').get();
    appendNode(elem, ['stuff', [[['and']]]]);
    assert(elem.childNodes.length === 2);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.childNodes[0].textContent === 'stuff');
    assert(elem.childNodes[1] instanceof Text);
    assert(elem.childNodes[1].textContent === 'and');
  })();

  // -----------
  //  mergeNode
  // -----------
  (() => {
    let elem, parent;

    parent = Elem('a', Elem('a', 'stuff')).get();
    elem = parent.childNodes[0];
    mergeNode(elem, undefined);
    assert(parent.childNodes.length === 0);

    parent = Elem('a', 'stuff').get();
    elem = parent.childNodes[0];
    mergeNode(elem, 'things');
    assert(parent instanceof HTMLAnchorElement);
    assert(parent.childNodes.length === 1);
    assert(parent.childNodes[0] instanceof Text);
    assert(parent.childNodes[0].textContent === 'things');

    parent = Elem('a', Elem('a', 'stuff')).get();
    elem = parent.childNodes[0];
    mergeNode(elem, 'things');
    assert(parent instanceof HTMLAnchorElement);
    assert(parent.childNodes.length === 1);
    assert(parent.childNodes[0] instanceof Text);
    assert(parent.childNodes[0].textContent === 'things');

    parent = Elem('a', Elem('a', 'stuff')).get();
    mergeNode(parent, Elem('a', Elem('div')));
    assert(parent instanceof HTMLAnchorElement);
    assert(parent.childNodes.length === 1);
    assert(parent.childNodes[0] instanceof HTMLDivElement);
    assert(parent.childNodes[0].childNodes.length === 0);
  })();

  // -------------------
  //  BaseElem.constructor
  // -------------------
  (() => {
    let elem;

    elem = Elem('stuff', 22, { style: 'things' });
    assert(elem.tag === 'STUFF');
    assert(elem.content === '22');
    assert(elem.attrs.style === 'things');
  })();

  // -----------
  //  BaseElem.get
  // -----------
  (() => {
    let elem;

    elem = Elem('div', 'stuff').get();
    assert(elem instanceof HTMLDivElement);
    assert(elem.childNodes.length === 1);
    assert(elem.textContent === 'stuff');
  })();

  // -------------
  //  BaseElem.merge
  // -------------
  (() => {
    let elem, parent;

    parent = Elem('a', Elem('div', 'stuff')).get();
    elem = parent.childNodes[0];
    Elem('a', 'things').merge(elem);
    assert(parent instanceof HTMLAnchorElement);
    assert(parent.childNodes.length === 1);
    assert(parent.childNodes[0] instanceof HTMLAnchorElement);
    assert(parent.childNodes[0].childNodes.length === 1);
    assert(parent.childNodes[0].textContent === 'things');

    elem = Elem('a').get();
    Elem('a', 'things').merge(elem);
    assert(elem instanceof HTMLAnchorElement);
    assert(elem.childNodes.length === 1);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.childNodes[0].textContent === 'things');

    elem = Elem('a', ['stuff', 'and', 'things']).get();
    Elem('a', 'quack').merge(elem);
    assert(elem instanceof HTMLAnchorElement);
    assert(elem.childNodes.length === 1);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.childNodes[0].textContent === 'quack');

    elem = Elem('a', ['stuff', 'and', 'things']).get();
    Elem('a', []).merge(elem);
    assert(elem instanceof HTMLAnchorElement);
    assert(elem.childNodes.length === 0);

    elem = Elem('a', ['stuff', 'and', 'things']).get();
    Elem('a', ['quack']).merge(elem);
    assert(elem instanceof HTMLAnchorElement);
    assert(elem.childNodes.length === 1);
    assert(elem.childNodes[0] instanceof Text);
    assert(elem.childNodes[0].textContent === 'quack');

    elem = Elem('a', ['stuff', 'and', 'things']).get();
    Elem('a', [1, 'and', 3, 4, 5]).merge(elem);
    assert(elem instanceof HTMLAnchorElement);
    assert(elem.childNodes.length === 5);
    assert(elem.childNodes[0].textContent === '1');
    assert(elem.childNodes[1].textContent === 'and');
    assert(elem.childNodes[2].textContent === '3');
    assert(elem.childNodes[3].textContent === '4');
    assert(elem.childNodes[4].textContent === '5');
  })();

  // ------
  //  wait
  // ------
  {
    const valObj = {};
    let called = 0;

    wait(valObj, () => {
      called++;
      assert(valObj.value === 2);
    });
    assert(called === 0);

    updateWait(valObj, 2);
    assert(called === 1);
    assert(valObj.value === 2);
    assert(waitMap.size === 0);
  }
  {
    const valObj1 = {};
    const valObj2 = {};
    let called = 0;

    wait([valObj1, valObj2], () => {
      called++;
      assert(valObj1.value === 1);
      assert(valObj2.value === 2);
    });

    assert(called === 0);
    updateWait(valObj1, 1);
    assert(called === 0);
    updateWait(valObj2, 2);
    assert(called === 1);
    assert(waitMap.size === 0);
  }
  {
    const v1 = {};
    const v2 = {};
    const v3 = {};
    let called1 = 0;
    let called2 = 0;

    wait([v1, v2], () => {
      called1++;
      assert(v1.value === 1);
      assert(v2.value === 2);
    });

    wait([v2, v3], () => {
      called2++;
      assert(v2.value === 2);
      assert(v3.value === 3);
    });

    assert(called1 === 0);
    assert(called2 === 0);
    updateWait(v2, 2);
    assert(called1 === 0);
    assert(called2 === 0);
    updateWait(v3, 3);
    assert(called1 === 0);
    assert(called2 === 1);
    updateWait(v1, 1);
    assert(called1 === 1);
    assert(called2 === 1);
    assert(waitMap.size === 0);
  }
  {
    const v1 = {};
    const v2 = {};
    const v3 = {};
    let called1 = 0;

    wait([v1, v2], () => {
      called1++;
      assert(v1.value === 1);
      assert(v2.value === 2);
    });

    assert(called1 === 0);
    updateWait(v1, 1);
    assert(called1 === 0);
    updateWait(v2, 2);
    assert(called1 === 1);

    let called2 = 0;
    wait([v2, v3], () => {
      called2++;
      assert(v2.value === 2);
      assert(v3.value === 3);
    });

    updateWait(v3, 3);
    assert(called1 === 1);
    assert(called2 === 1);
    assert(waitMap.size === 0);

    let called3 = 0;
    wait([v1, v2, v3], () => {
      called3++;
      assert(v1.value === 1);
      assert(v2.value === 2);
      assert(v3.value === 3);
    });
    assert(called3 === 1);
  }
});
