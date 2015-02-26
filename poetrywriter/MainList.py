#! /usr/bin/env python
# @author Nick Wilson
# @version 9.2.13
# MainList.py

import MainNode

# MainList.py - This file contains everything needed to make the MainList
#               that will be used in the poetry writer.

# MainList - this class will allow the use of the linked list data structure
#              in the poetry writer program
class MainList:
    #constructor
    def __init__(self):
        self.head = None
        self.current = None
        self.tail = None

    #AddNode - method adds a node to the MainList
    #
    #@param data - the word that will be stored in the node
    def AddNode(self, data):
        newnode = MainNode.Node(data)

        if self.head == None:
            self.head = newnode
            self.current = newnode

        else:
            self.current.SetLink(newnode)
            self.current = newnode

        self.tail = self.current
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
        while temp != None:
            print temp.data + ' %d' % (temp.occurence)
            tempNextList = temp.out
            if tempNextList != None:
                print 'nextlist portion =='
                tempNextList.PrintList()

            temp = temp.link

    #SetProb - method sets the probabillities for all the nodes in the          
    #          nextlist   
    def SetProb(self):
        total = 0
        temp = self.head
        while temp != None:
            total = total + temp.occurence
            tempNextList = temp.out
            tempNextList.SetProb()
            temp = temp.link

        temp = self.head
        
        while temp != None:
            temp.ratio = float(float(temp.occurence) / float(total))
            temp = temp.link

        currentTotal = 0
        temp = self.head
        while temp != None:
            currentTotal = currentTotal + temp.ratio
            temp.ratio = currentTotal
            temp = temp.link
