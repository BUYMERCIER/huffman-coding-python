__license__ = 'GolluM & Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2017-04-04'

"""
Huffman homework
2017
@author: corentin.mercier
"""


##################################################
# Warning:
# This file has been cleared from long doctrings
# See the complete specifications online.


from AlgoPy import binTree
from AlgoPy import heap


################################################################################
## COMPRESSION

def buildFrequencyList(dataIN): # Working
    """
    Builds a tuple list of the character frequencies in the input.
    """
    table = []
    _table = []
    for letter in dataIN:
        if letter not in _table:
            _table.append(letter)
            count = 0
            for i in range(len(dataIN)):
                if dataIN[i] == letter:
                    count += 1
            table.append((count, letter))
    return table

################################################################################
## BUILD THE TREE

def buildHuffmanTree(inputList): # Working
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    This is the hat function
    """
    l=[]
    for i in inputList:
        T = binTree.BinTree(i,None,None)
        l.append(T)
    tree = _buildHuffmanTree(l,0)
    return tree

def quickSort(L):
    """
    Reversed quickSort
    """
    less = []
    pivotList = []
    more = []
    if (L==[]):
        return L
    else:
        pivot = L[0].key[0]
        for i in L:
            if i.key[0] > pivot:
                more.append(i)
            elif i.key[0] < pivot:
                less.append(i)
            else:
                pivotList.append(i)
        less = quickSort(less)
        more = quickSort(more)
        return more + pivotList + less

def _buildHuffmanTree(L,x):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    if(len(L)<=1):
        return L[0]
    elif(L==[0]):
        return None
    L = quickSort(L)
    right = L.pop()
    left = L.pop()
    x += 1
    T = binTree.BinTree((right.key[0]+left.key[0],x),left,right)
    T.left.key = left.key[1]
    T.right.key = right.key[1]
    L.append(T)
    return _buildHuffmanTree(L, x)

################################################################################
## ENCODE DATA USING THE TREE

def encodeData(dataIN, huffmanTree): # Working
    """
    Encodes the input string to its binary string representation.
    """
    dic = codeDict(huffmanTree)
    string = ""
    for i in dataIN:
        for n in range(len(dic)):
            if i == dic[n][0]:
                string += dic[n][1]
    return string

def codeDict(tree):
    """
    Returns a list of tuples (letter,corresponding code)
    """
    l = []
    def dfsInfix(tree, string):
        '''
        Depth-first traversal
        Prints keys in inorder
        '''
        if tree != None:
            dfsInfix(tree.left, string + '0')
            if tree.left == None and tree.right == None:
              l.append((tree.key, string))
            dfsInfix(tree.right, string + '1')
    dfsInfix(tree, "")
    return l

################################################################################

def encodeTree(huffmanTree): # Working
    """
    Encodes a huffman tree to its binary representation
    """
    dic = codeDict(huffmanTree)
    code = ""
    for item in dic:
        code = code + remove1(item[1]) + "1" + letterToBin(item[0])
    return code

def remove1(string):
    """
    Removes all the 1s from a given string, but not just that ;)
    """
    string = str(string)
    ret = ""
    for x in string:
        if x == "1":
            ret = ""
        else:
            ret += "0"
    return ret

def letterToBin(letter):
    """
    Converts a letter into its binary representation
    """
    i = ord(letter)
    if i == 0:
        return "0"
    string = ""
    while i != 0:
        string = str(i % 2) + string
        i = i // 2
    if len(string) == 7:
        string = "0" + string
    return string

################################################################################

def toBinary(dataIN): # Working
    """
    Compresses a string containing binary code to its real binary value.
    """
    s = ""
    count = 0
    i = 0
    length = len(dataIN)
    while  count  < length:
    	mult = 1
    	number = 0
    	if count + 7 < length:
    		i = count + 7
    		while i>=count:
    			number = number + int(dataIN[i]) * mult
    			i = i - 1
    			mult = mult * 2
    	else:
    		i = length - 1
    		while i >= count:
    			number = number + int(dataIN[i]) * mult
    			i = i - 1
    			mult = mult * 2
    	s = s + chr(number)
    	count = count + 8
    return (s, count - length)

################################################################################

def compress(dataIn): # Working
    """
    The main function that makes the whole compression process.
    """
    freq = buildFrequencyList(dataIn)
    tree = buildHuffmanTree(freq)
    encodedData = encodeData(string, tree)
    encodedTree = encodeTree(tree)
    return (toBinary(encodedData), toBinary(encodedTree))


################################################################################
## DECOMPRESSION

def decodeData(dataIN, huffmanTree): # Working
    """
    Decode a string using the corresponding huffman tree into something more
    readable.
    """
    code = codeDict(huffmanTree)
    part = ""
    ret = ""
    for thing in dataIN:
        part += thing
        for item in code:
            if part == item[1]:
                ret += item[0]
                part = ""
    return ret

################################################################################

def decodeTree(dataIN): # Working
    """
    Decodes a huffman tree from its binary representation
    """
    lc = []
    lc.append(0)
    def _decodeTree (data, T, c):
        if c[0] < len(data):
            if data[c[0]] == '0':
                T = binTree.BinTree(c[0], None, None)
                c[0] += 1
                T.left = _decodeTree(data, T.left, c)
                T.right = _decodeTree(data, T.right, c)
            else:
                c[0] += 1
                c2 = c[0]
                oct = ""
                for i in range (c2, c2+8):
                    oct += data[c[0]]
                    c[0] += 1
                T = binTree.BinTree((_byteToChar(oct), 1), None, None)
            return T
    T = _decodeTree(dataIN, binTree.BinTree(None, None, None), lc)
    return beautify(T)

def _byteToChar(byte):
    """
    Converts a byte into a character
    """
    byteInt = 0
    for i in range(len(byte)):
        byteInt += (2**(len(byte)-1-i))*(ord(byte[i])-48)
    return(chr(byteInt))

def beautify(tree):
    '''
    Depth-first traversal
    Adds keys in inorder
    '''
    if tree != None:
        beautify(tree.left)
        if tree.left == None and tree.right == None:
            tree.key = tree.key[0]
        beautify(tree.right)
    return tree

################################################################################

def fromBinary (dataIN, align): # Working
    """
    Retrieve a string containing binary code from its real binary value
    (inverse of :func:`toBinary`).
    """
    _bin = ""
    for i in range (len(dataIN)-1):
        _bin += _CharToBin(dataIN[i])
    lastOct =  _CharToBin(dataIN[len(dataIN)-1])
    for i in range (align , len(lastOct)):
        _bin += lastOct[i]
    return _bin

def _CharToBin(c):
    """
    Converts a character to its binary form
    """
    Cint = ord(c)
    _bin = ""
    while Cint != 0:
        _bin = str(Cint % 2) + _bin
        Cint = Cint // 2
    while len(_bin) < 8:
        _bin = '0' + _bin
    return _bin

################################################################################

def decompress(data, dataAlign, tree, treeAlign): # Working
    """
    The whole decompression process.
    """
    tree = fromBinary(tree, treeAlign)
    code = fromBinary(data, dataAlign)
    newtree = decodeTree(tree)
    final = decodeData(code, newtree)
    return final

################################################################################
