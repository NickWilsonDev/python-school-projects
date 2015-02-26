#! /usr/bin/env python
# @author Nick Wilson
# @version 9.2.13
# 
# PoetryWriter.py
# This script reads in a text file, stores the words in a linked list, and
# rearranges the words into a 'sort of' poem based on the command line args.

import MainList, NextList, sys, random

# popNextList - this method adds a node to the nextlist of the appropriate
#               node in the mainlist depending on the the two words that were
#               passed in as parameters
#
# @param  prev - String that is the previous word
#         word - String that is the current word(directly after prev)
#         mainlist - the overall data structure that contains words read in
#                    from file 
def popNextList(prev, word, mainlist):
    # populate next list for each mainNode
    if prev != '':
        temp = mainlist.Find(prev)
        if temp == None:
            return
        elif temp.out == None:
            temp.out = NextList.NextList()
            temp.out.AddNode(word, mainlist)
        else:
            test = temp.out.Check(word)
            if test == True:
                tempNextNode = temp.out.Find(word)
                tempNextNode.Increment()
            else:
                temp.out.AddNode(word, mainlist)
    return

# addToMain - method adds a node to the mainlist
#
# @param prev - String that contains the previous word
#        word - String that contains the current word
#        mainlist - the overall data structure that contains the words read in
#                   from the txt file
def addToMain(prev, word, mainlist):
    if word != ' ' and word != '':
        if mainlist.Check(word) == True:
            temp = mainlist.Find(word)
            temp.Increment()
            popNextList(prev, word, mainlist)
        elif mainlist.Check(word) == False:
            mainlist.AddNode(word)
            popNextList(prev, word, mainlist)
        return
    else:
        return

# load - method loads up the specified file and reads in the words, and calls
#        the appropriate helper methods to update the mainlist data structure
#
# @param mainlist - the overall data structure
#        filename - the name of the file that will be read
def load(mainlist, filename):
    word  = ''
    prev  = ''
    first = ''
    last  = ''

    fo = open(filename, "r")
    for letter in open(filename).read():

        if letter == ',':
            addToMain(prev, word, mainlist)
            prev = word
            word = ','

        elif letter == '!':
            addToMain(prev, word, mainlist)
            prev = word
            word = '!'
            
        elif letter == '?':
            addToMain(prev, word, mainlist)
            prev = word
            word = '?'

        elif letter == ';':
            addToMain(prev, word, mainlist)
            prev = word
            word = ';'

        elif letter == '.':
            addToMain(prev, word, mainlist)
            prev = word
            word = '.'

        elif letter == ' ' or letter == '\n':

            if first == '':
                first = word
            if mainlist.Check(word):
                temp = mainlist.Find(word)
                temp.Increment()
                popNextList(prev, word, mainlist)
            else:
                if word != ' ' and word != '':    
                    mainlist.AddNode(word)
                    popNextList(prev, word, mainlist)
            prev = word
            word = ''

        else:
            word = word + letter

    if last == '':
        last = prev

    fo.close()
        
    # for the purpose of the poetry writer we set the last node(word)
    # to link to the first node(word)
    popNextList(last, first, mainlist)
    return

# write - function performs most of the work of the PoetryWriter.py
#         it takes as parameters the number of stanzas, lines, and words.
#         It also takes a pointer to the mainlist where the data from the 
#         original poem is stored
#
# @param numstanza - number of stanzas
#        numlines  - number of lines
#        numwords  - number of words
#        mainlist  - the overall list that has been generated, this list 
#                    stores all the words from the input file
def write(numstanza, numlines, numwords, mainlist):
    rand = random.uniform(0, 1)
    temp = mainlist.head
    currentWord = ''

    while temp != None:
        if rand <= temp.ratio:
            currentWord = temp.data
            break
        temp = temp.link
    
    total_stanzas = 0
    total_lines   = 0
    total_words   = 0

    while total_stanzas != numstanza:
        while total_lines != numlines:
            while total_words != numwords:
                blueWord = '\033[94m' + currentWord + '\033[0m\033[24m'
                sys.stdout.write(blueWord)
                #sys.stdout.write(currentWord)
                currentWord = getNextWord(mainlist, currentWord)
                sys.stdout.write(' ')
                total_words = total_words + 1
            print ''
            total_lines = total_lines + 1
            total_words = 0
        print ''
        total_stanzas = total_stanzas + 1
        total_lines = 0
    return

# getNextWord - function generates a random number then finds the word in the
#               mainlist, once found the random is compared with the ratios in
#               the nextlist and the next word is chosen
#
# @param mainlist - the overall data structure (LinkedList)
#        word     - String that contains the word that the next word will be 
#                   based on
def getNextWord(mainlist, word):
    rando = random.random()
    temp = mainlist.Find(word)
    tempNextList = temp.out
    tempNextNode = tempNextList.head
    
    while tempNextNode != None:
        if rando < tempNextNode.ratio or rando == tempNextNode.ratio:
            return tempNextNode.data
        tempNextNode = tempNextNode.link

# PoetryWriter.py - This script will take a txt file and several other 
#                    parameters as command line arguments and using these to 
#                    "construct" a new poem
#
# @param - argv - the list of command line arguments
def main(argv):
    if len(argv) != 5:
        msg = '\033[91m'
        msg = msg + 'Usage is PoetryWriter.py <input.txt> <numstanza> <numlines>'
        msg = msg + ' <numwords>\033[0m'
        print msg
        #print 'Usage is PoetryWriter.py <input.txt> <numstanza> <numlines> <numwords>
        sys.exit() #may have to change this to quit() ect

    else:
        filename  = argv[1]
        numstanza = int(argv[2])
        numlines  = int(argv[3])
        numwords  = int(argv[4])
        mainlist  = MainList.MainList()
        load(mainlist, filename)
        mainlist.SetProb()
        write(numstanza, numlines, numwords, mainlist)

main(sys.argv)
