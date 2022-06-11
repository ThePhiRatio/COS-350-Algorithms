"""
Code by: Nicholas Soucy
Purpose: Code creates an unsorted list of size n, then sorts it 
using quick sort. Output can be printed to text or the runs can 
be timed.
"""

import time
import random
import sys

sys.setrecursionlimit(1500)     #this quicksort uses recursion and needs a higher recursion limit for large n

#Wrapper function to have the array be the only input parameter
def quicksort(A):
    #Actual quicksort, written via the sudo code in the text
    def sort(A,p,r):
        if p < r:
            #partitions array and recursively calls sort on each partition
            q = partition(A,p,r)
            sort(A,p,q-1)
            sort(A,q+1,r)

    #helper function for sort, this divides the array
    def partition(A,p,r):
        x = A[r]       
        i = p - 1     
        for j in range (p, r):
            if (A[j] < x+1):
                i = i + 1
                #exchange A[i] with A[j]
                A[i], A[j] = A[j], A[i]
        #exchange A[i + 1] with A[r]        
        A[i+1], A[r] = A[r], A[i+1]
        return i+1      #returns the index for the partition

    p = 0
    r = len(A) - 1      #pivot for quicksort, pivot is default the last element

    sort(A,p,r)
    return A            

#Generates a list of length n with random numbers from 0 to 2n  
def generate_list(n):
    array = []
    for _ in range (0,n):
        array.append(random.randint(0,(n*2)))
    #print("Array Generation Done!")
    return array

#Prints all the output, and sorts array
def print_sort(array,n):
    print("***QUICKSORT***")
    print("Size of Array: ",n)
    print("Initial Array: ",array)
    quicksort(array)
    print("Sorted Array after sorting with Quicksort: ",array)

#gets the average runtimes of sorting for a specific n sized array
def runtime(n):
    runtime = []
    #generate array, sort it, and time it 50 times
    for _ in range (0,50):
        array = generate_list(n)
        first = time.time()
        quicksort(array)
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