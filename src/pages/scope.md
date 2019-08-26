---
title: Scope Based Programming
---

## The Problem
I was recently writing some software with a lot of densely connected data structure.

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

## The Intuition

## The Language