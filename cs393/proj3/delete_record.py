#! /usr/bin/python
"""
    @author Nick Wilson
    @version 4.20.14

    delete_record.py
    Script deletes record from a text database. It accepts arguments
    databasename, field name, and field value. It should verify that the 
    database exists and if so then it should remove any lines in that file that
    contain the field value for that field. If successful the the script should
    display how many records were deleted.

    Exit codes
        0 - successfully deleted record, if any fields matched
        1 - database did not exist
        2 - incorrect usage
        3 - database did not exist in "databases.txt"

"""

import sys, os.path, shutil

def getTemplate(name):
    """
        Function gets list of attributes for the database type, from the 
        "template.dat" file.
        @param
            name - string representing the template we want to find
        @return
            a list of attributes for this type of database
    """
    with open('template.dat') as f:
        for line in f:
            tempstr = line.split()
            if tempstr[0] == name:
                del tempstr[0]
                return tempstr

def checkdatabasetxt(name):
    """
        Function checks "databases.txt" file for existence of the specified
        database. If found then the template for that database is returned,
        else "None" will be returned and the script will know to exit with an
        error message.
        @param
            name - a string representing the database that we wish to add a 
                   record to
    """
    typedatabase = None
    with open('databases.txt') as f:
        for line in f:
            tempstr = line.split()
            if tempstr[0] == name:
                typedatabase = tempstr[1]
    return typedatabase


def deleteLine(filename, position, value):
    """
        Function reads file and splits each line. If string at proper position
        is not equal to the value then that line is copied to temp file. Then
        the temp file is renamed to the properly named file, overwritting it.
    """
    count = 0
    with open(filename) as f:
        with open("tmp.txt", "w") as new:
            for line in f:
                templine = line.split()
                if templine[position] == value:
                    count += 1
                else:
                    new.write(line)
    shutil.move("tmp.txt", filename)
    print "There were %d record(s) deleted from the \"%s\" database." % (count, filename)

def main(argv):
    if len(sys.argv) != 4:
        print "Usage: delete_record.py <database> <fieldname> <fieldvalue>"
        sys.exit(2)
    print argv[1]
    databasename = argv[1] + ".db"
    if os.path.isfile(databasename) == False:
        print "Database \"%s\" does not exist" % databasename
        sys.exit(1)
    else:
        templatename = checkdatabasetxt(argv[1])
        if templatename == None:
            sys.exit(3)
        listAttr = getTemplate(templatename)
        position = listAttr.index(argv[2])
        deleteLine(databasename, position, argv[3])
        sys.exit(0)

main(sys.argv)
