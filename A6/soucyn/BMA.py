# By: Nicholas Soucy
# Purpose: Code impliments the Boyer-Moore Algorithm for text pattern matching.

import time

def lastOccurenceFunction(pat):
    #POST: Creates a dictionary of the last occurence of each letter in the pattern string for the text
    occur = dict()
    #create a dict for the alphabet, set all equal to -1
    for l in pat:
        occur[l] = -1
        #if there is an occurence of the letter, set dict entry to the index of last occurence
        for i in range (len(pat) -1,-1,-1):
            if l == pat[i]:
                occur[l] = i
    #return the alphabet last occurence dictionary
    return occur

def BoyerMooreMatch(text,pat):
    last = lastOccurenceFunction(pat)
    m = len(pat)
    i = m - 1
    j = m - 1
    while i < len(text):
        # There is a match
        if text[i] == pat[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        # No match, character jump
        else:

            #this try block negates the need for an alphabet
            #try to let l be the index of last occurence
            try:
                l = last[text[i]]
            #if letter does not exist in pattern, set l to -1
            except:
                l = -1

            i = i + m - min(j, 1+l)
            j = m - 1
    return -1