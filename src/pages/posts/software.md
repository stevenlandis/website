---
title: My Software Philosophy
---

## All Software Sucks

Including my own, I just feel the shortcomings of third-party software the most when I use other people's software. There is always a case where I want to do something the library doesn't support.

With that in mind I'm trying to write software a different way. By providing basic building blocks for developers, I let them write their own libraries instead of forcing them to use my library.

I like the idea behind Window's [approach to rendering text](https://docs.microsoft.com/en-us/windows/win32/direct2d/direct2d-and-directwrite) because they support "incremental adoption" where developers can use different APIs depending on how much control they want over text position. While I don't think Windows implemented incremental adoption well, I like their intention.

Providing basic building blocks makes it easy for developers to flexibly use a library. It also means, as I am not omnipotent, that other developers can easily swap out one section of my code with another without re-writing the library.

Another reason why using third party libraries is hard is the learning curve. A library is, in a way, a language. It's a collection of functions and classes allowing developers to write readable code while the library implements that code efficiently. It's weird to think that programming languages go deeper than python or C. The style of any program also depends as much on the language as the libraries it uses.

Good library design means thinking critically about how the code will be used and figuring out how to express a solution within a programming language.