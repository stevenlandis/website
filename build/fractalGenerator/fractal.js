const PI = Math.PI;

function positiveModulo(i, n) {
  return ((i % n) + n) % n;
}

function cross(O, A, B) {
  return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0]);
}

function convexHull(points) {
  // copy points
  points = points.slice();

  const n = points.length;
  let k = 0;
  if (n <= 3) {return points;}
  const H = new Array(2*n);

  // Sort points lexicographically by x then y
  points.sort((a, b) => {
    const dx = a[0] - b[0];
    if (dx === 0) {
      return a[1] - b[1];
    } else {
      return dx;
    }
  });

  // Build lower hull
  for (let i = 0; i < n; i++) {
    while (k >= 2 && cross(H[k-2], H[k-1], points[i]) <= 0) {
      k--;
    }
    H[k++] = points[i];
  }

  // Build upper hull
  for (let i = n-1, t = k+1; i > 0; --i) {
    while (k >= t && cross(H[k-2], H[k-1], points[i-1]) <= 0) {
      k--;
    }
    H[k++] = points[i-1];
  }

  return H.slice(0, k-1);
}

const Fractal = {
  getTurns(nAngles, iterations) {
    let turns = nAngles;
    for (let i = 0; i < iterations; i++) {
      turns = nAngles + nAngles*turns + turns;
    }
    return turns;
  },
  getTurnI(baseSize, mirrored, i) {
    while (i % baseSize === 0) {
      i /= baseSize;
    }
    if (mirrored) {
      if (Math.floor(i/baseSize) % 2 === 0) {
        return i % baseSize;
      } else {
        return -(baseSize - i % baseSize);
      }
    } else {
      return i % baseSize;
    }
  },
  getLengthI(baseSize, mirrored, i) {
    if (mirrored) {
      if (Math.floor(i/baseSize) % 2 === 0) {
        return i % baseSize;
      } else {
        return baseSize - i%baseSize - 1;
      }
    } else {
      return i % baseSize;
    }
  },
  getPoints(base, lengths, mirrored, d0, turns) {
    const points = [];
    let dir = d0;
    points.push([0, 0]);
    let x = 0;
    let y = 0;

    let sinTable = [];
    let cosTable = [];
    for (let i = 0; i < 360; i++) {
      sinTable[i] = Math.sin(i*PI/180);
      cosTable[i] = Math.cos(i*PI/180);
    }

    let baseSize = base.length + 1;
    for (let i = 1; i <= turns; i++) {
      const lengthI = Fractal.getLengthI(baseSize, mirrored, i-1);
      const len = lengths[lengthI];
      x += len * cosTable[dir];
      y += len * sinTable[dir];
      points.push([x, y]);

      const turnI = Fractal.getTurnI(baseSize, mirrored, i);
      if (turnI < 0) {dir -= base[-turnI - 1];}
      else {dir += base[turnI - 1];}
      dir = positiveModulo(dir, 360);
    }

    const lengthI = Fractal.getLengthI(baseSize, mirrored, turns);
    const len = lengths[lengthI];
    x += len * cosTable[dir];
    y += len * sinTable[dir];
    points.push([x, y]);

    return points;
  },
  getOptimalAngleOffset(points) {
    hull = convexHull(points);
    const N = hull.length;
    hull.push(hull[0]);

    let minDotRange = Infinity;
    let minDotI = -1;

    for (let i = 0; i < N; i++) {
      const p0 = hull[i];
      const p1 = hull[i+1];

      let minDot = Infinity;
      let maxDot = -Infinity;

      const dx = p1[0] - p0[0];
      const dy = p1[1] - p0[1];

      const l = Math.sqrt(dx*dx + dy*dy);

      // get x and y parts of perpendicular unit vector
      const ux = -dy/l;
      const uy = dx/l;

      // get min and max dot product between u and each point
      for (let j = 0; j < N; j++) {
        const dot = hull[j][0]*ux + hull[j][1]*uy;

        if (dot < minDot) {minDot = dot;}
        if (dot > maxDot) {maxDot = dot;}
      }

      const dotRange = maxDot - minDot;
      if (dotRange < minDotRange) {
        minDotRange = dotRange;
        minDotI = i;
      }
    }

    // now, calculate optimal edge angle
    const p0 = hull[minDotI];
    const p1 = hull[minDotI+1];

    const dx = p1[0] - p0[0];
    const dy = p1[1] - p0[1];

    let angle = Math.atan2(dy, dx);
    return -angle;
  },
  getRotatedPoints(points, angle) {
    // Rotation matrix:
    // [a, b]
    // [c, d]
    let a = Math.cos(angle);
    let b = -Math.sin(angle);
    let c = Math.sin(angle);
    let d = Math.cos(angle);

    return points.map(p => [
      p[0]*a + p[1]*b,
      p[0]*c + p[1]*d
    ]);
  },
  getBounds(points) {
    let minX = Infinity;
    let maxX = -Infinity;
    let minY = Infinity;
    let maxY = -Infinity;

    for (const [x, y] of points) {
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
    }

    return {minX, maxX, minY, maxY};
  },
  getScaledPoints(points, width, height, padding) {
    const {minX, maxX, minY, maxY} = Fractal.getBounds(points);
    let wf = maxX - minX;
    let hf = maxY - minY;

    let wi = width;
    let hi = height;

    let scale, shiftX, shiftY;
    if (hf*wi > hi*wf) {
        // vertical constraint
        scale = hi/hf * (1-2*padding);
        shiftY = hi*padding - scale*minY;
        shiftX = (wi - scale*(minX+maxX))/2;
    } else {
        // horizontal constraint
        scale = wi/wf * (1-2*padding);
        shiftX = wi*padding - scale*minX;
        shiftY = (hi - scale*(minY+maxY))/2; 
    }

    return points.map(([x,y]) => [
      x*scale + shiftX,
      y*scale + shiftY
    ]);
  }
}
