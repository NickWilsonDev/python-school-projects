#! /usr/bin/python
"""
    @author Nick Wilson
    @version 3.28.14

    This script searches all the files in the current directory for a file
    containing the following information(in the first row, first column) of
    the file.

    templateFile definition

    If no such file is found, then a new template file named "template.dat" is
    created. If multiple template definition files are found, the script
    should print out the names of at least two of the duplicate files and exit
    with a status of 1. Otherwise the name of the file discovered is returned
    and exits with an status of 0.

    Exit codes
        0 - successful exit, filename should be returned
        1 - multiple template def files were found, and should have been
            printed out
        2 - no template def file was found, "template.dat" should have been
            created
"""
import sys, os
from os import listdir
from os.path import isfile, join

def getListFiles():
    """
        Function returns list of all files in current directory.
        Uses "os.listdir(path)" this returns all files and directories except 
        "." and "..".
        @return
            a list of files in the current directory
    """
    files = [f for f in listdir(".") if isfile(join(".",f)) ]
    return files

def checkFiles(files):
    """
        Function checks each file in a list of files for a first line 
        containing "templateFile definition" each file that is found is put
        into a list that is returned.
        @param
            files - list of files in current directory
        @return
            a list of files whose first line is "templateFile definition\n"
    """
    listOFiles = []
    for tempfile in files:
        with open(tempfile, 'r') as f:
            firstLine = f.readline()
            if firstLine == "templateFile definition\n":
                listOFiles.append(tempfile)
    return listOFiles

def main():
    """
        Entry point into program, it calls appropriate helper functions to 
        accomplish its work.
    """
    lfiles = getListFiles()
    listfiles = checkFiles(lfiles)
    if len(listfiles) == 0:
        newfile = "template.dat"
        templateFile = open(newfile, "w")
        templateFile.write("templateFile definition\n")
        templateFile.close()
        print "template.dat"
        sys.exit(2)
    elif len(listfiles) == 1:
        print listfiles[0]
        sys.exit(0)
    else:
        print "Warning multiple template definition files detected!!!"
        print str(listfiles)
        sys.exit(1)
main()
