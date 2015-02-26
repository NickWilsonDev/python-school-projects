#! /usr/bin/python

"""
    @author Nick Wilson
    @version 3.29.14

    Script reads from file specified and prints out the unique words
    encountered, how many times the word was encountered, and on what lines
    the word was found. Words should start with a letter but after that they
    can contain letters, numbers and hyphens. if a word appears on a line more
    than once the script will just print out that line number once.
    example:
        "and:     1  times, lines: 2"

    Assumptions
        files have correct read permissions and exist
    
    Exit codes
        0 - successful exit
        1 - no file specified
"""
import sys, re, string

class Word:
    """
        Class represents a word, and should make the job easier of keeping
        track of what lines each word appeared in without having to read the
        file multiple times.
    """
    def __init__(self, name, lineNum):
        self.name      = name.rstrip('\n')
        self.occurence = 1
        self.listOfLines = []
        self.listOfLines.append(lineNum)

    def incOccurrence(self, lineNum):
        self.occurence = self.occurence + 1
        if lineNum not in self.listOfLines:
            self.listOfLines.append(lineNum)

def printResults(listWords):
    """
        Function prints out the data in an organized manner.
    """
    width = 0
    for word in listWords:
        if len(word.name) > width:
            width = len(word.name)
    for word in listWords:
        lstring = str(word.listOfLines).replace('[','').replace(']','')
        print '%s: %d times, lines: %s' % (word.name.rjust(width), 
                word.occurence, lstring)


def contains(listWords, target):
    """
        Function traverses list of objects and tests if any of the objects
        contain the target word.
    """
    wordObj = None
    for i in listWords:
        if i.name == target:
            wordObj = i
            break
    return wordObj

def stripPunctuation(stri):
    """
        Function removes puncuation from string and then returns modified
        string.
    """
    for char in string.punctuation:
        stri = re.sub(r'[\W]+', ' ', stri) 

    return stri

def readFile(filename):
    """
        Function reads file word by word, builds a list of unique words, and 
        returns that list of word objects. Words may not begin with a number
        and must be at least two characters or more.
    """
    listOfWords = []
    currentLine = 1
    f = open(filename, "r")
    for line in f:
        line = stripPunctuation(line)
        for word in line.split():
            word = word.lower()
            if len(word) > 1:
                if not word[0].isdigit():
                    tempObj = contains(listOfWords, word)
                    if tempObj != None:
                        tempObj.incOccurrence(currentLine)
                    else:
                        temp = Word(word, currentLine)
                        listOfWords.append(temp)
        currentLine = currentLine + 1
    return listOfWords

def main(argv):
    """
        The main function provides an entry point into the program, it tests
        the command line arguments and calls the appropriate functions to 
        produce the desired output for this program.
    """
    if len(argv) == 1:
        print "Usage is pyIndex.py <file>"
        sys.exit(1)
    else:
        listOfWords = readFile(sys.argv[1])
# this line performs a sort on the list of objects by the attribute 'name'
        listOfWords.sort(key = lambda x: x.name)
        printResults(listOfWords)

main(sys.argv)
