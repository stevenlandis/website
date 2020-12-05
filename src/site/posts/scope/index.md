---
title: Scope Based Programming
---

### An experiment about a single language object and making it easier to pass information around an application.

## The Problem
I was recently writing some software with a lot of densely connected data structures.

```js
public render() {
  const {
    points,
    width,
    height,
    xUnit,
    yUnit,
    colors = DEFAULT_COLORS
  } = this.props

  const xVals = points.map(d => d.x)
  const xScale = getScale(xVals, xUnit)

  const yVals = points.map(d => d.y)
  const yScale = getScale(yVals, yUnit)

  const scaledPoints = points.map(p => {
    return {
      x: xScale(p.x)
      y: yScale(p.y)
    }
  })
}
```

It quickly becomes difficult to manage how all the functions manipulate variables and writing/reading/changing the code becomes near impossible without writing out a dependency graph.

In addition, as the manipulations become more complicated, functions need lots of arguments and perhaps even multiple outputs to efficiently share and compute data. These large functions are difficult to write/read/maintain.

## The Intuition

It would be nice to access variables without passing individual arguments to a function. It would also be nice to pass variables down without passing them as variables. While this does make code a little less readable, it makes it much simpler to pass variables around.

In other words, it sacrifices readability of low level functions for the readability of high level functions. This isn't too bad because most low lever functions are written by a small group of people who are familiar with the code.

## The Language: Scope

I came up with a language that solves these problems. I'll first explain what this language might look like and then I'll explain why making this language doesn't make sense.

While I was at it, I unified a bunch of things (functions, classes) into a single object: A scope.

### Scopes as mutators

The main idea behind Scope is that function scope extends to child functions.

```js
scope add {
  a += 5
}

var a = 5
add()
print(a) // 5
```

Functions inherit their parent's scope which makes it possible to pass variables by scope instead of by argument.

While this increases the change of side effects, it decreases the visual complexity of code. I'm not sure if the increase of side effects is a good or a bad thing.

### Scopes as functions

You can use a scope as an ordinary function with the following syntax:

```js
scope myFunction(a, b) {
  return a + b
}

print(myFunction(5, 6)) // 11
```

### Scopes as objects

Scopes can also be declared as objects, similar to javascript objects.

```js
scope myObj {
  var a = 1
  var b = 2
}
var obj = myObj()
print(obj.a) // a

scope mySecondObj(a) {
  var b = a + 10
}
var secondObj = mySecondObj(10)
print(secondObj.b) # 20
```

You can also use a js-like shorthand for objects:

```js
var obj = {a: 1, b: 2}
print(obj.a) // 1
```

### Scopes as object mutators

Scopes can be applied to an object using the dot operator:

```js
scope add {
  a += 5
}

var obj = {a: 5}

obj.add()

print(obj.a) // 10
```

This naturally leads right into classes.

### Scopes as classes

```js
scope myClass(a) {
  var b = a

  scope add {
    b += 5
  }
}

var instance = myClass(5)
print(instance.b) // 5
instance.add()
print(instance.b) // 10
```

## Conclusion (For Now)

I've showed how a single object (scope) can be used to represent most features of modern programming. While this demo lacks inheritance, there is probably a way to expose a scope's variables and add private variables to add this functionality.

Scopes let the programmer do a lot because most variables are accessible from strange places. This is good because it leads to concise code but it is bad because it encourages side-effects that complicate code.

This gets into why I don't think this is a viable language. For a programming language to be successful, it has to:

- Solve a problem. Scope does this.
- Be stress tested with real-world applications. Scope doesn't even exist.
- Have support ($$ and people). I'm the only person who knows about scope so definitely not this.

For these reasons, Scope is fun to think about but impractical to actually implement. I am thinking about adding some of Scope's features to javascript as a library instead of a brand-new language.