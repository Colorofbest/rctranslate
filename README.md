# rctranslate
Helps to __translate Android strings.xml__, providing batch translation for Google Translate

There are other projects to translate Android xml string files. But when you have a lot of expressions to translate, Google responds with a captcha page, so it's not working anymore.

With this project I suggest you a manual translation in the Google Translate webpage (or another translation app).
Allows to copy and paste a lot of translations at one time (and maybe better translations with a better context, because there are a lot of words).

# Prerequisite
Python 3

# How it works

## 1. Original file

Copy your strings.xml file in the project directory.

## 2. Create flat files to be translated, parsing the strings.xml

```python3 rctranslate.py```

 - creates files formatted to be copy and paste in Google Translate (totranslate-1.txt, totranslate-2.txt, ... by default)
 - creates empty files where you paste Google Translate result (translated-1.txt, translated-2.txt, ... by default)
 
## 3. Translate

Copy "totranslate-X.txt" data into Google Translate, one by one

## 4. Paste results

 - paste Google Translate results into the same number "translated-X.txt" files.

## 5. Recreate strings.xml for Android

```python3 rctranslate-recreate.py```

 - generates the strings-translated.xml (by default) file with translated data.
 
 
 
 Generated files are in "work" directory.
