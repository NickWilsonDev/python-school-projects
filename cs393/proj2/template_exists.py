#! /usr/bin/python

"""
    @author Nick Wilson
    @version 4.9.14

    template_exists.py

    This script accepts two command line arguments, the name of the template
    definitions file, and the name of the template. If the template definition
    supplied as an argument does not exist, prompt the user for a new template
    definition file. The script should prompt the user for the template
    definition file name, until the file is found. The script should return
    success if one (and only one) valid entry defining the template is found
    in the template definition file, otherwise the script ends in failure.

    exit codes
    0 - success, template found
    1 - incorrect arguments specified
    2 - 
"""

import os.path, sys

def main(argv):
    if len(sys.argv) != 3:
        print "usage: template_exists.py <template def file> <template name>"
        sys.exit(1)
    defFile = sys.argv[1]
    while os.path.isfile(defFile) == False:
        print "\"%s\" does not exist please enter another" % defFile
        defFile = raw_input()
    match = 0
    with open(defFile, "r") as f:
        for line in f:
            templine = line.split()
            if templine[0] == sys.argv[2]:
                match = 1
    if match == 1:
        print "found!!!!"
        sys.exit(0)
    else:
        print "template name not found"
        sys.exit(2)

main(sys.argv)
