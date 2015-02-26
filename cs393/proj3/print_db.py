#! /usr/bin/python

"""
    @author Nick Wilson
    @version 4.10.14

    print_db.sh

    This script prints a text database that has been sorted on a specified
    field. 
    usage: print_db.sh <database_name> [-n|-r] [-n|-r] [<field_name>]
    -n flag means sort numerically
    -r flag means sort reverse order
    default is to sort ASCII on first field

    exit codes
    0 - successful operation
    1 - incorrect arguments, usage message printed out
    2 - template definition file does not exist

"""
import sys, argparse, os, subprocess
from collections import OrderedDict
from subprocess import call

def makeLatexFile(filename, listDict):
    listAttr = getListAttr(filename)
    numofcells = len(listAttr)
    pdf = open('tmp.tex', 'w')
    pdf.write('\\documentclass{article}\n')
    pdf.write('\\begin{document}\n')
    pdf.write('\\begin{center}\n')
    pdf.write('\\begin{tabular}{ |c' + ' r ' * (numofcells - 1) + '| }\n')
    pdf.write('\\hline\n')

#headerinfo #######################
    tempstr = ""
    for temp in listAttr:
        tempstr += temp + ' & '
    tempstr = tempstr[:-3]
    tempstr += " \\\\\n"
    pdf.write(tempstr)
    pdf.write('\\hline\n')
#end of header ####################
#loop for putting data in

    for item in listDict:
        temp = str(item.values()).replace(', ', ' & ').replace('[','')
        temp = temp.replace(']','').replace('\'', '')
        pdf.write(temp + '\\\\\n')
#############################
    pdf.write('\\hline\n')
    pdf.write('\\end{tabular}\n')
    pdf.write('\\end{center}\n')
    pdf.write('\\end{document}\n')
    pdf.close()

def usage():
    """
        Function prints the usage message for this script.
    """
    print "usage: print_db.sh <database_name> [-n|-r] [-n|-r] [<field_name>]"
    sys.exit(1)

def getListAttr(dbName):
    p = subprocess.Popen("./find_template_file.py", stdout=subprocess.PIPE)
    tempDef = str(p.communicate()[0]).rstrip('\n')
    
    if (tempDef == None):
        print "Template definition file does not exist. Exiting..."
        sys.exit(2)

    dbType = dbName[:-3]
    templateType = None
    with open("databases.txt") as f:
        for line in f:
            templine = line.split()
            if templine[0] == dbType:
                templateType = templine[1]

    with open(tempDef) as f:
        for line in f:
            tempstr = line.split()
            if tempstr[0] == templateType:
                del tempstr[0]
                return tempstr



def genDictList(dbName, listFlags, fieldIndex):
    """
        Function generates an list of dictionaries based on the database 
        specified, and if any flags are set it sorts the data based on the flags.
    """
    listAttr = getListAttr(dbName)
    listDict = []
    with open(dbName) as f:
        for line in f:
            dataDict = OrderedDict({})
            templine = line.split()
            for attr in listAttr:
                dataDict.update({attr:templine[listAttr.index(attr)]})
            listDict.append(dataDict)
    index = fieldIndex
    ########## find index of field if field was specified in command args
    print index
    print "==============================="
    if len(listFlags) == 0:
        listDict = sorted(listDict, key=lambda i: i.values()[index])
    elif 'r' in listFlags:
        listDict = sorted(listDict, key=lambda i: i.values()[index], reverse=True)
    elif 'n' in listFlags:
        listDict = sorted(listDict, key=lambda i: int(i.values()[index]))
    else:
        listDict = sorted(listDict, key=lambda i: i.values()[index])
    
    return listDict


def cleanup():
    """
        Function cleans up temporary files that were made during the
        generation of the pdf file.
    """
    os.remove("tmp.tex")
    os.remove("tmp.pdf")
    os.remove("tmp.log")
    os.remove("tmp.aux")

def getFieldIndex(dbname, targetField):
    """
        Function gets index of target field.
    """
    p = subprocess.Popen("./find_template_file.py", stdout=subprocess.PIPE)
    tempDef = str(p.communicate()[0]).rstrip('\n')

    if (tempDef == None):
        print "Template definition file does not exist. Exiting..."
        sys.exit(2)

    index = 0
    dbname = dbname.replace('.db', '')
    with open(tempDef) as f:
        for line in f:
            templine = line.split()
            if templine[0] == dbname:
                index = templine.index(targetField)
                return index
    return index

def main(argv):
    """
        Entry point into the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("databasename")
    parser.add_argument("-n", help="sort numerically", action="store_true")
    parser.add_argument("-r", help="sort in reverse", action="store_true")

    parser.add_argument("-f", "--field", default=None, type=str, help="field to sort on")
    
    args = parser.parse_args()

    listFlags = []
    fieldIndex = 0

    if args.n:
        listFlags.append('n')
    elif args.r:
        listFlags.append('r')
    
    if args.field != None:
        fieldIndex = getFieldIndex(args.databasename, args.field)
    if len(argv) < 2:
        usage()
    else:
        listDict = genDictList(args.databasename, listFlags, fieldIndex)
        makeLatexFile(args.databasename, listDict)
        call(["pdflatex", "tmp.tex"])
        call(["okular", "tmp.pdf"])
        cleanup()

main(sys.argv)
