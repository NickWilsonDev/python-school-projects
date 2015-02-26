#! /usr/bin/env python
# @author Nick Wilson
# @version 9.2.13
# NextNode.py

import NextList, MainList

# NextNode - each node will have four fields
#        data      - will be the word or punctuation that is read from the txt
#                    file
#        occurence - the number of occurences that of the word inside the
#                    txt file
#        link      - link to the next node in list
#        out       - link to the corresponding node in the main list
#        ratio     - ratio describing probabillity of this word appearing
class NextNode:
    def __init__(self, data, mainlist):
        self.data      = data
        self.occurence = 1
        self.link      = None
        self.out       = mainlist.Find(data)
        self.ratio     = None

    def Increment(self):
        self.occurence = self.occurence + 1

    def SetLink(self, link):
        self.link = link

    def SetOut(self, out):
        if self.out is None:
            self.out = out

    def SetRatio(self, ratio):
        self.ratio = ratio
