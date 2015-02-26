#! /usr/bin/python
"""
    @author Nick Wilson
    @version 11.20.13

    File defines the Vertex class.
"""

class Vertex:
    """ Class basically defines a vertex from a graph and also several usefull
        methods for it.
    """

    def __init__(self, name):
        """ Initialize a Vertex with a name. Also initializes an empty
            adjacency list for the Vertex. """
        self.name   = name
        self.adList = list()

    def addToList(self, node):
        """ Adds a Vertex name to an adjacency list. """
        self.adList.append(node)
        return

    def getList(self):
        """ Return Nodes' adjacency list. """
        return self.adList

    def contains(self, node):
        """ Check and see if Nodes' adjacency list contains the specified
            node. """
        if node in self.adList:
            return True
        else:
            return False

    def remove(self, node):
        """ Remove a specified node from the nodes' adjacency list. """
        if node in self.adList:
            self.adList.remove(node)
        else:
            return
