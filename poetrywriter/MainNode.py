#! /usr/bin/env python
# @author Nick Wilson
# @version 9.2.13
# MainNode.py

import NextList

# MainNode - each node will have four fields
#        data      - will be the word or punctuation that is read from the txt
#                    file
#        occurence - the number of occurences that of the word inside the
#                    txt file
#        link      - link to the next node in list
#        out       - link to the corresponding node in other list
#        ratio     - number describing ratio of how often this word appears
class Node:
    def __init__(self, data):
        self.data      = data
        self.occurence = 1
        self.link      = None
        self.out       = NextList.NextList()
        self.ratio     = None

    def Increment(self):
        self.occurence = self.occurence + 1

    def SetLink(self, link):
        self.link = link

    def SetRatio(self, ratio):
        self.ratio = ratio
