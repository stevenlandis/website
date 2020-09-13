# A Dependency Library

# The Basics

At the base, there are nodes that store a value. I can have a name and an age:
```js
const name = node('Carl');
const age = node(1000);
```

I can't access these values directly, but there's a magic function called `open` that I can use to get the values.
```js
console.log(name); // Object {...}
console.log(open(name)); // 'Joe'
```

I can also change the value of nodes.
```js
name.set('Joe');
console.log(open(name)); // 'Carl'
```

The second thing I can make is a `fcn` which is a value computed from other nodes.
```js
const greeting = fcn(() =>
  `Hello, my name is ${open(name)} and I am ${open(age)} years old`);
```

I can then open my greeting to get the value:
```js
console.log(open(greeting));
// 'Hello, my name is Joe and I am 1000 years old'
```

But the magic really happens when I change one of the base values.
```js
age.set(29);
console.log(open(greeting));
// 'Hello, my name is Joe and I am 29 years old'
```

There we go, that's more reasonable.

# Goodbye classes, hello functions

A cool use of dependent variables is the ability to replace classes with functions and get some performance boosts.

Let's say I have a triangle formed by three points, and I want to get a bounding rectangle.

```js
function Triangle(pt0, pt1, pt2) {
  const minX = fcn(() =>
    Math.min(open(pt0.x), open(pt1.x), open(pt2.x)));
  const maxX = fcn(() =>
    Math.max(open(pt0.x), open(pt1.x), open(pt2.x)));
  const minY = fcn(() =>
    Math.min(open(pt0.y), open(pt1.y), open(pt2.y)));
  const maxY = fcn(() =>
    Math.max(open(pt0.y), open(pt1.y), open(pt2.y)));
  const width = fcn(() => open(maxX) - open(minX));
  const height = fcn(() => open(maxY) - open(minY));
  const area = fcn(() => {
    // via cross product method
    const v0 = {
      x: open(pt1.x) - open(pt0.x),
      y: open(pt1.y) - open(pt0.y)
    };
    const v1 = {
      x: open(pt2.x) - open(pt0.x),
      y: open(pt2.y) - open(pt0.y)
    };
    return Math.abs(v0.x * v1.y - v0.y * v1.x) / 2;
  })
  return {x: minX, y: minY, width, height, area};
}
```

So now I can use the triangle
```js
const pt0 = {x: node(1), y: node(3)};
const pt1 = {x: node(-1), y: node(0)};
const pt2 = {x: node(3), y: node(-7)};
const triangle = Triangle(pt0, pt1, pt2);

console.log(open(triangle.width)); // 4
console.log(open(triangle.height)); // 10
console.log(open(triangle.area)); // 13
```

There are some nice benefits to using this approach over a class:
1. Lazy computation: Values are only computed when they're needed. This means you can get the width of a triangle without the expensive area calculation.
2. Efficient value recalculation: Because the triangle's width doesn't depend on any of the point's y values, changing a y value won't force the width to be recalculated.
3. No `this`: Save your fingers by not typing `this` every time you want to access a value.

# The reason you shouldn't use this everywhere

While dependent variables are pretty cool, they're also really slow. Take the area example above. I compared calculating a triangle's area using a traditional approach and using the dependent variable and the traditional approach was about 2000x times slower. 2000x times. I haven't dug into why it runs so slowly, but I think it has to do with Javascript's garbage collector and the fact that dependent functions are closures with references to many variables. While they are convenient, they should be used carefully when making large applications.

# Another reason you shouldn't use this everywhere

Dependent variables created this way need to keep track of where each variable is used. If a `node` is used in a `fcn`, the node needs to remember that fcn is one of it's users. So what happens when the fcn is no longer needed?

GARBAGE COLLECTION

Suddenly there is this idea of an event loop that manages updating value and state:
1. Change a bunch of values and mark users as invalid
2. Read a bunch of values and re-calculate functions as needed
3. Maybe delete unused nodes

But where this gets tricky is assuming that the dependency graph stays fixed as dependencies change. In most useful programs, `node` changes affect the dependency graph in strange ways. Let's look at the simplest example:

```js
const a = node(5);
const b = node(7);
const cond = node(false);
const c = fcn(() => open(cond) ? open(a) : open(b))

console.log(open(c)) // 7
b.set(11);
console.log(open(c)) // 11
cond.set(true);
console.log(open(c)) // 5
```

In this example, the dependency graph changes based on if `cond` is true or false. However, this also means that the value of `c` needs to be recalculated if `cond` changes.

Another example is for operating on an element in an array:

```js
const list = [node(1), node(2), node(3)];
const i = node(0);
const val = fcn(() => open(list[open(i)]));

console.log(open(val)) // 1
i.set(2);
console.log(open(val)) // 3
list[2].set(42);
console.log(open(val)) // 42
```

This is pretty cool because it means that other elements in that list can change but `val` only depends on a single element. Taking this another step, array elements can be efficiently swapped and sorted by using an index array.

```js

```

However, there's an issue: In javascript, garbage collection only works if references are removed, and if every node and fcn stores a list of all nodes that use itself, each node has a list of references that will challenge the garbage collector. The only solution is to somehow delete nodes.

The idea is simple: When a function node is first created, it doesn't know which variables it depends on and it's dependencies don't have a reference to the node. It's in a `new` state. When the function node runs for the first time, it adds itself to the list of dependers in each of its depencencies, creating a reference loop and a garbage collection nightmare.

But what if there was a way to reset the node back to its new state. I propose `node.reset()`, a method that deletes the cached current value and disconnects dependencies. The node then behaves like a brand new node. If you really need the value, you can always re-calculate it, but it probably won't be needed again.

So there appear to be two ways to think about deleting nodes: top-down and bottom-up

### Top-Down Deleting
If I have a function node that is (probably) no longer needed, I can reset it which starts a chain reaction. Each node has a list of users, and if that list is empty, the node can probably be reset as well.

### Bottom-Up Deleting
This one might not even be necessary but it's still interesting to think about. If I have a base node that is no longer needed and I want to mark it as deleted, that means all nodes that depend on the base node also need to be invalidated and recalculated because they might depend on a deleted node. Now that I think about it, probably not needed and we can do everything with top-down deleting :).

# Stateful Components
Now I can begin to separate dependent logic out and create the base for stateful components.

Let's say I want to create a stateful component like a counter.

```js
function Counter(message) {
  const count = node(5);
  const countString = fcn(() => open(count).toString());

  const render = fcn(() => {
    const res = new Render();
    res.createElement('div', {}, `${open(message)}: ${open(countString)}`);
    res.createElement('button', {onClick: () => {
      count.set(open(count)+1);
    }}, 'Click Me!');
    return res;
  });

  return render;
}
```

Clicking on the button increments the counter and everything works well. However, when I unmount the counter, it still has a reference to message which means JS's garbage collector won't forget `render` or `countString` or `count`. Uh oh.

We need a way to un-watch the render node returned by counter which means carefully resetting the render function after `Counter` unmounts. Not too bad.

# What about async?

Async isn't too bad even though nodes are inherently sync.

```js
const resp = node(null);
(async () => {
  const json = await myWebRequest();
  resp.set(json);
})();

const sum = fcn(() => {
  if (open(resp) === null) {
    return 0;
  }
  return resp.prices.reduce((acc, price) => acc + price, 0);
})

console.log(open(sum)) // 0 b/c resp is initially null

// wait a while

console.log(open(sum)) // 42 b/c the web request finished
```

The main gotcha with async nodes is you need to have a base case for before the response has completed. While this may seem like a pain, and it does add complexity to projects, it makes it easy to visualize your app's state while loading and it updates very efficiently and lazily.

You can also do cool things like make a node that reads a file and updates when the file changes.

```js
function getFileReadNode(path, updateDelay = 1000) {
  const data = node(undefined); // begin as undefined
  let mTime = undefined;
  let run = true;
  (async () => {
    while (run) {
      data.set(await readFile(open(path)));
      await sleep(open(updateDelay));
    }
  }){}
  onReset(() => {
    run = false;
  });
  return data;
}

// a better implementation using the file's modify time
function getFileReadNode(path, updateDelay = 1000) {
  const data = node(undefined); // begin as undefined
  let mTime = undefined;
  let run = true;
  onReset(() => {
    run = false;
  });
  (async () => {
    while (run) {
      const newMTime = await getMTime(open(path));
      if (newMTime === undefined) {
        data.set(undefined);
      } else if (mTime !== newMTime) {
        data.set(await readFile(open(path)));
      }
      await sleep(open(updateDelay));
    }
  }){}
  return data;
}

const fileData = getFileReadNode('test.txt');
const fileSize = fcn(() => open(fileData) === undefined ? 0 : open(fileData).length);

// or
const filePath = node('test.txt');
const delay = node(500);
const fileData = getFileReadNode(filePath, delay);
```

This is really sweet because you can use the file's text throughout your application, but any variables that depend on it will be recalculated when the file changes.
