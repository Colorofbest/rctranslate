#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# recreate strings.xml for Android from translated files
# Parse translated files (generated with rctranslate.py) where you have copied translated results

# run : 
# PYTHONIOENCODING=utf8 python3 rctranslate-recreate.py

from common import get_filename
from common import create_dir
from common import SEPARATOR_COPYPASTE,WORK_DIRECTORY

# libraries
import html
import os
import xml.etree.ElementTree as ET
import sys
from io import BytesIO
import re
import time

#replace the element with new text translated
#not prefect with html tags : they are encoded in final xml
def update_element(parent, elem, txt):
    s = html.unescape(txt.replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/').strip()).replace("'", r"\'")

    elem.text = html.unescape(s)

    #not perfect
    for child in list(elem):
        elem.remove(child)
    return
    

# parameters
INFILE = input("Enter xml strings original filename: [default: strings.xml]\n")
if not INFILE:
    INFILE = "strings.xml"
OUTFILE = input("Enter output filename base : [default: strings-translated.xml]\n")
if not OUTFILE:
    OUTFILE = "strings-translated.xml"
OUTFILE_TRANSLATED = input("Enter empty translated filename: [default: translated.txt] (useful for translating several languages)\n")
if not OUTFILE_TRANSLATED:
    OUTFILE_TRANSLATED = "translated.txt"

print("==========================\n\n")

#parse all files file-1, file-2, ...
tabAllString = []
cptFile = 1;
filenameTranslated = get_filename(OUTFILE_TRANSLATED, cptFile)
while(os.path.isfile(os.path.join(WORK_DIRECTORY, filenameTranslated))):
    f = open(os.path.join(WORK_DIRECTORY, filenameTranslated), encoding="utf8")
    txt = f.read()
    tab = txt.split(SEPARATOR_COPYPASTE)

    #if last line is empty (because multiple files)
    if(tab[len(tab)-1] == ""):
        tab.pop()
    
    tabAllString.extend(tab)
    f.close()

    #next file
    cptFile+=1
    filenameTranslated = get_filename(OUTFILE_TRANSLATED, cptFile)
      
# read xml structure
tree = ET.parse(INFILE)
root = tree.getroot()
iElement = 0
isNotEnoughTranslatedStrings = False

print("nb string translated found = " + str(len(tabAllString)))

#same parse like in rctranslate.py
for i in range(len(root)):
    isTranslatable=root[i].get('translatable')
    if(root[i].tag=='string') & (isTranslatable!='false'):
        #translate element
        if(len(tabAllString) < iElement+1):
            isNotEnoughTranslatedStrings = True
        else:
            update_element(root, root[i], tabAllString[iElement])
        iElement+= 1
            
    if(root[i].tag=='string-array'):
        for j in range(len(root[i])):
            isTranslatable=root[i][j].get('translatable')
            if(root[i][j].tag=='item') & (isTranslatable!='false'):
                if(len(tabAllString) < iElement+1):
                    isNotEnoughTranslatedStrings = True
                else:
                    #translate element
                    update_element(root[i], root[i][j], tabAllString[iElement])
                iElement+= 1

if(isNotEnoughTranslatedStrings):
    print("Error : not enough translated strings : "+ str(len(tabAllString)))
    print("Need " + str(iElement) + " translated strings");
    
# write translated xml file
tree.write(os.path.join(WORK_DIRECTORY, OUTFILE), encoding='utf-8')

print("total files : " + str(cptFile))
print("total elements : " + str(iElement))
print("")
print("xml file generated : " + os.path.join(WORK_DIRECTORY, OUTFILE))



