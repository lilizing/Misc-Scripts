#-*-coding:utf-8-*-
"""
My first python program
"""
import re
import os
import sys
import csv
import glob
import time

reload(sys)
sys.setdefaultencoding("utf8") 

output = "import.csv"
media_dir = "/Users/leo/Library/Application Support/Anki2/leo/collection.media"

def copyFiles(sourceDir,  targetDir):
    for file in os.listdir(sourceDir): 
        if os.path.splitext(file)[1] == ".csv":
            continue
        sourceFile = os.path.join(sourceDir,  file) 
        targetFile = os.path.join(targetDir,  file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                    open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            First_Directory = False 
            copyFiles(sourceFile, targetFile)
  
def GetChinese(str):  
    line = str.strip().decode('utf-8', 'ignore')  # 处理前进行相关的处理，包括转换成Unicode等  
    p2 = re.compile(ur'[^\u4e00-\u9fa5\uff00-\uffef]')  # 中文的编码范围是：\u4e00到\u9fa5，中文标点符号范围是：\uff00-\uffef
    zh = "".join(p2.split(line)).strip() 
    return zh

def GetEnglish(content):
    value = content.strip().decode('utf-8', 'ignore')
    m = re.match(ur'([^\u4e00-\u9fa5])*', value)
    return m.group().strip()[11:]
    
def Main():
    curpath = os.getcwd()
    lrcfiles = curpath + "//*.lrc"
    flist = glob.glob(lrcfiles)
    writer = csv.writer(file(output, 'wb+'))
    pattern1 = re.compile(r'00]([\s\S]*) \r')

    # originCode = 'UTF-8'
    # if len(sys.argv) > 1:
    #     originCode = sys.argv[1]
    # print "***********原编码：" + originCode + "***********"

    i = 0
    for f in flist:
       i = i + 1

       newname_prefix = str(time.time()) + str(i)

       print "***********step1: 转码、提取中英文***********"
       newF = newname_prefix + '.lrc'
        #    os.system('iconv -f ' + originCode + ' -t UTF-8 "' + f + '" > "' + newF + '"')
        #    os.remove(os.path.join(curpath, f))
       
       os.system('enca -L zh_CN -x UTF-8 "' + f + '"')

       fh = file(f,'rw')
       content = fh.read()

       english = GetEnglish(content)
       chinese = GetChinese(content)

        #    print content
        #    print english
        #    print chinese
       
       print "***********step2: 重命名文件名***********"
       os.rename(f, newF)

       mp3file = f[:-3] + "mp3"
       newname = newname_prefix + ".mp3"
       
       os.rename(mp3file, newname)
       audio = "[sound:" + newname +"]"

       writer.writerow([audio, english, chinese])
       
       fh.close()

    del writer

    print "***********step3: 复制文件到媒体库***********"
    copyFiles(os.getcwd(), media_dir)
    


if __name__ == "__main__":
    Main()
    