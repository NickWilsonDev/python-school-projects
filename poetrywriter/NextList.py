#! /usr/bin/env python
# @author Nick Wilson
# @version 9.2.13
# NextList.py

import NextNode, sys

# NextList.py - This file contains everything needed to make the NextList
#               that will be used in the poetry writer.

# NextList - this class will allow the use of the linked list data structure
#              in the poetry writer program
class NextList:
    #constructor
    def __init__(self):
        self.head = None
        self.current = None

    #AddNode - method that adds a node to the nextlist
    #
    #@param data     - contains the word
    #       mainlist - overall data structure 
    def AddNode(self, data, mainlist):
        newnode = NextNode.NextNode(data, mainlist)

        if self.head == None:
            self.head = newnode
            self.current = newnode
        else:
            self.current.SetLink(newnode)
            self.current = newnode

    #Find - method finds and returns the node that contains the data that was
    #       passed in as a parameter
    #
    #@param data - the word that will be in the node we are seeking
    def Find(self, data):
        temp = self.head
        
        while temp != None:
            if temp.data == data:
                return temp
            temp = temp.link

    #Check - method finds the node that contains the data that is passed in as
    #        a parameter, returns true if the node exists and false otherwise
    #
    #@param data - word that we are seeking
    def Check(self, data):
        temp = self.head
        while temp != None:
            if temp.data == data:
                return True
            temp = temp.link
        return False

    #PrintList - method prints out the nextlist nodes, useful for debugging
    def PrintList(self):
        temp = self.head
        tempString = ''
        while temp != None:
            tempString = tempString + ' ' + temp.data + ' %d' % (temp.ratio)
            temp = temp.link

        print tempString
        sys.stdout.write('\n')

    #SetProb - method sets the probabillities for all the nodes in the 
    #          nextlist
    def SetProb(self):
        total = 0 
        temp = self.head
        while temp != None:
            total = float(total) + float(temp.occurence)
            temp = temp.link

        temp = self.head
        while temp != None:
            temp.ratio = float(float(temp.occurence) / float(total))
            temp = temp.link

        currentTotal = 0
        temp = self.head
        while temp != None:
            currentTotal = float(currentTotal) + float(temp.ratio)
            temp.ratio = currentTotal
            temp = temp.link

