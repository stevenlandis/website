class Parser:
  def __init__(self, txt):
    self.txt = txt
    self.i = 0
    self.lineN = 1
  def getState(self):
    return (self.i, self.lineN)
  def setState(self, state):
    self.i, self.lineN = state
  def peek(self, offset=0):
    if self.i + offset >= len(self.txt):
      return None
    return self.txt[self.i+offset]
  def step(self):
    if self.peek() == '\n': self.lineN += 1
    self.i += 1
  def getRange(self, lo, hi):
    return self.txt[lo:hi]
  def parse(self, rule):
    if type(rule) == str: return self.parseStr(rule)
    state = self.getState()
    good, val = rule(self)
    if not good:
      self.setState(state)
    return good, val
  def parseStr(string):
    if self.i + len(string) >= len(self.txt):
      return False
    for off in range(len(string)):
      if self.txt[self.i + off] != string[off]:
        return False
    self.i += len(string)
    return True

def T(string, eq=lambda a,b: a==b):
  def helper(parser):
    for char in string:
      c = parser.peek()
      if c == None or not eq(char, c):
        return False, None
      parser.step()
    return True, None
  return helper

def L(*rules):
  def helper(parser):
    res = []
    for rule in rules:
      good, val = parser.parse(rule)
      if not good:
        return False, None
      res.append(val)
    return True, res
  return helper

def R(rule):
  def helper(parser):
    res = []
    while True:
      i0 = parser.i
      good, val = parser.parse(rule)
      if not good or i0 == parser.i:
        break
      res.append(val)
    return True, res
  return helper
