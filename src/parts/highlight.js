const hljs = require('highlight.js')
const fs = require('fs')

function highlight() {
    const txt = fs.readFileSync('src\\parts\\temp.txt', {encoding: 'utf8'})
    const firstNL = txt.indexOf('\n')
    if (firstNL === -1) {
        throw new Error('temp.txt needs to have at least two lines')
    }
    const language = txt.substring(0, firstNL);
    const code = txt.substring(firstNL + 1, txt.length)

    const hlText = language === 'None'
      ? code
      : hljs.highlight(language, code).value

    fs.writeFileSync('src\\parts\\temp.txt', hlText)
}

highlight()