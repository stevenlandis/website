---
title: My Software Philosophy
---

## All Software Sucks

Including my own, I just feel the shortcomings of third-party software the most when I use other people's software. There is always a case where I want to do something the library doesn't support.

With that in mind I'm trying to write software a different way. By providing basic building blocks for developers, I let them write their own libraries instead of forcing them to use my library.

All software involves restricting what a developer can do. Some examples include [React](https://reactjs.org/) which forces developers to write hierarchical UIs and [Redux](https://redux.js.org) which forces developers to never modify data structures in place.

For the most part, these libraries have restrictions that don't chafe too much which is the sign of good design. Those developers must have spent a lot of time thinking about use cases and determined that the above restrictions don't stop other developers from expressing their ideas.

Another reason why using third party libraries is hard is the learning curve. A library is, in a way, a language. Its collection of functions and classes hopefully let a developer write code that is readable while the library implements that code efficiently. It's weird to think programming languages go deeper than python or C. The style of any program also depends as much on the language as the libraries it uses.