---
title: Run.js
date: Oct 9, 2019
---

I recently had a summer internship where I was exposed to React. I was blown away but how easy it lets me create applications, but I ran into a few situations where the framework fell short. This post is about my plans for (Yet another) javascript application development framework.

React is one of many emerging frameworks that use Declarative Programming, a style of programming where the programmer explains what the resulting application should look like and leaves efficiently changing state up to the framework. You write the application once and use callbacks to initiate changes to program state.

The core of my framework is a function `run(fcn)` that executes a lambda function in a specific environment. When it runs that function it also keeps track of all dependencies of `fcn`, so when any of those dependencies change, `fcn` re-runs. That's it!

Consider the following code for example:

```js
let aRef = Ref(1);
let bRef = Ref(2);

run(() => {
    let a = aRef.load();
    let b = bRef.load();

    console.log(`a: ${a}, b: ${b}`);
});

aRef.set(5);

/* OUTPUT
a: 1, b: 2
a: 5, b: 2
*/
```

When the function `run` is called for the first time it records that the run function depends on `a` and `b`, so when `a` changes to `5`, it re-runs the function which prints out another line.

Just this functionality is incredibly powerful because you can design your application as a graph using natural programming styles and splitting large section of code into smaller run functions that can be re-run as the application changes.

This lets the developer naturally design parts of the application to run as different states change. It also removes the issue of multiple sources of truth because as soon as a variable changes, all functions that use that variable also re-run.

## Ongoing Progress

My current challenge is thinking about another function, `place()` for placing elements in the DOM. This is a necessary part of any js app framework and I'm still thinking about how to set up my code to run efficiently. That being said, I'm pretty confident how `place` will work.

```js
run.mount(bodyElem, () => {
    let nameRef = Ref('Joe');
    let itemsRef = Ref(['Stuff', 'and', 'things'].map(Ref));

    place('div', nameRef);
    
    place('ul', () => {
        const items = itemsRef.load();

        for (const itemRef of items) {
            place('li', itemRef);
        }
    })
})
```

Which renders

```xml
<body>
    <div>Joe</div>
    <ul>
        <li>Stuff</li>
        <li>and</li>
        <li>things</li>
    </ul>
</body>
```

This setup also means that if a function changes `nameRef` to Sam with `nameRef.set('Sam')`, only the text content of the first div will change which means the application state just efficiently re-rendered.

I can just as easily change the list element with `itemsRef[0].set('things')` which changes the first element of the list. I'm still not sure what syntax I should use for base data types to support automatic re-renders on built-in functions like `push` and `pop`.

I believe this style of making applications has a few disadvantages with React:

- No JSX syntax.
- Harder to read.

And a few advantages:

- Flexible `place` syntax.
- Full developer control with how the application re-renders.
- More power for passing variables around.