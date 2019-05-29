all:
	python build.py
	chrome site\index.html
# 	chrome site\testDir\test.html

push:
	git subtree push --prefix site origin gh-pages