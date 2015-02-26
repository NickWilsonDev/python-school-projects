#! /usr/bin/python

"""
    @author Nick Wilson
    @version 1.17.14

    create_template.py

    Accepts as arguments a template name followed by up to eight field_names.
    Purpose is to create a new database template. Script calls the 
    find_template_file to find the file(file should reside in current dir)
    which contains information about the defined templates. After locating the
    template definition file, the script will append information about the 
    current template to the template definition file. If the template we are
    trying to add is already listed in that file, the script should exit with
    and appropriate error message and exit status. If the template is 
    successfully appended to the file, then an appropriate success message
    indicating the name of the new template should be printed out and the
    script should exit with a success indicator.

    Exit codes
        0 - success

"""
import sys, os, subprocess

def appendTemplateFile(templateFile, template):
    """
        Function appends template to the template.dat file.
    """
    
    temp = str(template).replace('[', '').replace(']', '')
    temp = temp.replace('\'', '').replace(',', '')
    temp += '\n'
    with open(templateFile, "a") as myfile:
        myfile.write(temp)


def main(argv):
    """
        not done /////////////////////////////////////////////
    """
    listargs = sys.argv
    if len(listargs) < 3:
        usage = "usage: create_template.py [template] [attribute] <attribute>"
        usage = usage + " <attribute> <attribute> <attribute> <attribute>"
        usage = usage + " <attribute> <attribute> <attribute>"
        print usage
        sys.exit(1)

    del listargs[0]
    
#find template definition file   use find_template_file.py
# create it if it does not exist
    p = subprocess.Popen("./find_template_file.py", stdout=subprocess.PIPE)

    tempDef = str(p.communicate()[0]).rstrip('\n')
    rc = p.returncode
    if int(rc) not in (0, 2):
        sys.exit(1)

#append list to template.dat
# if it is not already in the file
    p1 = subprocess.Popen(["./template_exists.py", tempDef,
            str(listargs[0]).rstrip('\n')], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    temp = p1.communicate()[0]
    rc = p1.returncode
    if int(rc) == 0:
        print "Template already exists in %s" % tempDef
        sys.exit(2)
    else:
        print "going to append"
        appendTemplateFile(tempDef, listargs)
        successmsg = "Template \"" + str(listargs[0]) + "\" has been added to "
        successmsg += "\"" + str(tempDef) + "\" definition file"
        print successmsg
        sys.exit(0)

main(sys.argv)
