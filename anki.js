// /[\u4e00-\u9fa5]|[\（\）\《\》\——\；\，\。\“\”\<\>\！]/g
// /[^\x00-\xff]/igm
// [^\u4e00-\u9fa5\uff00-\uffef]
let fs = require('fs');
let path = require('path');
let media_dir = "/Users/leo/Library/Application Support/Anki2/leo/collection.media"
let anki_file = 'anki.csv'
async function anki() {
    let dir = process.cwd();
    let allFiles = fs.readdirSync(dir);

    let files = allFiles.filter((file, index, array) => {
        return path.extname(file) == '.lrc'
    });

    let i = 0;
    for (let file of files) {
        i += 1;

        let newName = new Date().getTime() + '.' + i

        let inputFile = dir + '/' + file;
        let outFile = dir + '/anki.csv';

        if (fs.statSync(inputFile).isFile()) {
            if (path.extname(file) != '.lrc' && path.extname(file) != '.mp3') {
                continue;
            }
            await lrcHander(inputFile, dir + '/' + anki_file, newName).catch((err) => { console.log(err) })
        }

        let newLrcFile = dir + '/' + newName + path.extname(file)
        let oldMp3File = dir + '/' + path.basename(file, '.lrc') + '.mp3'
        let newMp3File = dir + '/' + newName + '.mp3'
        await rename(inputFile, newLrcFile)
        await rename(oldMp3File, newMp3File)
        copy(newMp3File, media_dir + '/' + newName + '.mp3')
    }
}

async function copy(src, dist) {
    return new Promise((resolve, reject) => {
        fs.stat(src, (err, st) => {
            if (err) {
                reject(err)
            } else {
                if (st.isFile()) {
                    let writer = fs.createWriteStream(dist);
                    writer.on('finish', () => {
                        resolve()
                    });
                    fs.createReadStream(src).pipe(writer);
                }
            }
        })
    })
}

async function rename(oldPath, newPath) {
    return new Promise((resolve, reject) => {
        fs.rename(oldPath, newPath, function (err) {
            if (err) {
                throw err;
            } else {
                resolve();
            }
        });
    })
}

async function lrcHander(inputFile, outputFile, audioName) {
    return new Promise((resolve, reject) => {
        let extname = path.extname(inputFile)
        if (extname == '.lrc') {
            var exec = require('child_process').exec;
            exec('enca -L zh_CN -x UTF-8 "' + inputFile + '"', function (err, stdout, stderr) {

                let content = fs.readFileSync(inputFile).toString();
                // let content = "[00:00.00]I remember when I was pregnant with Richard Philip and were living with Grandma and Grandpa. Philip was a young doctor, and he kept talking about having a house of our own. It's natural.		我还记得我怀理查德的时候。那时菲利普和我跟你爷爷和奶奶住在一起。菲利普是个年轻的医生，他老是说要有一所我们自己的房子。这是很自然的事。"
                content = content.replace(/\[00:00.00\]/, '')
                let english = content.match(/[\x00-\xff]/igm).join('').trim();
                let chinese = content.match(/[^\x00-\xff]/igm).join('').trim();
                let audio = "[sound:" + audioName + ".mp3]"
                let result = english + '|' + chinese + '|' + audio + '|Note:' + '\n'

                if (err) {
                    reject(err)
                } else {
                    fs.writeFile(outputFile, result, { flag: 'a+' }, function (err) {
                        if (err) {
                            reject(err)
                        } else {
                            resolve()
                        }
                    })
                }
            });
        } else {
            resolve()
        }
    })
}

anki()