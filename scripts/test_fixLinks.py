from fixLinks import fixLinks

fixed = fixLinks('''
<DOCTYPE! html>
<html>
<head>
  <title        stuff="things" things>
</head>
<body>
  <a style="stuff" href="stuff/things">This is some content</a>
</body>
</html>
''')
print(fixed)
