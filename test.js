let content = '[00:12.40]Dear Sally...you should probably be sitting down for this.		亲爱的Sally，你最好还是坐下来听我说'
content = content.replace(/\[\d\d:\d\d.\d\d\]/, '')
let values = content.split('\t\t')
// let english = content.match(/[\x00-\xff]/igm).join('').trim();
// let chinese = content.match(/[^\x00-\xff]/igm).join('').trim();
let english = values[0].trim()
let chinese = values[1].trim()
console.log(english)
console.log(chinese)