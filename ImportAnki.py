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
output = "Tobeimport.csv"
media_dir = "/Users/leo/Library/Application Support/Anki2/用户1/collection.media"

def Main():
    curpath = os.getcwd()
    lrcfiles = curpath + "//*.lrc"
    flist = glob.glob(lrcfiles)
    writer = csv.writer(file(output, 'wb+'))
    pattern1 = re.compile(r'00]([\s\S]*) \t')
    pattern2 = re.compile(r'\t([\s\S]*)')
    i = 0
    for f in flist:
       i = i + 1
       fh = file(f,'r')
       content = fh.read()
       english = pattern1.findall(content)
       chinese = pattern2.findall(content)

       #print content

       #print english
       #print chinese 
       mp3file = f[:-3] + "mp3"
       newname = str(time.time()) + str(i) + ".mp3"
       #print mp3file
       #print newname
       os.rename(mp3file, newname)
       question = "[sound:" + newname +"]"

       if not english:
	   answer =content[10:]
       else:
	   answer = english[0] + "   " + question
       writer.writerow([question, answer])
       fh.close()
    del writer
    print "***********复制音频文件到媒体库***********"
    copyFiles(os.getcwd(), media_dir)
      
def copyFiles(sourceDir,  targetDir):
    for file in os.listdir(sourceDir): 
        if os.path.splitext(file)[1] != ".mp3":
            continue
        print file
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

if __name__ == "__main__":
    Main()
    