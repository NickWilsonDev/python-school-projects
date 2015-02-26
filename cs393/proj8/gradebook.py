#! /usr/bin/python
"""
    @author Nick Wilson
    @version 2.24.14

    gradebook.py

    This script will read in student and grade information from three 
    different files, calculates an average, and writes a report out to a file.
    There are three input files called "students.txt", "items.txt", and 
    "scores.txt".

    Exit Codes

    3 - total weight of assignments did not sum up to 100
"""
import os.path, sys
from operator import itemgetter, attrgetter
class Item:
    def add_attr(self, name, value):
        """
            Method should allow dynamic adding of attributes at runtime, this
            is for when the item.txt file is read then an instance of this
            object will contain all the "assignments" for the course. And I
            wanted to try "duckpunching?"
        """
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        setattr(self.__class__, name, property(fget, fset))
        setattr(self, '_' + name, value)

class Student:
    def __init__(self, first, last, ID):
        self.first   = first
        self.last    = last
        self.ID      = ID

def checkFile(filename):
    """
        Function checks whether file exists and if it does it is then checked
        for read permissions.
    """
    if os.path.isfile(filename):
        if os.access(filename, os.R_OK):
            emptystring = ""
        else:
            print "The file % does not have read permissions" % filename
            sys.exit(2)
    else:
        print "The file % does not exist" % filename
        sys.exit(1)

def popStudentList():
    """
        Function reads the "students.txt", parses the file, and generates a 
        list of student objects.
    """
    studentList = []
    with open('students.txt') as f:
        for line in f:
            tempList = line.split(', ')
            detailList = tempList[1].split(':')
            studentList.append(Student(detailList[0], tempList[0], int(detailList[1])))
    studentList = sorted(studentList, key=attrgetter('last', 'first'))
    return studentList

def setItems():
    """
        Function reads items.txt and dynamically adds attributes to the item
        object, this object can then later be used to determine averages. Also
        checks to see if total value of all assignments is equal to 100
    """
    totalValue = 0
    item = Item()
    with open('items.txt') as f:
        for line in f:
            tupl = line.split()
            setattr(item, str(tupl[0]), (int(tupl[-1]) / 100.0))
            totalValue += (int(tupl[-1]))
        if totalValue != 100:
            print "The total value of assignments does not equal 100"
            sys.exit(3)
    return item

def loadScores(studentlist):
    """
        Function reads the scores.txt file and loads data into fields for the
        appropriate student object.
    """
    with open('scores2.txt') as f:
        for line in f:
            tempList = line.split()
            sId = int(tempList[0])
            tempObj = next((kid for kid in studentlist if kid.ID == sId), None)
            if hasattr(tempObj, str(tempList[1])):
                setattr(tempObj, str(tempList[1]), int(tempList[2]))

def getWidth(studentList):
    width = 0
    for kid in studentList:
        if (len(kid.first) + len(kid.last) + 2) > width:
            width = len(kid.first) + len(kid.last) + 2
    return width

def dashString(studentList):
    listOfGrades = vars(studentList[0]).keys()
    listOfGrades.remove("first")
    listOfGrades.remove("last")
    listOfGrades.remove("average")

    width = getWidth(studentList)
    dashstr = '-' * width + (" -----" * len(listOfGrades)) + ' ' + '-' * 7
    return dashstr

def headerString(studentList):
    listOfGrades = vars(studentList[0]).keys()
    listOfGrades.remove("first")
    listOfGrades.remove("last")
    listOfGrades.remove("average")

    width = getWidth(studentList)
    
    listAttr = vars(studentList[0]).keys()
    listAttr.remove("first")
    listAttr.remove("last")
    listAttr.remove("ID")
    listAttr.remove("average")
    listAttr = sorted(listAttr)
    listAttr.append("average")


    headerstr = "Name" + ' ' * (width - len("Name")) + " StuID "
    headerstr += str(listAttr).replace('[', '').replace(']', '')
    headerstr = headerstr.replace('\'', '').replace(',', '')

    return headerstr

def writeReport(studentList):
    """
        Function writes report.txt file with appropriate data contained in the
        list of students provided as a paremeter.
    """
    dashstr = dashString(studentList)
    headerstr = headerString(studentList)
    attrList = vars(studentList[0]).keys()
    for temp in ("last", "first", "average", "ID"):
        attrList.remove(temp)

    attrList = sorted(attrList)
    width = getWidth(studentList)
    averagestr = "average" + ' ' * (width - len("average") + 7)

    f = open('report.txt', 'w')
    f.write(headerstr + '\n')
    f.write(dashstr + '\n')

    for kid in studentList:
        namelength = len(kid.last + kid.first) + 2
        kidstr = kid.last + ", " + kid.first + ' ' * (width - namelength) + ' '
        kidstr += str(kid.ID)
        for temp in attrList:
            if getattr(kid, temp) != None:
                kidstr += ' ' * (5 - len(str(getattr(kid, temp))) + 1)
                kidstr += str(getattr(kid, temp))
            else:
                kidstr += ' ' * 6
        kidstr += ' ' * (7 - len(str(kid.average)) + 1)
        kidstr += str(kid.average)
        f.write(kidstr + '\n')

    attrList.append("average")
    for temp in attrList:
        average = 0
        tempCount = 0
        for kid in studentList:
            if getattr(kid, temp) != None:
                average += getattr(kid, temp)
                tempCount += 1
        if tempCount == 0:
            average = 0
        else:
            average = average / tempCount
        if temp != "average":
            averagestr += ' ' * (5 - len(str(average))) + str(average) + ' '
        else:
            averagestr += ' ' * (7 - len(str(average))) + str(average)

    f.write(dashstr + '\n')
    f.write(averagestr + '\n')
    f.close()

def calcAvg(studentList, item):
    """
        Function calculates averages for all the students in the list using
        the item object whose attributes contain the weights for grading.
    """
    gradeList = vars(studentList[0]).keys()
    for temp in ("last", "first", "ID", "average"):
        gradeList.remove(temp)
    gradeList = sorted(gradeList)

    for kid in studentList:
        average = 0
        numAttr = 0
        for temp in gradeList:
            if getattr(kid, temp) != None:
                average += getattr(kid, temp) * getattr(item, temp)
                numAttr += 1
        setattr(kid, "average", average)

def giveStudentsItems(students, itemList):
    """
        Function updates student objects in list of students to have every
        attribute that is contained in itemList, along with an "average",
        attribute
    """
    itemList.append("average")
    for kid in students:
        for item in itemList:
            setattr(kid, str(item), None)

def main():
    checkFile("students.txt")
    checkFile("scores.txt")
    checkFile("items.txt")
    item = setItems()
    itemList = vars(item).keys()
    students = popStudentList()
    giveStudentsItems(students, itemList)

    loadScores(students)
    calcAvg(students, item)
    print "about to write report.txt"
    writeReport(students)

main()
