---
title: "bld: Replacing Make"
---

# Make is amazing

Seriously. Make lets you build files incrementally while expressing complex build rules with an efficient syntax. It also lets you define custom commonly-used commands for a project which makes building and cleaning much easier.

The only downside is that Make is not a complete scripting language. I'm a pretty lazy person, so it was hard for me to learn the syntax of advanced rules and I ran into a few cases where I wanted to build my project in a way that Make didn't allow.

This is my motivation for bld. I want it to be a library that makes it easy to write files to build a project in python. Python is a great scripting languages with lots of libraries and it has a very clear syntax which makes it ideal for connecting different commands together into a build system.

# The Test
To test how well my building library works, I made a static website generator and tested how easy it was to implement building features. If you are reading this website, then the test worked!

## Goals
- Write a `build.py` file that creates a website.
- Get incremental builds to work.
- Get live building to work.

I'm currently able to build a website, but incremental builds don't work. It turns out that python files can import other python files which means the incremental builder needs to read files to find dependencies. This should be a simple regex to extract imported files but it will make the builder much slower because it has to read through a lot of python files.

There are three ways around this:

1. Get the build file to generate a static 'plan' for building the current project. It will be expensive to make this plan but running the plan is cheap. This assumes that most file changes only involve changing files and not creating new files or changing imports. I also have to re-generate the plan manually.

2. Get live building to work. This is the best solution but I really don't want to deal with watching a file. Yet. It is an eventual goal and will make my life a lot easier but it is a complex addition to this library and I need to think about how it will work.

3. Each file has a 'import' file in a temp directory that stores it's imports. This seems like a good neutral option because it makes it possible to do make-style incremental builds and keeps the expense of each run low. It does add a little more memory to the project.

# The Building Blocks: Navigating the File System

A key part of writing a build system is finding the files to build. For this website, I have a folder `pages/` with a bunch of files that define a page. Some pages that need custom control are a python file and other pages, such as this one, are a single markdown file with some meta-data.

This means bld.py has to recursively look through the contents of `pages/`. When it finds a python file, it runs that python file and saves the resulting string as an html file. When it finds a markdown file, it parses that file as markdown, highlights the corresponding code sections and saves that as html.

## Virtual And Disk Files and Directories

This library provides all that functionality using two base objects, `DiskDir / DiskFile` and `VirDir / VirFile`. Disk objects are files and directories that actually exist on the disk and Vir objects are virtual files and directories that will be built (placed) during the build process. 

These disk and virtual file objects make it easier to navigate and manipulate files and directories.

It all starts with getting the `pages/` directory:

```python
pageDir = bld.DiskDir('src/pages')
```

The output will be stored in the `build/` directory and this is represented as a virtual directory that will be populated with files during the build process:

```python
buildDir = bld.VirDir('build')
```

At this point, if I wanted to write `'Hello World'` to `build\test.txt`, I could use the following code:

```python
text = 'Hello World'

# testFile is a VirFile
testFile = buildDir.getFile('test.txt')

# place the output directory
buildDir.place('.')

# write the file
testFile.write(text)
```

I could then use this structure to build my whole project and I would be done. However, I only want to build the bare minimum number of files each time and I don't want to re-build `test.txt` if its contents don't change.

## Rules

This is where rules come in. `Rule` is a class that can be sub-classed to create custom rules for building files. A rule has three parts:

1. Input files
2. Output files
3. Some function to build the output files from input files

Because a rule declares which files it depends on before running, `bld` checks the write time of the input files before running each rule which means **each rule runs only when it needs to run**.

In the previous example, I could replace the code with a rule for writing `'Hello World'` with a rule:

```python
class HelloWorldRule(bld.Rule):
    def __init__(self, outFile):
        self.init()

        # add single input file
        self.addOut(outFile)
    def run(self):
        # print some text so we can see if the rule runs
        print(f'Writing HelloWorld to {self.outputs[0].name}')

        text = 'Hello World'
        self.outputs[0].write(text)
```

And call it like:

```python
buildDir = bld.VirDir('build')
testFile = buildDir.getFile('test.txt')
HelloWorldRule(testFile)

buildDir.build('.') # automatically runs HelloWorldRule the first time
```

When I start out, my file structure looks like this:

```
./
    build.py
```

I then run `build` for the first time

```
>>> build
Writing HelloWorld to test.txt
>>>
```

Then, my file structure looks like this:
```
./
    build.py
    build/
        test.txt
```

It even made the folder `build/` so `text.txt` has a place to live!

When I run `build` again, the real magic happens:

```
>>> build
>>>
```

Nothing! That's right, `Rule` automatically detects that `test.txt` already exists and doesn't run the rule again.

## Rule Inputs

That's a cool example, but what if I want a file to depend on another file? This is where the input part of rules comes into play.

The simplest rule that takes another file as input is the copy rule which is included in `bld`, but I'll make a copy here:

```python
class CopyRule(bld.Rule):
    def __init__(self, inFile, outFile):
        self.init()
        self.addIn(inFile)
        self.addOut(outFile)
    def run(self):
        [inFile] = self.inputs
        [outFile] = self.outputs
        outFile.write(inFile.read())
```

Yep, it's really that simple. I can use this rule to build the project as follows:

```
Before:
./
    copyMe.txt

After:
./
    copyMe.txt
    copiedMe.txt
```

And the `build.py` file:

```python
copyMe = bld.DiskFile('copyMe.txt')
copiedMe = bld.VirFile('copiedMe.txt')
CopyRule(copyMe, copiedMe)

# run the rule
copiedMe.build('.')
```