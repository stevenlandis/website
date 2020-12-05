---
title: bld2
date: Jan 11, 2020
---

## Motivation

This website is a static website that I built from scratch. That means I had to build my own static website generator which led me to create a project building library for incremental builds called bld (short for build).

However, I wasn't pleased with how my project builder was scaling and I didn't like the complexity of adding new rules. The real benefit of bld was its wrapper functions for common project building actions rather than its syntax for indicating project structure. The `File` and `Dir` objects made it really easy to create complex file structures in little code and the `bld.call` function made it easy to call building commands.

Some of the features such as directory merge/remove actions weren't as useful as I originally thought.

In summary, bld had some unnecessary features and the code wasn't easy to read.

## bld2

The original bld takes a functional approach to creating projects: the programmer specifies the dependency structure for their project and bld figures out how to accomplish that structure.

I ended up making bld2 more imperative where the programmer indicates *how* to build the project. And it all comes down to one function:

```
shouldUpdate(sourceFiles, resultFiles)

sourceFiles: array of File objects or paths
resultFIles: array of File objects or paths
```

Let's say I have `main.c` and I want to compile it into the executable `main` using `shouldUpdate`:

```py
if shouldUpdate(['main.c'], ['main']):
    bld.call('gcc main.c -o main')
```

Rather than creating complex subclassed `Rule` objects for each build step, this syntax clearly shows *how* bld2 executes the program and saves the programmer a few lines of code.

However, there are a few features that can't be implemented because of this change:

- Multithreading: bld2 can no longer create a task queue and distribute building steps on multiple processors because it can't reason about dependency. This feature wasn't implemented in bld, but that feature is no longer possible.
- Automatic clean function: bld2 can no longer automatically remove created files. However, now that I think about it, programmers can just store a list of all created files and remove the files from that list on clean. Having a list of created files would also be useful for obsolete files. I like this better.

And that's the thing. The more I think about functionality that gets lost in the transition from imperative to functional, the more solutions I find. I guess it's easier to build a functional system atop an imperative system than the other way around.

The best guarantee for a partial-building system is the output is identical to if the project was build from scratch for the first time. It is very functional because the programmer just describes what they want the output to look like and not how to achieve that output. What, not how.

One common issue with build systems is leftover files. For example, if you compile

```
gcc main.c -o main
```

once, you have `main` in your directory. However, if you want to change the executable's name to `myExecutable`, you would simply run

```
gcc main.c -o myExecutable
```

The issue is that your directory still has the leftover `main` executable which would not happen if the programmer built the project from scratch.

The easiest way to fix this issue is for `bld` to keep track of which files it has currently written, called `currentFiles`. When the build script runs, `bld` can keep track of all written files by listening to calls to `shouldUpdate`. This creates another set of files called `nextFiles`. All files in `currentFiles` that are not in `nextFiles` should be deleted.

### Example

Initial directory:

```
testDir
--build.py
--main.c
```

Initial `build.py`:

```py
if shouldUpdate('main.c', 'main'):
    bld.call('gcc main.c -o main')
```

Directory after building:

```
testDir
--build.py
--main.c
--main
--currentFiles
```

And current files is a simply the following text file:

```
main
```

You then change `build.py` to the following:

```py
if shouldUpdate('main.c', 'main'):
    bld.call('gcc main.c -o myExecutable')
```

During the build, `currentFiles` is `[main]` and `nextFiles` is `[myExecutable]` which means bld deletes `main`.

Directory after building the second time:

```
testDir
--build.py
--main.c
--myExecutable
--currentFiles
```

And currentFiles is now the following text file:

```
myExecutable
```

A nice side effect of keeping a list of current files is that clean operations can be done automatically. Cleaning this directory means removing all non-essential files which removes all files in currentFiles and then removes currentFiles.

## What about directories?

The one thing I overlooked in that example is directories. The easiest way to handle them is to keep track of all directories that had files removed from them. At the very end of the build process, the script checks those directories to see if any are empty and repeats the process until all directories have at least one thing in them. This is a similar approach to Github which doesn't support empty directories and instead focuses only on files which makes sense for projects because files are the only source of truth in a project. There is never a situation where project information is stored in a directory. As such, empty directories probably shouldn't exist.

But what is someone wants directories to exist? There may be a way to tell bld to keep track of directories and not delete some empty directories.

## Why it is challenging to use

In a world where command-line-commands only write one file, this setup works really well. But consider the command `python` which runs a python file which can import any number of files. It suddenly becomes very challenging to track which files have been touched and which files need to be changed.

This leads to a compromise for writing efficient build systems with bld2:
- if the command is simple like copying a file, use `shouldUpdate`.
- if the command is complex like using a python script to generate a website, run the calculation each time.

In practice this works pretty well: This site takes 5s to build from scratch and 0.7s to re-build. The main time sync is converting a bunch of images from .png to .jpg which is easy to run only when necessary with `shouldUpdate`.
