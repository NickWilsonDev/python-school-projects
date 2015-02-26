#! /usr/bin/python

"""
    @author Nick Wilson
    @version 2.24.14

    Script mimmicks functionallity of the linux "tee" command. It should
    take input from standard input and print it to standard out and to any
    files supplied as arguments on the command line.
    For right now it will not overwrite files, for safety.
    Assumptions
        files have correct read permissions and exist
        max screen size of 100 rows

    Exit codes
        0 - successful exit
        1 - specified file did not have write permissions or did already 
            existed
"""
import sys, os

def writeFile(fileList, user_input, appendflag):
    """
        Function writes specified user input to all files in specified
        filelist. But if the flag "append" is true the function simply appends
        the input to the end of the specified files.
    """
    user_input = user_input + '\n'
    for temp in fileList:
        if appendflag == True:
            with open(temp, "a") as f:
                f.write(user_input)
                f.close()
        else:
            with open(temp, "w") as f:
                f.write(user_input)
                f.close()

def main(argv):
    """
        Function provides entry point into the script. To exit the program
        catches the EOF exception sent when the user presses "ctrl + d".
    """
    print "ctrl + d to quit"
    appendflag = False
    if len(sys.argv) == 1:
        user_input = ""
        while True:
            try:
                user_input = raw_input()
                print ">", user_input
            except EOFError:
                print "Exiting...."
                sys.exit(0)

    else:
        arglist = argv
        del arglist[0]
        if '-a' in arglist:
            i = arglist.index("-a")
            appendflag = True
            del arglist[i]

        print 'File list:', str(argv)
        filelist = []
        user_input = ""
        for temp in arglist:
            filelist.append(temp)
        while True:
            try:
                user_input = raw_input()
#print ">", user_input
                writeFile(filelist, user_input, appendflag)
                print user_input
                appendflag = True
            except EOFError:
                print "Closing files and Exiting....."
                sys.exit(0)
main(sys.argv)
