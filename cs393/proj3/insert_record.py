#! /usr/bin/python

"""
    @author Nick Wilson
    @version 4.10.14

    insert_record.py
    The script will insert a record into a text database. It accepts one
    argument, which is the database name. The insert_record.py script should
    then prompt the user for the values of the fields in that database. The
    should then read in the field values and append these values in a new line
    to the end of the <database>.db file. Finally, the script should print a
    message that a new database record has been added.

    exit codes
        0 - success, record was added to the <database>.db
        1 - database did not exist in the databases.txt file 
        2 - <database>.db does not exist
        3 - incorrect usage of script
"""
import sys, os.path

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

def checkfileexists(name):
    """
        Function checks whether a file "name.db" actually exists.
        @param
            name - string representing the database we are looking for
        @return
            boolean true or false
    """
    tempname = name + ".db"
    return os.path.isfile(tempname)

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

def main(argv):
    if len(sys.argv) != 2:
        print "Usage: insert_record.py <database>"
        sys.exit(3)
    else:
        if checkfileexists(argv[1]):
            typedb = checkdatabasetxt(argv[1])
            if typedb == None:
                print "%s database type was not found exiting..." % typedb
                sys.exit(1)
            else:
                print argv[1]
                listAttributes = getTemplate(typedb)
                listAttributes = str(listAttributes).replace('[', '')
                listAttributes = listAttributes.replace(']', '')
                listAttributes = listAttributes.replace(',', '')
                listAttributes = listAttributes.replace('\'', '')

                print "Enter values for %s:" % listAttributes
                inputString = raw_input()
#while len(listAttributes) != len(inputString.split()):
                dataName = argv[1] + ".db"
                with open(dataName, "a") as f:
                    f.write(inputString + '\n')
                print "Record added to \"%s\" database." % argv[1]
                sys.exit(0)
        else:
            print "%s.db does not exist" % argv[1]

main(sys.argv)
