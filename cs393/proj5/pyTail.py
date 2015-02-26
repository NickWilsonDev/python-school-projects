#! /usr/bin/python

"""
    @author Nick Wilson
    @version 3.29.14

    Script mimmicks functionallity of the linux "tail" command. It should read
    lines from files supplied on the command line, if no files are specified
    it will fall back to standard input, and write the last 10 lines of the 
    input to standard out. The script should optionally accept an argument
    that defines the number of lines to print out.

    Assumptions
        files have correct read permissions and exist
        max screen size of 100 rows

    Exit codes
        0 - successful exit
        1 - specified file did not have read permissions or did not exist
"""
import sys, os

def getLineCount(filename):
    """
        Function counts lines in file specified in parameter and returns them.
    """
    numlines = sum(1 for line in open(filename))
    return numlines

def printLastNLines(filelist, numlines):
    """
        Function prints last 'n' lines of every file specified in the file
        list.
    """
    for f in filelist:
        print "===> %s <===" % f
        totalLines = getLineCount(f)
        if totalLines < numlines:
            for line in open(f):
                line = line.rstrip('\n')
                print line
        else:
            startPos = totalLines - numlines
            currentPos = 1
            for line in open(f):
                if currentPos > startPos:
                    line = line.rstrip('\n')
                    print line
                currentPos = currentPos + 1

def main(argv):
    """
    Function provides entry point into the script.
    """
    index = -1
    fileList = argv
    tailLines = 10
    del argv[0]
    for arg in fileList:
        if arg.startswith('-') and arg[1:].isdigit():
            tailLines = -1 * int(arg)
            index = fileList.index(arg)
        if index != -1:
            del fileList[index]

    if len(sys.argv) == 0:
        print "Ctrl + d to exit"
        user_input = ""
        userList = []
        while True:
            try:
                user_input = raw_input()
                userList.append(user_input)
                if len(userList) > tailLines:
                    del userList[0]
            except EOFError:
                for line in userList:
                    print line
                sys.exit(0)
    else:
        printLastNLines(fileList, tailLines)
        sys.exit(0)
main(sys.argv)
