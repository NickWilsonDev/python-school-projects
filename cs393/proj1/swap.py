#! /bin/python

"""
    Nick Wilson
    The purpose of this script is to swap the contents of two files.
    Date 12.14.13

    Exit codes
    0 -- successful operation
    1 -- user only specified one file to swap
    2 -- user did not specify the correct number of files to swap
         should be 0 or 2
    3 -- one or more of the files specified do not exist
    4 -- one or more of the files do not have read permisions
    5 -- one or more of the files do not have write permisions
    6 -- the filename that would be temporarily used by the swap is already
         in use
"""
import sys, os

def print_usage():
    """
    Function prints the usage message for the script
    """
    print "swap.py [filename] [filename]"

def swap_file(source, dest):
    """
    Function reads from source file one line at a time and writes to 
    destination file what has been read.
    Params
        source - file that will be read from
        dest   - file that will be written to
    """
    sourcefile = open(source, "r")
    destfile   = open(dest, "w")

    for line in sourcefile:
        destfile.write(line)
    destfile.close()
    sourcefile.close()

def check_permissions(filename):
    """
    Function checks whether file specified as a parameter exists and has
    correct read and write permissions. If any of these tests fail then the
    script exits with the appropriate error code
    Param
        filename - the name of the file that will be checked
    """
    if os.access(filename, os.F_OK):
        if os.access(filename, os.R_OK):
            if os.access(filename, os.W_OK):
                return True
            else:
                print filename, " does not have write permissions"
                sys.exit(5)
        else:
            print filename, " does not have read permissions"
            sys.exit(4)
    else:
        print filename, " does not exist"

        sys.exit(3)

def main(argv):
    """
    Function provides entry point into script, it calls the appropriate helper
    functions to handlw some of the work.
    """
    if os.access("temp.txt", os.F_OK):
        print 'The file temp.txt that needs to be used during the swap already'
        print ' exists'
        sys.exit(6)
    else:
        if len(sys.argv) not in (1, 3):
            print_usage()
            sys.exit(2)
        else:
            temp = "temp.txt"
            if len(sys.argv) == 1:
                print "Please enter first filename that will be swapped"
                file1 = raw_input("Filename: ")
                print "Please enter second filename to be swapped"
                file2 = raw_input("Filename: ")
                
                check_permissions(file1)
                check_permissions(file2)
                swap_file(file1, temp)
                swap_file(file2, file1)
                swap_file(temp, file2)
            else:
                file1 = sys.argv[1]
                file2 = sys.argv[2] 
                check_permissions(file1)
                check_permissions(file2)
                swap_file(file1, temp)
                swap_file(file2, file1)
                swap_file(temp, file2)
            os.remove("temp.txt")
            sys.exit(0)

main(sys.argv)
