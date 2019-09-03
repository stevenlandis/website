---
title: Declarative Baking
date: 9-3-2019
author: Steven Landis
---

I recently had a summer internship where I had to use a lot of React. It was eye opening because I learned how awesome declarative app design is and how much easier it makes my life.

Over those weeks I also learned that there are improvements to React in terms of abstracting its logic and making it easier to make all aspects of an application declarative instead of just the rendering logic.

As I was busy staring at walls deep in thought, my mom asked me what I was thinking about. After a few minutes of mentally stumbling around how to explain my crazy thoughts, I inevitably went back to cooking as a metaphor for programming. Cooking is an activity that everyone relates to and it's very similar to programming which makes it great for metaphors.

Let's say you want to bake a cake and it has the following recipe. In this example the amounts of each ingredient don't really matter, it's more about how the ingredients are combined.

```
Ingredients:
- flour
- baking soda
- sugar
- salt
- milk
- eggs
- vanilla

Instructions:
 1. Combine dry ingredients in a bowl.
 2. Combine wet ingredients in another bowl.
 3. Whisk together wet and dry ingredients.
 4. Bake the mixture and enjoy!
```

I'm sure I missed some important steps but the general idea is there.

So, here's the problem. You bake a cake, but after, you decide you want to use whole milk instead of low-fat milk. Being a smart human being, you don't re-bake the entire cake. You still have some leftover dry ingredients mixed together so you just re-mix the wet ingredients with different milk, whisk wets and drys together, and bake another cake.

Here are some cool observations:

- You didn't have to repeat the entire recipe when you changed the milk.
- The finished cake is identical to if you had re-done the entire recipe.
- The recipe writer didn't have to describe how to efficiently re-make a cake. You figured that out on your own.

This is the magic of declarative programming. You, the programmer, write a 'recipe' that is rendered as an application. The application framework's job is to figure out efficient ways to change the application *as though it completely re-ran with changed 'ingredients'*.