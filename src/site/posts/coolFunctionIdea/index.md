---
title: Cool Function Idea
date: Oct 10, 2020
---

# Cool Function Idea

Alright, is mostly for my own brainstorming.

So I had an idea to make functions with extreme overloading capabilities. Like for classes, instead of calling a constructor, you would call `init(classType)` and the compiler would figure out which class to make based on the class type. But like there would be a bunch of definitions for `init`, one for each class and the compiler would figure out which to call based on the arguments.

Yeah, that's it in a sentence: Figure out which function definition to call based on the arguments.

This solves one of my pet peeves with C++, where you have to define a 'friend' function when overloading addition or other operators. It would be so much easier to make a new object like:
```c++
class MyAddableClass {
  value: int;
}

MyAddableClass add(MyAddableClass a, MyAddableClass b) {
  return MyAddableClass(a.value + b.value);
}
```

or something like that. But it would be really nice if function overloading was powerful enough to replace some other language constructs like classes.

And then I saw a video about the Julia programming language where they were talking about the fancy "dynamic dispatch" that enabled developers to easily re-use and extend existing libraries. This was awesome! I saw my idea being useful in another project.

So I spent the afternoon thinking about where to go from there, and this all ties into my idea of an OS/package manager/programming environment.

There are some key principals I'm thinking of:

### 1. Data and methods are separate
Data is defined to store information and methods operate on that data. Keeping data and methods also makes it easier to extend libraries because data and the methods operating on that data are decoupled. In the case of the Julia programming language, this makes it really easy to extend and modify existing libraries without subclassing or re-writing the source code.

### 2. Data and methods should be freed of their source files.
Text editors and files are a great way to develop, but they make it challenging to manipulate large numbers of objects and move programming projects around. Programming libraries and apps shouldn't be constrained to files - they should be free and queryable and fluid.

Imagine this: each data type and method has it's own definition. They exist in a module and can be written individually in a text editor, but they live independent of their source file. They can be compressed into a binary format. They can be compiled. They can be serialized to a single file. They can be statically analyzed. They can be traced to find dependencies between code elements.

```
Search for a function:
> add

Results:
add(int, int)
add(float, int)
add(int, float)
add(float, float)
add(vec, vec)
```

```
Make a new data type
name: RGB Color
fields:
  r: float
  g: float
  b: float

Make associated functions
init(RGB Color) {
  color = makeBlank(RGB Color)
  color.r = 0
  color.g = 0
  color.b = 0
  return color
}
init(RGB Color, r: float, g: float, b: float) {
  color = makeBlank(RGB Color)
  color.r = r
  color.g = g
  color.b = b
  return color
}

add(left: RGB Color, right: RGB Color) {
  r = left.r + right.r
  g = left.g + right.g
  b = left.b + right.b
  return init(RGB Color, r, g, b)
}
```
