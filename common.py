#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Common functions

import os

SEPARATOR_COPYPASTE = "-------"
# generated files
WORK_DIRECTORY = "work"
# max characters to translate in one click (google translation limit)
MAX_CAR_COPY_PASTE = 5000

# get filename with number
# file-1,file-2
def get_filename(default_filename, cpt = 1):
    dot_index = default_filename.rfind(".")
    if(dot_index == -1):
        #filename-2
        return default_filename + "-" + str(cpt)
    else:
        #filename-2.txt
        return ("-" + str(cpt) + ".").join(default_filename.rsplit(".", 1))
    pass

# creates a directory from current directory if not exists
def create_dir(dirname):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, dirname)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    pass
