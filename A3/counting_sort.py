"""
Code by: Nicholas Soucy
Purpose: Code creates an unsorted list of size n, then sorts it 
using counting sort. Output can be printed to text or the runs can 
be timed.
"""

import time
import random

#Wrapper function to have the array be the only input parameter
def countSort(A):
    #Actual counting sort, written via the sudo code in the text
    def sort(A,B,k):
        C = []          #array for counting amounts of certain values
        #initalize the counting array to zeros
        for _ in range(0,k+1):
            C.append(0)
        #count up how many there is of each element
        for j in range (0, len(A)):
            C[A[j]] = C[A[j]] + 1
        #populate the final array with the correct values in the correct order
        for j in range (0, k+1): 
            while (C[j] > 0):
                B.append(j)
                C[j] -= 1
    k = max(A)      #size of counting array
    B = []          #initilize final array
    sort(A,B,k)
    return B

#Generates a list of length n with random numbers from 0 to 2n    
def generate_list(n):
    array = []
    for _ in range (0,n):
        array.append(random.randint(0,(n*2)))
    return array

#Prints all the output, and sorts array
def print_sort(array,n):
    print("***COUNTING SORT***")
    print("Size of Array: ",n)
    print("Initial Array: ",array)
    final = countSort(array)
    print("Sorted Array after sorting with counting sort: ",final)

#gets the average runtimes of sorting for a specific n sized array
def runtime(n):
    runtime = []
    #generate array, sort it, and time it 50 times
    for _ in range (0,50):
        array = generate_list(n)
        first = time.time()
        countSort(array)
        second = time.time()

        runtime.append(second-first)

    #average all the runtimes over the 50 times
    average = 0
    for i in range(0,50):
        average = average + runtime[i]
    average = average/50
    print("Runtime: ",average)

#Driver Code
n = 20
array = generate_list(n)
print_sort(array,n)
#runtime(n)