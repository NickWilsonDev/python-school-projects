#! /usr/bin/python
"""
    @author Nick Wilson
    @version 4.24.14

    cache.py
    This script reads data from standard input and produces statistics about a
    cache 'trace' to standard output. The input will contain cache
    configuration information followed by memory references consisting of 
    hexadecimal addresses, one per line.
    
    ::The script should also check that the number of sets does not exceed 8K 
    and the associativity level does not exceed 8

    ::Also check that line size is at least 4 and that the number of sets and
    line size will be a power of two

    ::Cache simulator should use LRU replacement algorithm

    ::Cache is a write-back and write allocate cache

    Exit codes
        0 - success
        1 - line size is not at least 4
        2 - Number of sets is not a power of two
        3 - line size is not a power of two
        4 - Number of sets exceeded 8000
        5 - Set size was greater than 8

"""
import sys, re, math

class CacheBlock:
    """
        Class models a cache block, it will contain a set number of lists.
        These lists represent rows in the cache, and they each are of the
        format ::: [ tag, data , valid bit, dirty bit]
    """
    def __init__(self, setSize):
        """
            Method is the constructor for this class, it will create a 
            multidimensional list the dimensions are specified by the 
            parameter.
            @param
                setSize - how many rows will be in this CacheBlock
        """
        self.cacheSet = [[None for i in xrange(4)] for i in xrange(setSize)]

    def getRow(self, tag):
        """
            Method traverses rows checking for appropriate tag or None
            @param
                tag - a value used to determine what row to return or None
            @return
                targetRow - a row with the matching tag, or None if no row
                            with the proper tag is in the cache block
        """
        targetRow = None
        for tempRow in self.cacheSet:
            if tempRow[0] == tag:
                targetRow = tempRow
        return targetRow

    def getUnallocatedRow(self):
        """
            Method returns a row with a value of "None", if none are found it
            returns -1.
        """
        for tempRow in self.cacheSet:
            if tempRow[0] == None:
                return tempRow
        return -1

    def printCache(self):
        """
            Function prints the rows of this particular cache block, mostly
            used for debugging purposes.
        """
        for tempRow in self.cacheSet:
            print str(tempRow)

def checkPowerTwo(num):
    """
        Function checks to see if the number entered in the parameter is
        a power of two. It came from this website
        "helloacm.com/check-integer-is-the-power-two/"
        @param
            num - integer that will be checked
    """
    if num < 1:
        return False
    return (num & (num - 1)) == 0

def testValues(numSets, setSize, lineSize):
    """
        Function performs various tests and exits with code if one fails.
        @param
            numSets  - number of sets
            setSize  - how big each set is
            lineSize - size of line in each set
    """
    if lineSize < 4:
        print "Line Size is not at least 4. Exiting..."
        sys.exit(1)
    if checkPowerTwo(numSets) == False:
        print "Number of sets is not a power of 2. Exiting..."
        sys.exit(2)
    if checkPowerTwo(lineSize) == False:
        print "Line size is not a power of 2. Exiting..."
        sys.exit(3)
    if numSets > 8000:
        print "Number of sets may not exceed 8000"
        sys.exit(4)
    if setSize > 8:
        print "Set size may not be greater than 8"
        sys.exit(5)

def genCache(numSets, setSize):
    """
        Function generates a fake cache composed of cache blocks in a list.
        @param
            numSets - number of cacheBlocks to make
            setSize - number of rows in each cacheBlock
        @return
            listOfSets - a fake cache composed of CacheBlock objects
    """
    listOfSets = []
    temp = 0
    while temp < numSets:
        cache = CacheBlock(setSize)
        listOfSets.append(cache)
        temp +=1
    return listOfSets

def checkAddress(listSets, index, tag, offset, typeOfAccess):
    """
        Function checks address and determines whether the result is a hit or
        miss, and also the number of Memory references that are needed.
        @param
            listSets     - the fake cache, a list of cacheblock objects
            index        - the index of the cacheblock we desire to check
            tag          - used to determine what "row" in cache block we are
                           checking against
            offset       - also used to determine what "row" to check against
            typeOfAccess - will be "R" or "W"
        @return
            infoList - a list that contains hit/miss in [0] and # of memory
                        references in [1]
    """
    targetBlock = listSets[index]
    flag = "miss"
    memRef = 1
    infoList = []
    row = targetBlock.getRow(tag)

    if typeOfAccess == 'R':
        if row == None:
            row = targetBlock.getUnallocatedRow()
            if row != -1:
                row[0] = tag
                row[2] = 1
                row[3] = 0
            else:
                row = targetBlock.cacheSet[0]
                if row[3] == 1:
                    memRef = 1 
                else:
                    memRef = 1
                row[0] = tag
                row[2] = 1
                row[3] = 0
        else:
            flag = "hit"
            memRef = 0
            row[3] = 1
#row[2] = 0
    else:       ########### typeof access is W
        if row == None:
            row = targetBlock.getUnallocatedRow()
        elif row != None:  #this means a row with the proper tag was found
            flag = "hit"
            memRef = 0
            if row[3] == 0 or row[3] == None:
                row[0] = tag
                row[2] = 1
                row[3] = 1
            elif row[3] == 1: # this means that data is at this cache row but not written to main memory
                print "mem reference 2"
                flag = "miss"
                memRef = 2
                row[0] = tag
                row[2] = 1
                row[3] = 0
        if row != -1:   # empty slot found
            row[0] = tag
            row[2] = 1
            row[3] = 1
        else:
            memRef = 2
            row = targetBlock.cacheSet[0]
            row[0] = tag
#row[2] = 1
            row[3] = 0
            flag = "miss"

    infoList.append(flag)
    infoList.append(memRef)
    return infoList

def printSummary(totalHits, totalMisses, totalAccesses):
    """
        Function prints summary information from testing cache.
        @param
            totalHits     - the total number of hits
            totalMisses   - the total number of misses
            totalAccesses - the total number of accesses
    """
    print "Simulation Summary Statistics"
    print "-----------------------------"
    print "Total hits       : %d" % (totalHits)
    print "Total misses     : %d" % (totalMisses)
    print "Total accesses   : %d" % (totalAccesses)
    print "Hit ratio        : %f" % (float(totalHits) / float(totalAccesses))
    print "Miss ratio       : %f" % (float(totalMisses) / float(totalAccesses))

def printHeader(numSets, setSize, lineSize):
    """
        Function prints header information.
        @param
            numSets - number of sets
            setSize - size of each set
            lineSize - size of each line(row)
    """
    print "Cache Configuration\n"
    print "%d %d-way set associative entries" %(numSets, setSize)
    print "of line size %d bytes" % (lineSize)
    print "Access Address    Tag   Index Offset Result Memrefs"
   
    dashString =  "-" * 6 + " " + "-" * 8 + " " + "-" * 7 + " " + "-" * 5
    dashString += " " + "-" * 6 + " " + "-" * 6 + " " + "-" * 8
    print dashString

def main():
    """
        Function provides the entry point into the program.
    """
    numSets = raw_input("Please enter number of sets: \n" )
    numSets = int(re.findall('\d+', numSets)[0])
    setSize = raw_input("Please enter sizeof sets: \n" )
    setSize = int(re.findall('\d+', setSize)[0])
    lineSize = raw_input("Please enter size of lines: \n" )
    lineSize = int(re.findall('\d+', lineSize)[0])

    testValues(numSets, setSize, lineSize)
    listSets = genCache(numSets, setSize)
    printHeader(numSets, setSize, lineSize)
    totalAccesses = 0
    totalHits     = 0
    totalMisses   = 0
    user_input = ""

    for line in sys.stdin:
        listAttr = line.replace('\n', '').split(':')
        totalAccesses += 1
        """ 
            next instruction formats hex into 32 bit binary string with "0b"
            prefix
        """
        bitString = str(format(int(listAttr[2], 16), '#034b'))
        bitString = bitString.replace(bitString[:2], '')
        """ converts hexadecimal string to binary """
        blockOffsetBitSize = int(math.log(lineSize, 2))
        indexBitSize       = int(math.log(numSets, 2))
        tagBitSize         = lineSize - (blockOffsetBitSize + indexBitSize)
        offset = int(bitString[-( blockOffsetBitSize):], 2)
        bitString = bitString[: -(blockOffsetBitSize)]
        index = int(bitString[-( indexBitSize):], 2)
        bitString = bitString[: -(indexBitSize)]
        tag = int(bitString, 2)

        checkList = checkAddress(listSets, index, tag, offset, listAttr[0])
        if checkList[0] == "hit": totalHits += 1
        else: totalMisses += 1
        print "%s        %s       %d        %d     %d    %s    %d"\
                % (listAttr[0], listAttr[2], tag, index, offset, checkList[0],\
                        checkList[1])
    printSummary(totalHits, totalMisses, totalAccesses)

#for temp in listSets:
#        temp.printCache()


main()
