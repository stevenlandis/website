---
title: Rule Inputs
---

This post discusses how to find dependencies for [bld](../bld), a project builder I made.

Rules have inputs (dependencies) and outputs (results). For bld, these inputs and outputs are files, but they could be many other things such as variables. Bld only lets users declare inputs and outputs before running a rule but there is another way.

Let's say you are baking a cake and you want to know which ingredients to use for each step. The recipe can specify ingredients in two different ways:

1. Listing the ingredients before the recipe and referencing them throughout the recipe.
2. Specifying the ingredients throughout the recipe.

It's the difference between

```
1. Mix ingredients
  - 1 cup flour
  - 1 cup water

  Mix the flour and water in a bowl.

2. Bake the dough
  - Dough mixture
  - A pan
  - A hot oven

  Pour the dough mixture into a pan.
  Bake for 20 minutes.
```

and

```
1. Mix 1 cup flour and 1 cup water in a bowl.
2. Pour the dough mixture into a pan and
   bake for 20 minutes.
```

The first recipe makes it clear what the cook needs to do for each step but makes more work for the recipe writer.

In the second recipe, ingredients are implied by the instructions which is easier for the recipe writer but harder to see required ingredients. I would rather write a program using the second approach and use a program analysis tool to create the first form.

Consider the following code snippet:

```js
// The function wait(cond, fcn) waits until condition is true
// to run fcn.

var a = false;
var b = false;
print("set a and b");

wait(a && b, () => {
  print("a and b are both true!");
});
print("set up wait function");

a = true;
print("set a to true");

b = true;
print("set b to true");

/*
OUTPUT
> set a and b
> set up wait function
> set a to true
> a and b are both true!
> set b to true
*/
```

This isn't achievable with normal javascript, but a few small changes would make this program possible.

```js
// The function wait(cond, fcn) waits until condition is true
// to run fcn.

var a = Var(false);
var b = Var(false);
print("set a and b");

wait(
  () => {
    a.get() && b.get();
  },
  () => {
    print("a and b are both true!");
  }
);
print("set up wait function");

a.set(true);
print("set a to true");

b.set(true);
print("set b to true");

/*
OUTPUT
> set a and b
> set up wait function
> set a to true
> a and b are both true!
> set b to true
*/
```

Just like the second recipe approach, `wait()` remembers what variables it's condition uses when it first runs. Whenever one of those variables changes, it re-runs the condition. When both `a` and `b` are set to `true`, the waited function finally runs.

This optimization is very efficient because it only checks the condition when one of its dependencies changes. This also creates very clean code and lets the library handle all dependency analysis.

In addition, `a` or `b` could be a computed variable:

```js
var a1 = Var(false);
var a2 = Var(false);

var a = FcnVar(() => a1.get() || a2.get());
var b = Var(true);

wait(
  () => {
    a.get() && b.get();
  },
  () => {
    print("a and b are both true!");
  }
);
print("set up wait function");

a1.set(true);
print("set a1 to true");

/*
OUTPUT
> set up wait function
> a and b are both true!
> set a1 to true
*/
```

The library automatically figures out that `a` depends on `a1` and `a2`, so changing their values propagates the change up to `wait`.

# Update: Mar 12, 2020

I have a working version! I made a few changes and the function works as expected, but I'm running into some unexpected issues with integrating `run()` into a program. More on that later.

There are some mild changes. First of all, instead of `wait`, I switch the function to `run` because it makes a little more sense. I also changed `Var` to `Ref`.

```js
var a1 = Ref(false);
var a2 = Ref(false);

var a = FcnRef(() => a1.get() || a2.get());
var b = Ref(true);

run(() => {
  if (a.get() && b.get()) {
    print("a and b are both true!");
  }
});
print("set up run function");

print("setting a1 to true");
a1.set(true);

/*
OUTPUT
> set up wait function
> setting a1 to true:
> a and b are both true!
*/
```

And there it is. In plain javascript with a minimal syntax, this script is an efficient implementation of dependent variables. This setup means it is possible to use variables with confidence.

One of the main issues with programming is duplication of source of truth. Dependent programming eliminates this issue because variables are recalculated whenever their value changes. For example, I can confidently use `a` without worrying about when its value changes. I don't need to re-run my check when `a1` and `a2` change because the library takes care of that.

It's all sunshine and rainbows from here on out, right? Well, it turns out that integrating `run` into other applications can be a little tricky. For one, it would be nice to cache changed variables until they can be written.
