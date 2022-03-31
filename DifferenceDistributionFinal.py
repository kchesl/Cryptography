
from ctypes.test.test_bitfields import BITS

# Define the given sbox stuff
SboxInput = [[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
SboxOutput = [[1,1,0], [1,0,1], [0,0,1], [0,0,0], [0,1,1], [0,1,0], [1,1,1], [1,0,0]]
ReversedSboxOutput = [[0, 1, 1], [0, 1, 0], [1, 0, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [0, 0, 0], [1, 1, 0]]

def DifferenceDistribution(xP, yP):
    xP = SboxInput[xP]
    yP = SboxInput[yP]
    
    dd = 0;
    for i in range(8):
        x = SboxInput[i]
        y = SboxOutput[i]
        
        #print("x ", x)
        #print("y ", y)
        #print("yPrime ", yPrime)

        xStar = XOR(x, xP)
        xStarDec = bitsToDec(xStar)
        yStar = SboxOutput[xStarDec]
        
        #print("xStar ", xStar)
        #print("xStarDec ", xStarDec)
        #print("yStar ", yStar)
        
        yPrime = XOR(y, yStar)
        #print("yPrime ", yPrime)
        #print("yP ", yP)
        ###################
        if (yPrime == yP):
            dd += 1
    #print("dd", dd)
    return (dd)

#def XOR(x, a):
#    c = 0
#    for i in range(len(a)):
#        if a[i] == 1:
#            if x[i] == 1:
#                c += 1
#   return (c % 2)
def XOR(a, b):
    answer = []
    for i in range(len(a)):
        if (a[i] + b[i]) % 2 == 1:
            answer.append(1)
        else :
            answer.append(0)
    return answer

def bitsToDec(bits):
    decNum = 0
    for bit in bits:
        decNum = (decNum * 2) + bit
    return decNum    
    

def printTable():
    print("TABLE")
    print(*range(0, 8), " ")
    
    for i in range(8):
        for j in range(8):
            print(DifferenceDistribution(i, j)," ", end="")
            if j == 7:
                print('\n')
                
printTable();

#[y, y*]
plaintext1 = [[0, 1, 0], [1, 1, 0]]
plaintext2 = [[1, 0, 1], [1, 1, 1]]
plaintext3 = [[0, 0, 1], [0, 0, 0]]

trip1 = [0, 0, 1]
trip2 = [0, 1, 1]
trip3 = [1, 1, 1]

text_pairs = [plaintext1, plaintext2, plaintext3]

key_counts = []
for i in range(8):
    key = SboxInput[i]
    trip1_count = 0
    trip2_count = 0
    trip3_count = 0
    for pair in text_pairs:
        xored_y = XOR(key, pair[0])
        xored_y_star = XOR(key, pair[1])
        rev_y = ReversedSboxOutput[bitsToDec(xored_y)]
        rev_y_star = ReversedSboxOutput[bitsToDec(xored_y_star)]
        final = XOR(rev_y, rev_y_star)
        if final == trip1:
            trip1_count = trip1_count + 1
        elif final == trip2:
            trip2_count = trip2_count + 1
        elif final == trip3:
            trip3_count = trip3_count + 1
    key_counts.append((1/4) * trip1_count + (1/8) * trip2_count + (1/8) * trip3_count)
    
print(key_counts)
        
#DifferenceDistribution(3, 3);

        
        

    
    