import heapq
import os

class BinaryTreeNode:
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq
    

def convertintobytes(paddedenctext):
    array = []
    for i in range(0, len(paddedenctext), 8):
        byte = paddedenctext[i: i + 8]
        array.append(int(byte, 2))
    return array


class HuffmanCoding:

    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.revcodes = {}

    def makefreqdict(self, text):
        freqdict = {}
        for char in text:
            if char not in freqdict:
                freqdict[char] = 0
            freqdict[char] += 1
        return freqdict

    def buildheap(self, freqdict):
        for key in freqdict:
            freq = freqdict[key]
            binary_tree_nodes = BinaryTreeNode(key, freq)
            heapq.heappush(self.heap, binary_tree_nodes)

    def buildtree(self):
        while len(self.heap) > 1:
            binarytreenode1 = heapq.heappop(self.heap)
            binarytreenode2 = heapq.heappop(self.heap)
            freqsum = binarytreenode2.freq + binarytreenode1.freq
            newnode = BinaryTreeNode(None, freqsum)
            newnode.left = binarytreenode1
            newnode.right = binarytreenode2
            heapq.heappush(self.heap, newnode)
        return

    def buildcodeshelper(self, root, currbits):
        if root is None:
            return
        if root.value is not None:
            self.codes[root.value] = currbits
            self.revcodes[currbits] = root.value

        self.buildcodeshelper(root.left, currbits + '0')
        self.buildcodeshelper(root.right, currbits + '1')

    def buildcodes(self):
        root = heapq.heappop(self.heap)
        self.buildcodeshelper(root, '')

        # if root.value is not None:
        #     self.codes[root.value] = currbits



    def getencodedtext(self, text):
        encodedtext = ''
        for char in text:
            encodedtext += self.codes[char]
        return encodedtext

    def getpaddedenctext(self, encodedtext):
        extra = 8 - (len(encodedtext) % 8)
        for i in range(extra):
            encodedtext += '0'
        paddedinfo = '{0:08b}'.format(extra)

        paddedencodedtext = paddedinfo + encodedtext
        return paddedencodedtext

    @property
    def compress(self):

        filename, fileext = os.path.splitext(self.path)
        output_path = filename + '.bin'

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()

            text = text.rstrip()

            freq_dict = self.makefreqdict(text)

            self.buildheap(freq_dict)

            self.buildtree()

            self.buildcodes()

            encodedtext = self.getencodedtext(text)

            padencodedtext = self.getpaddedenctext(encodedtext)

            bytesarray = convertintobytes(padencodedtext)

            finalbytes = bytes(bytesarray)

            output.write(finalbytes)

        print('compressed')
        return output_path

    def removepadding(self, text):
        paddedinfo = text[:8]
        extrapadding = int(paddedinfo, 2)

        actualtext = text[8:]
        textafterpaddingremoved = actualtext[:-1 * extrapadding]
        return textafterpaddingremoved

    def decodetext(self, text):
        decodedtext = ''
        currentbits = ''
        for bits in text:
            currentbits += bits
            if currentbits in self.revcodes:
                character = self.revcodes[currentbits]
                decodedtext += character
                currentbits = ''
        return decodedtext

    def decompress(self, inputpath):
        filename, fileext = os.path.splitext(self.path)
        output_path = filename + 'decompressed' + '.txt'
        with open(inputpath, 'rb') as file, open(output_path, 'w') as output:
            bitstring = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bitstring += bits
                byte = file.read(1)
            actualtext = self.removepadding(bitstring)
            decompressedtext = self.decodetext(actualtext)
            output.write(decompressedtext)


path = r'C:\Users\hp\Desktop\text.txt '
h = HuffmanCoding(path)
outputpath = h.compress
h.decompress(outputpath)
