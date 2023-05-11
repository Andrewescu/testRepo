# Import necessary modules
import math
import hashlib
import bitarray
from concurrent.futures import ThreadPoolExecutor

def loadRock():
    loadedArr = []
    with open("rockyou.ISO-8859-1.txt", "r", encoding="ISO-8859-1") as file:
        for line in file:
            word = line.strip()
            loadedArr.append(word)
    print(loadedArr[:10], "\n")
    return loadedArr

def loadDict():
    dictArr = []
    with open("dictionary.txt", "r", encoding="ISO-8859-1") as file:
        for line in file:
            word = line.strip()
            dictArr.append(word)
    print(dictArr[:10])
    return dictArr

# Define the BloomFilter class
class BloomFilter:
    # Constructor
    def __init__(self, n, p):
        """
        n: Expected number of elements to be added.
        p: Desired false positive probability.
        """
        # Calculate the size of bit array (m) and number of hash functions (k)
        self.m = math.ceil(-(n * math.log(p)) / (math.log(2)**2))
        self.k = math.ceil((self.m / n) * math.log(2))
        
        # Initialize bit array of size m with all bits set to 0
        self.filter = bitarray.bitarray(self.m)
        self.filter.setall(0)

    # Hashing function
    def _hash(self, data, i):
        """
        data: The element to be hashed.
        i: The index of the hash function.
        """
        # Create a new SHA-256 hash object
        h = hashlib.sha256()
        
        # Hash the input data concatenated with the hash function index
        h.update((str(i) + data).encode("utf-8"))
        
        # Return the resulting hash value modulo m
        return int(h.hexdigest(), 16) % self.m

    # Method to add an element to the filter
    def add(self, data):
        """
        data: The element to be added.
        """
        # Hash the element with k different hash functions and set the corresponding bits to 1
        for i in range(self.k):
            idx = self._hash(data, i)
            self.filter[idx] = 1

    # Method to check if an element might be in the filter
    def contains(self, data):
        """
        data: The element to be checked.
        """
        # Hash the element with k different hash functions and check if all the corresponding bits are 1
        if all(self.filter[self._hash(data, i)] for i in range(self.k)):
            return "maybe"
        else:
            return "no"

TP = 0
FP = 0
TN = 0
FN = 0

# Usage example
n = 1000  # Expected number of elements
p = 0.01  # Desired false positive probability

bloom_filter = BloomFilter(n, p)
# bloom_filter.add("hello")  # Add "hello" to the filter
# bloom_filter.add("world")  # Add "world" to the filter

# print("hello", bloom_filter.contains("hello"))  # Check if "hello" might be in the filter
# print("world", bloom_filter.contains("world"))  # Check if "world" might be in the filter
# print("unknown", bloom_filter.contains("unknown"))  # Check if "unknown" might be in the filter

rockArr = loadRock()
# rockArr = ['123456', '12345', '123456789', 'password', 'iloveyou', 'princess', '1234567', 'rockyou', '12345678', 'abc123']

dictArr = loadDict()
# dictArr = ['!', '!!', '!!!!!!', '!!!!!!', '!!!!!!!', '!!!!!!!!', '!!!!!!!!!!', '!!!gerard!!!', '!!!sara', '!"£$%^']

print("hasing")

with ThreadPoolExecutor() as executor:
    for rString in rockArr:
        print("hashing", rString)
        executor.submit(bloom_filter.add, rString)


with ThreadPoolExecutor() as executor:
    futures = {executor.submit(bloom_filter.contains, dString): dString for dString in dictArr}

for future in futures:
    dString = futures[future]
    print("checking", dString)
    contained = future.result()

    if contained == "maybe":
        if dString in rockArr:
            TP += 1
        else: 
            FP += 1
    else:
        if dString in rockArr:
            FN += 1
        else:
            TN += 1
    print(contained)

    

print("TP", TP)
print("FP", FP)
print("TN", TN)
print("FN", FN)