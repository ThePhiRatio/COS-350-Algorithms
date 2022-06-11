# By: Nicholas Soucy
# Purpose: Code impliments the Knuth-Morris-Pratt Algorithm for text pattern matching.

import time

def CreateFailureFunction(pat):
    f = [0 for i in range(len(pat))]
    i = 1 
    j = 0
    m = len(pat)            #length of pattern
    f[0] = 0
    while i < m:
        #increment characters matched
        if pat[j] == pat [i]:
            f[i] = j + 1
            i += 1
            j += 1
        #j indexes after prefix that must match
        elif j > 0:
            j = f[j-1]
        #no match
        else:
            f[i] = 0
            i += 1    
    return f


def KMP(text,pat):
    f = CreateFailureFunction(pat)
    i = 0                   
    j = 0
    m = len(pat)            #length of pattern
    while i < len(text):
        #we have a match
        if pat[j] == text[i]:
            if j == (m - 1):
                #match found
                return (i - m + 1)
            i += 1
            j += 1
        #we have a partial match
        elif j > 0:
            j = f[j-1]
        #no match
        else:
            i += 1
    return -1

text = 'aaabaaaaa'
pat = 'aaba'
print(KMP(text,pat))
