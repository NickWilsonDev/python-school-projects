#! /usr/bin/python

"""
    @author Nick Wilson
    @version 1.17.14

    This script prompts the user to create a database, create a template for
    a database, or search through a template data file to see if a specified
    template exists.
"""
import sys, subprocess

def display_choices():
    print "Please select one of the following"
    print "1 - create a database"
    print "2 - create a template for a database"
    print "3 - search for a specified template"
    print "0 - exit"

def main():
    choice = 7
    while choice not in (0, 1, 2, 3):
        display_choices()
        choice = raw_input("Please select: ")
        print "choice is ", choice
        choice = int(choice)
        if choice == 0:
            print "Now exiting..."
            sys.exit(0)
        elif choice == 1:
            print "Please enter:: <templatename> <database name>"
            args = raw_input()
            subprocess.call("./create_database.py " + args, shell=True)
        elif choice == 2:
            print "Please enter:: <templatename> <1-8 attributenames>"
            args = raw_input()
            subprocess.call("./create_template.py " + args, shell=True)
        elif choice == 3:
            print "Please enter:: <template def file> <template name>"
            args = raw_input()
            subprocess.call("./template_exists.py " + args, shell=True)

main()
""" need to add calls to other scripts as needed """
