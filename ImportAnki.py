#-*-coding:utf-8-*-
"""
My first python program
"""
import re
import os
import sys
import csv
#from sys import argv
import glob
import time

# sys.setdefaultencoding('utf-8')

output = "Tobeimport.csv"
media_dir = "/Users/leo/Library/Application Support/Anki2/用户1/collection.media"

reload(sys)  
sys.setdefaultencoding("utf8")  

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
    return m.group().strip()[10:]
    
def Main():
    curpath = os.getcwd()
    lrcfiles = curpath + "//*.lrc"
    flist = glob.glob(lrcfiles)
    writer = csv.writer(file(output, 'wb+'))
    pattern1 = re.compile(r'00]([\s\S]*) \r')

    i = 0
    for f in flist:
       i = i + 1
       
       newname_prefix = str(time.time()) + str(i)

       print "***********step1: 字幕处理 - 转码、重命名、提取中英文***********"
       newF = newname_prefix + '.lrc'
    #    os.system('iconv -f GB2312 -t UTF-8 ' + f + ' > ' + newF)
    #    os.remove(os.path.join(curpath, f))

       os.rename(f, newF)

       fh = file(newF,'r')
       content = fh.read()

       english = GetEnglish(content)
       chinese = GetChinese(content)

       print "***********step2: 音频处理 - 重命名音频文件***********"
       mp3file = f[:-3] + "mp3"
       newname = newname_prefix + ".mp3"
       
       os.rename(mp3file, newname)
       question = "[sound:" + newname +"]"

       writer.writerow([question, chinese, english])
       
       fh.close()

    del writer
    
    print "***********step3: 复制音频文件到媒体库***********"
    copyFiles(os.getcwd(), media_dir)
    


if __name__ == "__main__":
    Main()
    