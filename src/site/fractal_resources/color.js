const Color = {
  intToHex(i) {
    i = Math.round(i);
    i = Math.min(i, 255);
    i = Math.max(i, 0);
    const hex = i.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  },
  rgbToHex(c) {
    return '#' +
      Color.intToHex(c.r) +
      Color.intToHex(c.g) +
      Color.intToHex(c.b);
  },
  hexToRgb(c) {
    // #ABCDEF
    return {
      r: parseInt(c.substring(1,3), 16),
      g: parseInt(c.substring(3,5), 16),
      b: parseInt(c.substring(5,7), 16),
    }
  },
  rising(v) {
    return 255*v;
  },
  falling(v) {
    return Color.rising(1-v);
  },
  getPrimaryColor(a) {
    // clamp to [0,1)
    a -= Math.floor(a);

    const res = {};

    const section = Math.floor(6*a);
    const val = 6*a - section;

    switch(section) {
    case 0:
        res.r = 255;
        res.g = Color.rising(val);
        res.b = 0;
        break;
    case 1:
        res.r = Color.falling(val);
        res.g = 255;
        res.b = 0;
        break;
    case 2:
        res.r = 0;
        res.g = 255;
        res.b = Color.rising(val);
        break;
    case 3:
        res.r = 0;
        res.g = Color.falling(val);
        res.b = 255;
        break;
    case 4:
        res.r = Color.rising(val);
        res.g = 0;
        res.b = 255;
        break;
    case 5:
        res.r = 255;
        res.g = 0;
        res.b = Color.falling(val);
        break;
    }

    return res;
  },
  linColor(c0, c1, a) {
    if (a > 1) a = 1;
    let res = {};
    res.r = c0.r*(1-a) + c1.r*a;
    res.g = c0.g*(1-a) + c1.g*a;
    res.b = c0.b*(1-a) + c1.b*a;
    return res;
  },
};
