#! /usr/bin/python

"""
    @author Nick Wilson
    @version 1.27.13

    Script mimmicks functionallity of the linux "more" command. It should
    display 15 lines from a file specified on the command line and then a
    division bar, waiting on user to press "enter". If no file is specified
    script should read from standard input.

    Assumptions
        files have correct read permissions and exist
        max screen size of 100 rows

    Exit codes
        0 - successful exit
        1 - specified file did not have read permissions or did not exist
"""
import sys, os

def clear():
    """
    Function clears the terminal screen by printing nothing 100 times.
    """
    row = 0
    while row < 100:
        print ""
        row = row + 1

def main(argv):
    """
    Function provides entry point into the script.
    """
    if len(sys.argv) == 1:
        print "Enter 'q' and enter to exit"
        user_input = ""
        count = 1
        while user_input != 'q':
            user_input = raw_input()
            print ">", user_input
            count = count + 1
            if count == 16:
                raw_input("---------------------Press Enter ----------------")
                count = 1
                clear()
        sys.exit(0)

    else:
        filename = argv[1]
        if not os.access(filename, os.F_OK):
            print "File does not exist"
            sys.exit(1)
        if not os.access(filename, os.R_OK):
            print "File does not have read permisions"
            sys.exit(1)
            
        filename = open(filename, "r")
        count = 1
        for line in filename:
            print line.rstrip('\r\n')
            count = count + 1
            if count == 16:
                raw_input( "--------------------Press Enter ----------------")
                count = 1
                clear()
        sys.exit(0)
main(sys.argv)
