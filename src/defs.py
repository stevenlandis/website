def file(fName):
    with open(fName,'r') as f: print(f.read(),end='')

def code(fName, syntax):
    res = f'<pre><code class="{syntax}">'
    with open(fName,'r') as f: res += f.read()
    res += '</code></pre>'
    print(res)