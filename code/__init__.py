# -*- coding: utf-8 -*-

import os, sys
import shutil

dirOpencc = "..\\bin\\opencc\\"
dirOrigin = "..\\civclub\\civ5root\\"
dirOutput = ".\\output\\"
dirAssets = "Assets\\"

absDirOpencc = os.path.abspath(dirOpencc)

specialFiles = ['Gameplay\\XML\\NewText\\CIV5Credits_zh_CN.txt',
                'Gameplay\\XML\\NewText\\CIV5Credits_zh_TW.txt',
                'Gameplay\\XML\\NewText\\ChineseSimp.xml',
                'Gameplay\\XML\\NewText\\ChineseTrad.xml',
                'UI\\Fonts\\Tw Cent MT\\TwCenMT14.ggxml',
                'UI\\Options\\OptionsMenu.xml']

countDir = 0
countFile = 0


def copyLocaleFiles(path):
    if not os.path.isdir(path):
        return

    lastDir = os.getcwd()
    os.chdir(path)
    
    dirName = os.path.basename(path)
    if dirName == 'zh_CN' or dirName == 'zh_TW':
        dstPath = path.replace(dirOrigin, dirOutput)
        print "[dir] coping dir: %s to %s" % (path, dstPath)
        countDir++
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

    fileList = os.listdir(".")
    for subPath in fileList:
        absPath = os.path.abspath(subPath)
        if os.path.isdir(absPath):
            processPath(absPath, isZhCn or inZhCn)
        elif (isZhCn or inZhCn) and (subPath[-3:] == "xml" or subPath[-3:] == "XML"):
            absPathTw = absPath.replace("zh_CN", "zh_TW")
            convertZ(absPath, absPathTw + '.orig')
            
            ## 將檔案內文字 zh_CN 替換為 zh_TW
            input = open(absPathTw+".orig")
            output = open(absPathTw, 'w')
            for s in input:
                output.write(s.replace("zh_CN", "zh_TW"))
            input.close()
            output.close()
            ## 刪除暫存檔
            os.remove(absPathTw+".orig")
            
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


def preprocess():
    ## 刪除目的資料夾
    cmdRmdir = 'rmdir /s /q "%s"' % dirOutput
    os.system(cmdRmdir)
    ## 重建目的資料夾
    os.makedirs(dirOutput)
    
    shutil.copytree(dirOrigin+dirAssets, dirOutput+dirAssets)

    ## 需手動修改內容
    prefix = os.path.abspath(dirOutput + dirAssets)
    xmlFile = prefix + '\\Gameplay\\XML\\NewText\\Chinese.xml'
    xmlCn = prefix + '\\Gameplay\\XML\\NewText\\ChineseSimp.xml'
    xmlTw = prefix + '\\Gameplay\\XML\\NewText\\ChineseTrad.xml'
    creditsCn = prefix + '\\Gameplay\\XML\\NewText\\CIV5Credits_zh_CN.txt'
    creditsTw = prefix + '\\Gameplay\\XML\\NewText\\CIV5Credits_zh_TW.txt'
    dlcCreditsCn = prefix + '\\DLC\\Expansion\\Gameplay\\XML\\Text\\CIV5Credits_zh_CN.txt'
    dlcCreditsTw = prefix + '\\DLC\\Expansion\\Gameplay\\XML\\Text\\CIV5Credits_zh_TW.txt'
    os.rename(xmlFile, xmlCn)
    convertZ(xmlCn, xmlTw) # 這個檔不能單單轉換
    convertZ(creditsCn, creditsTw)
    convertZ(dlcCreditsCn, dlcCreditsTw)


## src, dst 的路徑需為絕對路徑
def convertZ(src, dst):
    lastPath = os.getcwd()
    os.chdir(absDirOpencc)

    ## 轉碼
    cccmd = 'opencc.exe -i "%s" -o "%s" -c zhs2zht.ini' % (src, dst)
    os.system(cccmd)
    countFile++

    os.chdir(lastPath)


preprocess()
processPath(dirOutput, False)
# setupLocaleFiles()

print 'count of locale dirs: %d' % (countDir,)
print 'count of locale files: %d' % (countFile,)
