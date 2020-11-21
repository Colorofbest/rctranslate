#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Parse an Android strings.xml file to translate it in Google Translate by Copy and Paste
# creates files formatted to be copy and paste in Google Translate
# creates empty files where you paste Google Translate result
# then use rctranslate-recreate.py to recreate strings.xml for Android

# run :
# PYTHONIOENCODING=utf8 python3 rctranslate.py


from common import get_filename
from common import create_dir
from common import SEPARATOR_COPYPASTE,WORK_DIRECTORY,MAX_CAR_COPY_PASTE


cptFile = 1
cptNbCarTotal = 0
cptNbCar = 0
listFilesToTranslate = []
listFilesTranslated = []


# add string to the file, with separator
def add_string(file, txt):
    global f
    global cptFile
    global cptNbCar,cptNbCarTotal
    global listFilesToTranslate
    txt = txt.replace('\\ ', '\\').replace('\\ n ', '\\n').replace('\\n ', '\\n').replace('/ ', '/').strip()
    txt+= "\n" + SEPARATOR_COPYPASTE + "\n"

    cptNbCar+= len(txt)
    cptNbCarTotal+= cptNbCar

    if(cptNbCar > MAX_CAR_COPY_PASTE):
        #file too long, new file
        cptFile+=1
        cptNbCar = len(txt)
        
        filename = get_filename(OUTFILE, cptFile)
        filenameTranslated = get_filename(OUTFILE_TRANSLATED, cptFile)
            
        #work with this new file
        f.close()
        f = open(WORK_DIRECTORY + "/" + filename, "w")
        listFilesToTranslate.append(filename)
        
        #empty translated file
        fTranslated = open(WORK_DIRECTORY + "/" + filenameTranslated, "w").close()
        listFilesTranslated.append(filenameTranslated)
    
    f.write(txt)
    
# node element to string with html
def element_to_string(element):
     s = element.text or ""
     for sub_element in element:
         s += ET.tostring(sub_element, encoding='unicode')
     s += element.tail
     return s

# MAIN PROGRAM

# libraries
import html
import os
import xml.etree.ElementTree as ET
import sys
from io import BytesIO
import re
import time

# parameters
INFILE = input("Enter input xml strings filename: [default: strings.xml]\n")
if not INFILE:
    INFILE = "strings.xml"
OUTFILE = input("Enter output filename base : [default: totranslate.txt]\n")
if not OUTFILE:
    OUTFILE = "totranslate.txt"
OUTFILE_TRANSLATED = input("Enter empty translated filename: [default: translated.txt] (useful for translating several languages)\n")
if not OUTFILE_TRANSLATED:
    OUTFILE_TRANSLATED = "translated.txt"


create_dir(WORK_DIRECTORY)
filename = f = open(WORK_DIRECTORY + "/" + get_filename(OUTFILE), "w")

#initialize empty translated file
filenameTranslated = get_filename(OUTFILE_TRANSLATED)
fTranslated = open(WORK_DIRECTORY + "/" + filenameTranslated, "w").close()
listFilesToTranslate.append(filenameTranslated)

print("==========================\n\n")

# read xml structure
tree = ET.parse(INFILE)
root = tree.getroot()
iElement = 0

for i in range(len(root)):
    isTranslatable=root[i].get('translatable')
    if(root[i].tag=='string') & (isTranslatable!='false'):
        add_string(f, element_to_string(root[i]))
        iElement+= 1
        
    if(root[i].tag=='string-array'):
        for j in range(len(root[i])):
            isTranslatable=root[i][j].get('translatable')
            if(root[i][j].tag=='item') & (isTranslatable!='false'):
                add_string(f, element_to_string(root[i][j]))
                iElement+= 1

    
f.close()

print("end")
print("total characters : " + str(cptNbCarTotal))
print("total elements : " + str(iElement))
print("total files : " + str(cptFile))
print("")
print("Now :")
print(" - copy and translate (in Google Translate) files in " + WORK_DIRECTORY + " : " + ", ".join(listFilesToTranslate))
print(" - paste result in" + WORK_DIRECTORY + " : " + ", ".join(listFilesToTranslate))



