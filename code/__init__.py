# -*- coding: utf-8 -*-

import os, sys
import shutil

dirOpencc = "D:\\Apps\\opencc\\"
# dirOrigin = "D:\\Steam\\steamapps\\common\\sid meier's civilization v\\assets\\"
dirOrigin = "D:\\civ5zh\\civ5mock\\Assets\\"
#dirOutput = "D:\\work\\civ5zh\\Sources\\assets\\"
dirOutput = "D:\\civ5zh\\civ5mock\\AssetsOutput\\"

specialFiles = ['Gameplay\\XML\\NewText\\CIV5Credits_zh_CN.txt',
                'Gameplay\\XML\\NewText\\CIV5Credits_zh_TW.txt',
                'Gameplay\\XML\\NewText\\ChineseSimp.xml',
                'Gameplay\\XML\\NewText\\ChineseTrad.xml',
                'UI\\Fonts\\Tw Cent MT\\TwCenMT14.ggxml',
                'UI\\Options\\OptionsMenu.xml']

countDir = 0
countFile = 0

def doEntry(entry, isInZhCN):
    if os.path.isdir(entry):
        doDir(entry, isInZhCN)
    elif isInZhCN:
        doFile(entry)
        
def doDir(dir, isInZhCN):
    lastDir = os.getcwd()
    os.chdir(dir)
    
    isZhCN = os.path.basename(dir) == 'zh_CN'
    # 如果是位於簡中語系資料夾下，就先產生對應的繁中語系資料夾
    if isInZhCN or isZhCN:
        global countDir
        countDir += 1
        
        dirZhTW = dir.replace('zh_CN', 'zh_TW')
        if os.path.isdir(dirZhTW):
            print '[dir] %s already exists' % (dirZhTW,)
        else:
            print '[dir] make dir: %s'
            os.makedirs(dirZhTW)
            
    entryList = os.listdir(dir)
    for entry in entryList:
        absPath = os.path.abspath(entry)
        doEntry(absPath, isInZhCN or isZhCN)
        
    os.chdir(lastDir)
    
def doFile(txtFile):
    if txtFile[-3:] != 'xml':
        return
    
    global countFile
    countFile += 1
    txtFileZhTW = txtFile.replace('zh_CN', 'zh_TW')
    txtFileZhTWOrig = txtFileZhTW + '.orig'
    print '[file] create zh_TW copy of %s' % (txtFile,)
    os.chdir(dirOpencc)
    # 轉碼
    cmdOpencc = 'opencc.exe -i "%s" -o "%s" -c zhs2zht.ini' % (txtFile, txtFileZhTWOrig)
    os.system(cmdOpencc)
    # 替換檔案內文字
    input = open(txtFileZhTWOrig)
    output = open(txtFileZhTW, 'w')
    for s in input:
        output.write(s.replace("zh_CN", "zh_TW"))
    input.close()
    output.close()
    # 刪除暫存檔
    os.remove(txtFileZhTWOrig)
    # 回到原資料夾
    os.chdir(os.path.dirname(txtFile))
    
def copyLocaleFiles(path):
    if not os.path.isdir(path):
        return

    lastDir = os.getcwd()
    os.chdir(path)
    
    dirName = os.path.basename(path)
    if dirName == 'zh_CN' or dirName == 'zh_TW':
        dstPath = path.replace(dirOrigin, dirOutput)
        print "[dir] coping dir: %s to %s" % (path, dstPath)
        shutil.copytree(path, dstPath)
    else:
        subPathList = os.listdir(path)
        for subPath in subPathList:
            copyLocaleFiles(os.path.abspath(subPath))
            
    os.chdir(lastDir)

def processPath(path, inZhCn):
    lastPath = os.getcwd()
    os.chdir(path)

    isZhCn = os.path.basename(path) == 'zh_CN'
    
    if isZhCn or inZhCn:
        pathZhTw = path.replace("zh_CN", "zh_TW")
        if not os.path.isdir(pathZhTw):
            os.makedirs(pathZhTw)
    
    if isZhCn or inZhCn:
        print os.path.basename(path) + "\t" + os.path.abspath(path)
    
    fileList = os.listdir(path)
    for subPath in fileList:
        absPath = os.path.abspath(subPath)
        if os.path.isdir(absPath):
            processPath(absPath, isZhCn or inZhCn)
        elif (isZhCn or inZhCn) and subPath[-3:] == "xml":
            absPathTw = absPath.replace("zh_CN", "zh_TW")
            #shutil.copyfile(absPath, absPathTw)
            os.chdir("D:\\Apps\\opencc\\")
            # 轉碼
            cccmd = "opencc.exe -i \"" + absPath + "\" -o \"" + absPathTw + ".orig\" -c zhs2zht.ini"
            os.system(cccmd)
            # 替換 zh_CN 為 zh_TW
            input = open(absPathTw+".orig")
            output = open(absPathTw, 'w')
            for s in input:
                output.write(s.replace("zh_CN", "zh_TW"))
            input.close()
            output.close()
            os.remove(absPathTw+".orig")
            os.chdir(path)
            
  
    os.chdir(lastPath)

def setupLocaleFiles():
    # 刪除目的資料夾
    cmdRmdir = 'rmdir /s /q "%s"' % dirOutput
    os.system(cmdRmdir)
    # 重建目的資料夾
    os.makedirs(dirOutput)
    copyLocaleFiles(dirOrigin)

    # 針對特殊檔案進行複製
    for sf in specialFiles:
        origFile = dirOrigin + sf
        targetFile = dirOutput + sf
        targetPath = os.path.dirname(targetFile)
        if not os.path.isdir(targetPath):
            os.makedirs(targetPath)
        print '[file] coping file: %s' % sf
        shutil.copy(origFile, targetFile)


def preprocess(path):
    xmlFile = dirOrigin + 'Gameplay\\XML\\NewText\\Chinese.xml'
    xmlCn = dirOrigin + 'Gameplay\\XML\\NewText\\ChineseSimp.xml'
    xmlTw = dirOrigin + 'Gameplay\\XML\\NewText\\ChineseTrad.xml'
    creditsCn = dirOrigin + 'Gameplay\\XML\\NewText\\CIV5Credits_zh_CN.txt'
    creditsTw = dirOrigin + 'Gameplay\\XML\\NewText\\CIV5Credits_zh_TW.txt'
    os.rename(xmlFile, xmlCn)
    shutil.copy(xmlCn, xmlTw)
    shutil.copy(creditsCn, creditsTw)
    # 需手動修改內容

os.chdir(dirOrigin)
preprocess(dirOrigin)
processPath(dirOrigin, False)
#doEntry(dirOrigin, False)
setupLocaleFiles()

print 'count of locale dirs: %d' % (countDir,)
print 'count of locale files: %d' % (countFile,)