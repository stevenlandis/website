from src.parser.parser import Parser, T, L, R

def isWs(char):
  # normal whitespace
  return char in [' ', '\t', '\r']

def isMWs(char):
  # Multiline whitespace
  return char in [' ', '\t', '\r', '\n']

def isAlpha(char):
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'

def isDigit(char):
    return '0' <= char <= '9'

def isAlphanumeric(char):
    return isAlpha(char) or isDigit(char)

def R_ws(parser):
  # normal whitespace
  while True:
    char = parser.peek()
    if not isWs(char): break
    parser.step()
  return True, None

def R_mws(parser):
  # multiline whitespace
  while True:
    char = parser.peek()
    if not isMWs(char): break
    parser.step()
  return True, None

def R_nl(parser):
  while True:
    char = parser.peek()
    if char == None: return False, None
    parser.step()
    if char == '\n': return True, None

def R_preKey(parser):
  char = parser.peek()
  if char == None or char in [':', ' ', '\t', '\r', '\n']:
    return False, None
  i0 = parser.i
  parser.step()

  while True:
    char = parser.peek()
    if char == None or char in ['\t', '\r', '\n']:
      return False, None
    parser.step()
    if char == ':':
      return True, parser.getRange(i0, parser.i-1)

def R_singleQuote(parser):
  if parser.peek() != "'": return False, None
  parser.step()
  i0 = parser.i
  while True:
    char = parser.peek()
    if char == None: return False, None
    parser.step()
    if char == "'":
      return True, parser.getRange(i0, parser.i-1)

def R_doubleQuote(parser):
  if parser.peek() != '"': return False, None
  parser.step()
  i0 = parser.i
  while True:
    char = parser.peek()
    if char == None: return False, None
    parser.step()
    if char == '"':
      return True, parser.getRange(i0, parser.i-1)

def R_preQuote(parser):
  good, val = parser.parse(R_singleQuote)
  if good: return good, val

  good, val = parser.parse(R_doubleQuote)
  if good: return good, val

  return False, None

def R_preValue(parser):
  good, val = parser.parse(R_preQuote)
  if good: return good, val

  i0 = parser.i
  while True:
    char = parser.peek()
    if char == None: return False, None
    if char == '\n':
      return True, parser.getRange(i0, parser.i)
    parser.step()

def R_preEntry(parser):
  good, key = parser.parse(R_preKey)
  if not good:
    return False, None

  parser.parse(R_mws)

  good, val = parser.parse(R_preValue)
  if not good:
    return False, None

  return True, (key, val)

def R_inlineCode(parser):
  char = parser.peek()
  if char == None or char != '`':
    return False, None
  parser.step()

  i0 = parser.i
  while True:
    char = parser.peek()
    if char == None or char == '\n':
      return False, None
    parser.step()
    if char == '`':
      break
  return True, parser.getRange(i0, parser.i-1)

def R_italic(parser):
  char = parser.peek()
  end = None
  if char == '*': end = '*'
  elif char == '_': end = '_'
  else: return False, None 
  parser.step()
  i0 = parser.i
  while True:
    char = parser.peek()
    if char == None: return False, None
    parser.step()
    if char == end:
      break
  return True, parser.getRange(i0, parser.i-1)

def R_bold(parser):
  end = None
  if parser.parse('**'): end = '**'
  elif parser.parse('__'): end = '__'
  else: return False, None

  i0 = parser.i
  while True:
    if parser.parse(end):
      break
    char = parser.peek()
    if char == None:
      return False, None
    parser.step()
  return True, parser.getRange(i0, parser.i-2)

def R_header(parser):
  n = 0
  while True:
    char = parser.peek()
    if char == None or char == '\n':
      return False, None
    if char == '#':
      n += 1
      if n > 6: return False, None
      parser.step()
    else:
      break
  if n == 0: return False, None
  parser.parse(R_ws)

  good, val = parser.parse(R_text)
  if good:
    return True, (n, val)

def parseMd(txt):
  parser = Parser(txt)
  parser.parse(R_mws)

  good, _ = parser.parse(T('---'))
  pre = []
  if good:
    # parse the preamble
    while True:
      parser.parse(R_mws)
      
      good, _ = parser.parse(T('---'))
      if good: break

      good, val = parser.parse(R_preEntry)
      if not good:return False, None
      pre.append(val)

  content = []
  parser.parse(R_mws)
