# -*- coding: utf-8 -*-

import os, sys
import shutil

dirOpencc = "..\\bin\\opencc\\"
dirOrigin = "..\\civclub\\civ5root\\"
dirOutput = ".\\output\\"
dirAssets = "Assets\\"

absDirOpencc = os.path.abspath(dirOpencc)

countDir = 0
countFile = 0


def processPath(path, inZhCn):
    global countDir
    lastPath = os.getcwd()
    os.chdir(path)

    isZhCn = os.path.basename(path) == 'zh_CN'
    
    if isZhCn or inZhCn:
        pathZhTw = path.replace("zh_CN", "zh_TW")
        if not os.path.isdir(pathZhTw):
            os.makedirs(pathZhTw)
    
    if isZhCn or inZhCn:
        print os.path.basename(path) + "\t" + os.path.abspath(path)
        countDir += 1

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


def preprocess():
    ## 刪除目的資料夾
    cmdRmdir = 'rmdir /s /q "%s"' % dirOutput
    os.system(cmdRmdir)
    ## 重建目的資料夾
    os.makedirs(dirOutput)
    
    shutil.copytree(dirOrigin+dirAssets, dirOutput+dirAssets)

    ## 需手動修改內容
    prefix = os.path.abspath(dirOutput + dirAssets)
    
    xmlCnOld = prefix + '\\Gameplay\\XML\\NewText\\Chinese.xml'
    xmlCn = prefix + '\\Gameplay\\XML\\NewText\\ChineseSimp.xml'
    xmlTw = prefix + '\\Gameplay\\XML\\NewText\\ChineseTrad.xml'
    os.remove(xmlCnOld)
    shutil.copy(".\\special\\ChineseSimp.xml", xmlCn)
    shutil.copy(".\\special\\ChineseTrad.xml", xmlTw)
    
    creditsCn = prefix + '\\Gameplay\\XML\\NewText\\CIV5Credits_zh_CN.txt'
    creditsTw = prefix + '\\Gameplay\\XML\\NewText\\CIV5Credits_zh_TW.txt'
    dlcCreditsCn = prefix + '\\DLC\\Expansion\\Gameplay\\XML\\Text\\CIV5Credits_zh_CN.txt'
    dlcCreditsTw = prefix + '\\DLC\\Expansion\\Gameplay\\XML\\Text\\CIV5Credits_zh_TW.txt'
    convertZ(creditsCn, creditsTw)
    convertZ(dlcCreditsCn, dlcCreditsTw)

    sqlPath = prefix + '\\SQL\\'
    shutil.copy(".\\special\\Civ5DlcLocalizationDatabaseSchema.sql", sqlPath)
    shutil.copy(".\\special\\Civ5LocalizationDatabaseSchema.sql", sqlPath)
    

## src, dst 的路徑需為絕對路徑
def convertZ(src, dst):
    global countFile
    lastPath = os.getcwd()
    os.chdir(absDirOpencc)

    ## 轉碼
    cccmd = 'opencc.exe -i "%s" -o "%s" -c zhs2zhtw_vpy.ini' % (src, dst)
    os.system(cccmd)
    countFile += 1

    os.chdir(lastPath)


preprocess()
processPath(dirOutput, False)

print 'count of locale dirs: %d' % (countDir,)
print 'count of locale files (converted): %d' % (countFile,)
