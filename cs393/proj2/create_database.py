#! /usr/bin/python
"""
    @author Nick Wilson
    @version 4.20.14

    Script accepts two command line arguments. The name of the template, and 
    the name of a database file we wish to create.  This script creates a new
    empty database file "based upon" a template that exists in the template
    definitions file.  The name of the database and the name of the template
    will be supplied as command line arguments into the script.

    Exit codes
        1 - incorrect number of command line arguments
        2 - specified template does not exist
        3 - no template definition file was found
        4 - database already exists
"""
import sys, subprocess
import os.path

def checkDatabases(database, template):
    """
       Function checks "databases.txt" to see if it already contains a
       database using the specified template and database name. It returns
       true if it does false otherwise.
       @param
            database - name of database we are checking for
            template - name of template we are checking for
       @return
           boolean - signifies whether or not database already exists
    """
    if not os.path.isfile("databases.txt"):
        return False
    else:
        target = database + " " + template
        with open("databases.txt", "r") as myfile:
            for line in myfile:
                if target == line:
                    return True
        return False

def checkTemplate(templateDef, template):
    """
        Function checks template definition file for the specified template
        @param
            templateDef - the template definition file
            template    - basically a string containing the name of the
                          template we are looking for
        @return
            boolean - signifies whether template exists in template def file
    """
    print "checking %s" % templateDef
    with open(templateDef, "r") as f:
        for line in f:
            templine = line.split()
            if templine[0] == template:
                return True
        return False

def main(argv):
    """
       Entry point into the program, calls appropriate helper functions to
       accomplish goals of the script.
    """
    if len(argv) != 3:
        print "Usage: ./create_database.py <template name> <database name>"
        sys.exit(1)
    else:
        templateName = argv[1]
        databaseFile = argv[2]
        p = subprocess.Popen("./find_template_file.py", stdout=subprocess.PIPE)
        tempDef = str(p.communicate()[0]).rstrip('\n')
        rc = p.returncode

        if int(rc) != 0:
            print "No template definition file was found exiting..."
            sys.exit(3)

        result = checkTemplate(str(tempDef), templateName)
        if result == False:
                print "Template does not exist in %s" % tempDef
                sys.exit(2)

        result = checkDatabases(databaseFile, templateName)
        if result == True:
                print "Database \"%s\" already exists." % argv[2]
                sys.exit(4)
        else:
            data = databaseFile + " " + templateName + "\n"
            with open("databases.txt", "a") as myfile:
                myfile.write(data)
            dataname = databaseFile + ".db"
            open(dataname, 'a').close()
            print "Database \"%s\" using template \"%s\" has been created." % (argv[1], argv[2])
            sys.exit(0)

main(sys.argv)
