"""
Code by: Nicholas Soucy
Purpose: Code creates a b_treeNode and b_tree in order to store data and show 
disk reads and disk writes.

Code was heavily inspired by Natekupp on Github, which was in turn, inspired by the 
sudocode in the textbook as well. 
http://gist.github.com/natekupp/1763661#file-gistfile1-py
"""
import random

class b_treeNode(object):
#POST: Initializes the b_treeNode object
    def __init__(self, leaf=False):
        self.leaf = leaf            #boolean to determine if the node is a leaf
        self.keys = []              #a list of keys for the node
        self.children = []                 #list of children of current node
    
    #Prints the B-Tree inorder 
    def inorder_traversal(self):
        #if the node is a leaf node, just print values
        if self.leaf:
            for j in range(0,len(self.keys)):
                print(self.keys[j],end=", ")
        #if the node isn't a leaf node, recursvely call left until you get to a leaf node
        else:
            self.children[0].inorder_traversal()
            for j in range (1, len(self.children)):
                print(self.keys[j-1],end=", ")
                self.children[j].inorder_traversal()

class b_tree(object):
#POST: Initializes the b_tree
    def __init__(self, t):
        self.root = b_treeNode(leaf=True)    #Create root of tree
        self.t = t                          #set t to be minimum key value
        self.diskreadCount = 0
        self.diskwriteCount = 1             #initialization needs a disk write
    
    def search(self, k, x=None):
    #POST: Returns the index of the key, k, when found, 
    #if the key is not in the b_tree, return none.
        if isinstance(x, b_treeNode):
            i = 0
            while i < len(x.keys) and k > x.keys[i]:    #look for index of k
                i += 1
            if i < len(x.keys) and k == x.keys[i]:      #found exact match
                return (x, i)
            elif x.leaf:                                #no match in keys, and is leaf ==> no match exists
                return None
            else:                                       #search children
                self.diskreadCount += 1                 #disk read would be needed
                return self.search(k, x.children[i])
        else:                                           #no node provided, search root of tree
            return self.search(k, self.root)

    def insert_list(self, l):
    #POST: Inserts each element of a list passed to it
        #Insert each element of the list
        for i in range(len(l)):    
            self.insert(l[i]) 

    def insert(self, k):
    #POST: inserts the given element into the tree in the correct location
        r = self.root
        if len(r.keys) == (2*self.t) - 1:     #keys are full so split
            s = b_treeNode()
            self.root = s
            s.children.insert(0, r)           #former root is now 0th child of new root s
            self._split_child(s, 0)            
            self._insert_nonfull(s, k)
        else:
            self._insert_nonfull(r, k)
    
    def _insert_nonfull(self, x, k):
    #POST: Helper subclass of insert, inserts a key into a non-full node.
        i = len(x.keys) - 1
        if x.leaf:
            # insert a key
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1] = k
            self.diskwriteCount += 1
        else:
            # insert a child
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            self.diskreadCount += 1
            if len(x.children[i].keys) == (2*self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.children[i], k)
        
    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = b_treeNode(leaf=y.leaf)
        
        # slide all children of x to the right and insert z at i+1.
        x.children.insert(i+1, z)
        x.keys.insert(i, y.keys[t-1])
        
        # keys of z are t to 2t - 1,
        # y is then 0 to t-2
        z.keys = y.keys[t:(2*t - 1)]
        y.keys = y.keys[0:(t-1)]
        
        # children of z are t to 2t els of y.children
        if not y.leaf:
            z.children = y.children[t:(2*t)]
            y.children = y.children[0:(t)]    
        
        self.diskwriteCount += 3          #need three writes for x, y, and z

    #Calls the inorder_traversal in the node class
    def inorder(self):
        print("Inorder list: ")
        self.root.inorder_traversal()    

    #Accessor for disreadCount
    def getDiskRead(self):
        return self.diskreadCount

    #Accessor for diswriteCount
    def getDiskWrite(self):
        return self.diskwriteCount


"""        
    def delete(self, k):
        index = self.search(k)
        #if the key is present
        if(index is not None):
            #if the node is a leaf
            if(self.isLeaf(index) is True):
                self.delete_from_leaf(index)
            #if the node is not a leaf
            else:
                self.delete_from_nonleaf(index)
    
    def delete_from_leaf(self, index):
        for i in range ((index+1),len(self.keys)):
            self.keys[i-1] = self.keys[i]
        del self.keys[len(self.keys)]
        pass


    def delete_from_nonleaf(self, index):
        k = self.keys[index]
        pass

    def isLeaf(self,k):
        pass
"""
#b_2_4_tree class that creates a 2_4 tree from the b_tree class
class b_2_4_tree(b_tree):
    def __init__(self):
        self.t = 2                          #this t is the minimum t value, this would correspond to a maximum t of 4
        self.root = b_treeNode(leaf = True)
        self.diskreadCount = 0
        self.diskwriteCount = 1             #initialization needs a disk write

#Generates a list of length n with random numbers from 0 to 10n   
def generate_list(n):
    array = []
    for _ in range (0,n):
        array.append(random.randint(0,(n*10)))
    return array

#nums = [10,1,5,15,89,8,54,16,24,69,87,99,11,22,32,42,52,62,72,82,92,21,31,41,51,61,71,81,91]
nums = generate_list(50)
b = b_2_4_tree()
b.insert_list(nums)
print("***2-4-TREE***")
print("List before enterting 2-4-tree: ",nums)
b.inorder()
print("\n")
print("Amount of DiskReads: ",b.getDiskRead())
print("Amount of DiskWrites: ",b.getDiskWrite())