const PI = Math.PI;

function positiveModulo(i, n) {
  return ((i % n) + n) % n;
}

function cross(O, A, B) {
  return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

function convexHull(points) {
  const n = points.length;
  let k = 0;
  if (n <= 3) {
    return points;
  }
  const H = [];

  // Sort points lexicographically
  points.sort((a, b) => {
    const dx = a.x - b.x;
    if (dx === 0) {
      return a.y - b.y;
    } else {
      return dx;
    }
  });

  // Build lower hull
  for (let i = 0; i < n; i++) {
    while (k >= 2 && cross(H[k - 2], H[k - 1], P[i]) <= 0) {
      k--;
    }
    H.push(P[i]);
    k++;
  }

  // Build upper hull
  for (let i = n - 1, t = k + 1; i > 0; --i) {
    while (k >= t && cross(H[k - 2], H[k - 1], P[i - 1]) <= 0) {
      k--;
    }
    H.push(P[i - 1]);
    k++;
  }

  return H;
}

class Fractal {
  constructor(base, lengths, iterations, mirrored) {
    this.base = base;
    this.lengths = lengths;
    this.iterations = iterations;
    this.mirrored = mirrored;

    this.d0 = 0;
  }

  setTurns() {
    let bl = this.base.length;
    let turns = bl;
    for (let i = 0; i < this.iterations; i++) {
      turns = bl + bl * turns + turns;
    }

    this.turns = turns;
    pr(`Fractal has ${this.turns} turns`);
  }

  setPoints() {
    this.points = [{ x: 0, y: 0 }];
    let dir = this.d0;
    let x = 0;
    let y = 0;

    const baseSize = this.base.length + 1;
    for (let i = 0; i < this.turns; i++) {
      let turnN = i;
      while (turnN % baseSize === 0) {
        turnN = Math.round(turnN / baseSize);
      }
      if (this.mirrored) {
        if (Math.floor(turnN/baseSize) % 2 === 0) {
          dir += 
        }
      }
    }
  }
}
