#! /usr/bin/python

"""
    @author Nick Wilson
    @version 11.20.13

    Topological.py
    File contains functions, that when used with the Vertex class enable the
    reading of a file containing relationships describing a directed acyclic
    graph. A topological sort can then be performed on this graph and all
    the orderings are printed out.
"""

import sys
import copy
import Vertex

def genVertexList(filename):
    """ Generate a unique listing of all the vertices.

    Args:
        filename: A string that is the name of the file to be opened.

    Returns:
        vList: A list containing all the vertices defined in the input file.
    """
    fo = open(filename, "r")
    pre_list = []
    for line in fo:
        line.split()
        for word in line:
            pre_list.append(word)
    fo.close()
    ver_list = list(set(pre_list))

    vList = list()
    for node in ver_list:
            newNode = Vertex.Vertex(node)
            vList.append(newNode)
            vList = [x for x in vList if x.name.isalnum()]
    return vList

def popVertexList(vList, filename):
    """ Populates the adjacency lists in each of the vertices.

    Args:
        vList: A list of all the vertices.
        filename: String that is the name of the file to be read.
    """

    fo = open(filename, "r")
    for line in fo:
        line.split()
        word1 = line[0]
        word2 = line[2]
        for node2 in vList:
            if (node2.name == word2):
                node = node2
                break
        node.addToList(word1)
    fo.close()

    vList = [x for x in vList if x.name.isalnum()]

def printList(vList):
    """ Prints the vertex name and its adjacency list for every vertex in the
        list. Was useful for debugging purposes.

    Args:
        vList: A list of vertices to be printed.
    """

    for node in vList:
        print("nodename __%c__" % node.name)
        print 'adjlist == %'
        print node.adList

def getRoots(vList):
    """ Returns a list of vertices that have empty adjacent lists.

    Args:
        vList: A list of vertices.

    Returns:
        rootlist: A list of vertices that have empty adjacency lists.
    """
    rootlist = list()
    for node in vList:
        if not node.adList:
            rootlist.append(node)
    return rootlist

def removeRoot(vList, nodeName):
    """ Remove a specified node from a specified list of nodes.

    Args:
        vList: A list of vertices.
        nodeName: A string containing the name of the node we wish to remove.

    Returns:
        newlist: A list of vertices without the one that was removed.
    """
    newList = [x for x in vList if x.name != nodeName]
    return newList

def cloneList(vList):
    """ Simply makes a deep copy of a list of Vertices. """
    clone = copy.deepcopy(vList)
    return clone

def updateDepList(updatedList, nodeName):
    """ Updates the adjacency lists inside every Node in the vertex list.

    Args:
        updatedList: A list of vertices.
        nodeName: The name of the Node that will be removed.

    Returns:
        updatedList: A list of vertices with updated adjacency lists.
    """
    for node in updatedList:
        node.remove(nodeName)
    return updatedList

def topSort(takenVert, vList, totalVert):
    """ Perform a topological sort.

    This function is basically a loop that executes recursive calls for every
    iteration of the loop. It provides new "copies" of the important data,
    such as an updated list of verteces and already "visited" vertices. When
    the base case for the recursion is met it prints out the list of taken
    vertices (topological ordering), and then continues through the iterative
    loop.

    Args:
        takenVert: A list of names of vertices.
        vList: A vertex list.
        totalVert: List containing every vertex from the original graph.
    """

    if (len(takenVert) == totalVert):
        print "an ordering is %s" % str(takenVert)
    else:
        rootList = getRoots(vList)
        unusedRoots = [x for x in rootList if x.name not in takenVert]
        for node in unusedRoots:#node is an actual vertex node
            newList = cloneList(vList)
            newTaken = cloneList(takenVert)
            newTaken.append(node.name)
            newList = removeRoot(newList, node)
            newList = updateDepList(newList, node.name)
            topSort(newTaken, newList, totalVert)

def main(argv):
    """ Check usage and set every thing up then make the call to topSort() 
        function.

    Checks the command line arguments, if incorrect print usage message and
    exit. Otherwise call proper functions to make and populate the vertex
    list. Then call topSort().

    Args:
        argv: The command line arguments.
    """

    if len(sys.argv) != 2:
        print 'Usage is python Topological.py <input.txt>'
        sys.exit()
    else:
        filename = argv[1]
        takenVert = list()
        vList = genVertexList(filename)
        popVertexList(vList, filename)
        vList = [x for x in vList if x.name.isalnum()]
        totalVert = len(vList)
        topSort(takenVert, vList, totalVert)

main(sys.argv)
