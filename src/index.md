# CS56 Lab Simplification
I found the [normal lab](https://ucsb-cs56.github.io/s19/lab/lab05/) to be too confusing to easily read so I made this guide to help me understand the lab.

## Pair Programming
Read the website, it's the same as always.

## Introduction
Message board applications let users post messages and reply to messages. This lab will not have a user interface, just a library.

## Tags
Posts have tags that summarize their content. A post about food might have a `food` tag. Users can subscribe to tags and recieve updates whenever a post with a tag is posted.

Tags are always given as alphanumeric and case insensitive. I think tags should be their own class but they are stored as strings in this lab so make sure to call `.toLowerCase()`. 

## Subject-Observer Pattern
Before getting into how the classes are defined, I'll describe some interfaces that enable this pattern.

```java
interface Observer {
    public void update(Post post);
}
```

```java
interface Subject {
    public void registerUserTag(String tag, User user);
    public void removeUserTag(String tag, User user);
    public void notifyUsers(Post p);
}
```

`User` objects implement `Observer` because they observe and `MessageBoardManager` objects implement `Subject` because they are observed.

## Posts
Posts have the following properties:
```
tags: ArrayList<String>
message: String
replies: ArrayList<Post>
id: Integer
 - a unique Post ID assigned on post creation.
 - I used a static variable to keep track of this ID.
parentID:
 - non-reply posts have parentID = -1
user: User
 - User who made the post

```
Child posts inherit tags from their parents.

And the following methods:
```java
public ArrayList<String> getTags() {return tags;}
public int getPostID() {return id;}
public String toString(); // useful for printing
```

## Users
`implements Observer`

Users have the following properties:
```
id: Integer
 - Similar to postID, unique integer for every user
tags: ArrayList<String>
posts: ArrayList<Post>
```
And the following method:
```java
// displays a stub-like message saying the user was notified
// inherited from Observer
public void update(Post p)
```

## MessageBoardManager
`implements Subject`

MessageBoardManagers have the following methods. It's up to the programmer to implement necessary properties.
```java
public void addPost(Post p)
public void addReply(Post reply)
public void displayTagMessages(String tag)
public void displayKeywordMessages(String keyword)
public void displayThread(int postID)
public void displayUserPosts(User user)
public void registerUserTag(String tag, User user)
public void removeUserTag(String tag, User user)
public void notifyUsers(Post p)
```