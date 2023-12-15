import array
import math
from sys import argv
import csv

"""
Sandy Marrero Hernandez
Bloom Filter Project 2
"""


##Helper Functions provided by professor
def makeBitArray(bitSize, fill=0):
    intSize = bitSize >> 5  # number of 32 bit integers
    if bitSize & 31:  # if bitSize != (32 * n) add
        intSize += 1  #    a record for stragglers
    if fill == 1:
        fill = 4294967295  # all bits set
    else:
        fill = 0  # all bits cleared

    bitArray = array.array("I")  # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return bitArray

    # testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.


def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return array_name[record] & mask

    # setBit() returns an integer with the bit at 'bit_num' set to 1.


def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return array_name[record]

    # clearBit() returns an integer with the bit at 'bit_num' cleared.


def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return array_name[record]

    # toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.


def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return array_name[record]


"""
    Creates a Bloom filter and processes it using two input files, one which is used to create and fill the positions with and one to check against to see if they are present inside our BloomFilter.

            Parameters:
                   csv1 (str): String representation of filename used for creating BloomFilter
                   csv2 (str): String representation of filename used to check if present in BloomFilter.
            Returns:
                    arr (list): List of strings containing all the elements of csv2 and their presence inside the DB.
"""


def bloom_filter(csv1, csv2):
    lst = []
    ##Initializes a lst containing all elements inside the csv1 file.
    with open(csv1) as csv_input:
        read = csv.reader(csv_input)
        next(read)
        for line in read:
            lst.append(line[0])
    ##Using the formulas for the BloomFilter we determine the ammount of times it must be hashed, the BloomFilter size, etc.
    p = 0.0000001
    n = len(lst)
    m = math.ceil((n * math.log(p)) / math.log(1 / (pow(2, math.log(2)))))
    m = int(m)
    k = round((m / n) * math.log(2))
    k = int(k)
    ## Constructs the bit array using the parameters as its size.
    bloomArray = makeBitArray(int(m))
    number_hash = int(k)

    ##Sets the bit to 1 in the BF for all the hashes found and possible positions of each email inside BF.
    for line in lst:
        x = hash(line)
        for i in range(0, number_hash):
            line_hash = hash(line + str(i))
            output = setBit(bloomArray, line_hash % m)

    arr = []
    lst_check = []
    # Initializes a lst containing all elements inside the csv2 file. These lists is of all elements we need to check if present inside the DB.
    with open(csv2) as csv_input:
        read = csv.reader(csv_input)
        next(read)
        for line in read:
            lst_check.append(line[0])
    # Goes through each element in the list and checks if their present inside the DB using the determined hash method and repeating it the ammount of times it has to be hashed.
    # If present the element is added to a list containing all elements and the status which is Probably in the DB. Otherwise, it is added with "Not in the DB"
    for line in lst_check:
        x = hash(line)
        i = 0
        found = False
        while i < number_hash and not found:
            line_hash = hash(line + str(i))
            if testBit(bloomArray, line_hash % m) == 0:
                arr.append(line + "," + "Not in the DB")
                found = True
            i += 1
        if not found:
            arr.append(line + "," + "Probably in the DB")
    return arr


if len(argv) > 1:
    results = bloom_filter(argv[1], argv[2])
    for line in results:
        print(line)
