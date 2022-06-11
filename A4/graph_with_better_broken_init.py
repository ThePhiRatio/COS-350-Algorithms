#Code by: Nicholas Soucy
#Purpose: To impliment three graph representations, edge list, adjacency list, and adjacency matrix.

class Vertex ():
    def __init__(self,graph,name,color=None):
        #For graph
        self.graph = graph
        self.name = name

        #For dft
        self.discovery = 0
        self.finish = 0
        self.color = 'black'

class Edge ():
    def __init__(self,graph,v1,v2,weight=None):
        self.graph = graph
        self.v1 = v1
        self.v2 = v2
        self.weight = weight

class Graph ():

    def __init__(self,graph_desc=None,properties=None):

        self.properties = properties

        self.vertices = []      #List of vertex objects to preserve order in graph             

        if graph_desc:
            if properties == None:
                self.properties = [graph_desc[0]]
            else:
                self.properties.append(graph_desc[0])

            for ele in graph_desc[1:]:
                if self.find_vertex(ele[0]) is None:
                    self.add_vertex(ele[0])
                if len(ele) > 1:              #then it's a real edge description
                    if self.find_vertex(ele[1]) is None:
                        self.add_vertex(ele[1])
                    # Not checking for duplicate edges here:
                    self.add_edge(ele[0],ele[1],ele[2])
    
    def find_vertex(self,name):
        for v in range(0,len(self.vertices)):
            if self.vertices[v].name == name:
                return v
        return None

    def all_vertices(self,desc):
        all_vert = []
        if desc == ['name']:
            for v in range(0,len(self.vertices)):
                all_vert.append(self.vertices[v].name)
        elif desc == ['vert']:
            for v in range(0,len(self.vertices)):
                all_vert.append(Vertex(self,self.vertices[v].name))

        return all_vert

    def incident_to(self,vertex,edge):
        if isinstance(edge, Edge):
            if self.find_edge(edge.v1,edge.v2) is not None:
                if vertex == edge.v1 or vertex == edge.v2:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if self.find_edge(edge[0],edge[1]) is not None:
                if vertex == edge[0] or vertex == edge[1]:
                    return True
                else:
                    return False
            else:
                return False

    def to_list(self):
        if 'digraph' in self.properties:
            output = ['digraph']
        else:
            output = ['graph']

        for vname in self.vertices:
            output.append([vname.name])

        ListEdge = self.all_edges(['name'])
        for e in ListEdge:
            output.append(e)

        return output

    def to_gv(self):
        desc = self.to_list()

        print(desc[0], " {")

        if desc[0] == 'digraph':
            sep = " -> "
        else:
            sep = " -- "
            
        for thing in desc[1:]:
            if len(thing) == 1:  # vertex
                print('   ', thing[0])
            elif len(thing) > 2: # edge, weight exists
                print('   ', thing[0], sep, thing[1], ' ', '[weight="', thing[2],
                      '"]')
            else: #no weight
                print('   ', thing[0],sep,thing[1])
        print('}')
    
    def dft(self,vertex):
        global time
        global span
        
        #create the spanning tree based on the type of graph and graph representation
        if isinstance(self,AdjList):
            if 'digraph' in self.properties:
                span = AdjList(['digraph'])
            else:
                span = AdjList(['graph'])
        elif isinstance(self,EdgeList):
            if 'digraph' in self.properties:
                span = EdgeList(['digraph'])
            else:
                span = EdgeList(['graph'])
        elif isinstance(self,AdjMatrix):
            if 'digraph' in self.properties:
                span = AdjMatrix(['digraph'])
            else:
                span = AdjMatrix(['graph'])


        #Reset all dft vertex variables
        for v in self.vertices:
            v.color = 'black'
            v.discovery = 0
            v.finish = 0

        time = 1
        self._dft(vertex)
        return span

    def _dft(self,vertex):
        global time
        global span
        self.vertices[self.find_vertex(vertex)].color = 'red'
        span.add_vertex(vertex)
        self.vertices[self.find_vertex(vertex)].discovery = time
        time += 1
        for v in self.adjacent_vertices(vertex): 
            if self.vertices[self.find_vertex(v)].color == 'black':
                if self.edge_cost(vertex,v) == -1:
                    span.add_edge(vertex,v)
                else:
                    span.add_edge(vertex,v,self.edge_cost(vertex,v))
                self._dft(v)
        self.vertices[self.find_vertex(vertex)].color = 'blue'
        self.vertices[self.find_vertex(vertex)].finish = time
        time += 1

    def print_vert_dft(self):
        for i in range(0, len(self.vertices)):
            print(self.vertices[i].name, " ", self.vertices[i].color," ",self.vertices[i].discovery,"/",self.vertices[i].finish)

class AdjList(Graph):
    def __init__(self,graph_desc=None,properties=None):
        super().__init__(graph_desc,properties)
        self.adj_list = []

    #WORKS
    def add_vertex(self,name):
        for v in self.vertices:
            if v.name == name:
                return None
            
        self.vertices.append(Vertex(self,name))
        self.adj_list.append([])

    #WORKS
    def delete_vertex(self,name):
        if self.find_vertex(name) is not None:
            #remove all edges that connect to that vertex
            for i in range (0,len(self.adj_list)):
                for j in self.adj_list[i].copy():
                    #if the element contain the vertex you want to delete, remove it
                    if self.find_vertex(name) == j[0]:
                        self.adj_list[i].remove(j)
                    #if it doesnt contain the vertex you want to delete, shift it.
                    elif j[0] > self.find_vertex(name):
                        j[0] = j[0] -1

            #remove vertex from adj list
            del self.adj_list[self.find_vertex(name)]

            #remove vertex from vert list
            del self.vertices[self.find_vertex(name)]
        else:
            print("Vertex "+name+" does not exist!")

    #WORKS
    def add_edge(self,v1,v2,weight=None):
        #if vertex v1 doesnt exist, add it
        if self.find_vertex(v1) == None:
            self.add_vertex(v1)
        #if vertex v2 doesnt exist, add it
        if self.find_vertex(v2) == None:
            self.add_vertex(v2)
        #if edge doesn't already exist, add it
        if self.find_edge(v1,v2) == None:
            self.adj_list[self.find_vertex(v1)].append([self.find_vertex(v2),weight])
            if 'digraph' not in self.properties:
                self.adj_list[self.find_vertex(v2)].append([self.find_vertex(v1),weight])

    #WORKS
    def delete_edge(self,v1,v2):
        #Search in the list of the given source vertex
        if (self.find_vertex(v1) is not None) and (self.find_vertex(v2) is not None) and (self.find_edge(v1,v2) is not None):
            for i in self.adj_list[self.find_vertex(v1)].copy():
                #if the dest vertex is in the source list, delete it
                if self.find_vertex(v2) == i[0]:
                    self.adj_list[self.find_vertex(v1)].remove(i)
                    break
                    #if it is an undirected graph
            if 'digraph' not in self.properties:
                #search through the list of the dest vertex
                for j in self.adj_list[self.find_vertex(v2)].copy():
                    #if the source vertex is in the dest vertex list, delete it
                    if self.find_vertex(v1) == j[0]:
                        self.adj_list[self.find_vertex(v2)].remove(j)
                        break
        else:
            print("Edge from "+v1+" to "+v2+" does not exist!")

    #check
    def all_edges(self,spec):
        list_edges = []
        if spec == ['name']: 
            #go through each element in list
            for i in range (0,len(self.adj_list)):
                #go through each element in the list of list
                for j in range (0,len(self.adj_list[i])):
                    #append edge info to edge list
                    list_edges.append([self.vertices[i].name,self.vertices[self.adj_list[i][j][0]].name,self.adj_list[i][j][1]])
        elif spec == ['edge']:
            #go through each element in list
            for i in range (0,len(self.adj_list)):
                #go through each element in the list of list
                for j in range (0,len(self.adj_list[i])):
                    #append edge info to edge list
                    list_edges.append(Edge(self.vertices[i].name,self.vertices[self.adj_list[i][j][0]].name,self.adj_list[i][j][1]))

        return list_edges

    #WORKS
    def find_edge(self,v1,v2,weight=None):
        #Search in the list of the given source vertex
        for i in range (0,len(self.adj_list[self.find_vertex(v1)])):
            #if the dest vertex is in the source list, delete it
            if self.find_vertex(v2) in self.adj_list[self.find_vertex(v1)][i]:
                return True
        return None

    #WORKS
    def incident_edges(self,v):
        if self.find_vertex(v) is not None:
            incident = []
            for e in range (0,len(self.adj_list[self.find_vertex(v)])):
                incident.append([v,self.vertices[self.adj_list[self.find_vertex(v)][e][0]].name])
            return incident
        else:
            print("Vertex "+v+" does not exist!")

    #WORKS
    def adjacent_vertices(self,v):
        if self.find_vertex(v) is not None:
            adj_vert = []
            for e in range (0,len(self.adj_list[self.find_vertex(v)])):
                adj_vert.append(self.vertices[self.adj_list[self.find_vertex(v)][e][0]].name)
            return adj_vert
        else:
            print("Vertex "+v+" does not exist!")

    #WORKS
    def edge_cost(self,v1,v2):
        if self.find_edge(v1,v2) is not None:
            for i in range (0,len(self.adj_list[self.find_vertex(v1)])):
                if self.find_vertex(v2) in self.adj_list[self.find_vertex(v1)][i]:
                    return self.adj_list[self.find_vertex(v1)][i][1]
        else:
            print("Edge from "+v1+" to "+v2+" does not exist!")

    #WORKS
    def path_cost(self,vert_list):
        distance = 0
        for i in range (0,len(vert_list) - 1):
            distance += self.edge_cost(vert_list[i],vert_list[i+1])
        return distance

    #WORKS
    def adjacent_to(self,v1,v2):
        if (self.find_vertex(v1) is not None) and (self.find_vertex(v2) is not None):
            for e in range (0,len(self.adj_list[self.find_vertex(v1)])):
                if self.find_vertex(v2) == self.adj_list[self.find_vertex(v1)][e][0]:
                    return True
            return False
        else:
            return False

class EdgeList(Graph):
    #WORKS
    def __init__(self,graph_desc=None,properties=None):
       super().__init__(graph_desc,properties)
       self.edges = []

    #WORKS
    def add_vertex(self,name):
        for v in self.vertices:
            if v.name == name:
                return None
        self.vertices.append(Vertex(self,name))

    #WORKS
    def delete_vertex(self,v_name):
        if self.find_vertex(v_name) is not None:
            for e in self.edges.copy():
                #delete if edge contains vertex
                if e.v1 == self.find_vertex(v_name) or e.v2 == self.find_vertex(v_name):
                    self.edges.remove(e)
                #shift all index values to perseve order, if you don't delete it
                else:
                    if e.v1 > self.find_vertex(v_name):
                        e.v1 = e.v1 - 1
                    if e.v2 > self.find_vertex(v_name):
                        e.v2 = e.v2 - 1

            #delete vertex from list
            del self.vertices[self.find_vertex(v_name)]
        else:
            print("Vertex "+v_name+" does not exist!")
        
    #WORKS
    def add_edge(self,v1,v2,weight=None):
        source = self.find_vertex(v1)
        dest = self.find_vertex(v2)
        #if vertex v1 doesnt exist, add it
        if source == None:
            self.add_vertex(v1)
            source = self.find_vertex(v1)
        #if vertex v2 doesnt exist, add it
        if dest == None:
            self.add_vertex(v2)
            dest = self.find_vertex(v2)
        #if edge doesn't already exist, add it
        if self.find_edge(v1,v2) == None:
            self.edges.append(Edge(self,source,dest,weight))
            if 'digraph' not in self.properties:
                self.edges.append(Edge(self,dest,source,weight))

    #WORKS
    def delete_edge(self,v1,v2):
        if (self.find_vertex(v1) is not None) and (self.find_vertex(v2) is not None) and (self.find_edge(v1,v2) is not None):
            e = self.find_edge(v1,v2)
            if e is not None:
                del self.edges[e]
            if 'digraph' not in self.properties:
                e = self.find_edge(v2,v1)
                if e is not None:
                    del self.edges[e]
        else:
            print("Edge from "+v1+" to "+v2+" does not exist!")

    #WORKS
    def all_edges(self,spec):
        all_edges = []
        if spec == ['name']:
            for e in self.edges:
                all_edges.append([self.vertices[e.v1].name,self.vertices[e.v2].name,e.weight])
        elif spec == ['edge']:
            for e in self.edges:
                all_edges.append(Edge(self.vertices[e.v1].name,self.vertices[e.v2].name,e.weight))
        return all_edges

    #WORKS
    def find_edge(self,v1,v2):
        #iterate through the entire list
        for e in range(0,len(self.edges)):
            #if the edge matches the v1,v2 pair, return index
            if self.edges[e].v1 == self.find_vertex(v1) and self.edges[e].v2 == self.find_vertex(v2):
              return e
        return None

    #WORKS
    def incident_edges(self,v):
        if self.find_vertex(v) is not None:
            incident = []
            for e in range (0,len(self.edges)):
                if (self.edges[e].v1 == self.find_vertex(v)) or (self.edges[e].v2 == self.find_vertex(v)):
                    incident.append([self.vertices[self.edges[e].v1].name,self.vertices[self.edges[e].v2].name])
            return incident
        else:
            print("Vertex "+v+" does not exist!")

    #WORKS
    def adjacent_vertices(self,v):
        if self.find_vertex(v) is not None:
            adj_vert = []
            for e in range (0, len(self.edges)):
                if (self.edges[e].v1 == self.find_vertex(v)) and (self.find_vertex(v) not in adj_vert):
                    adj_vert.append(self.vertices[self.edges[e].v2].name)
            return adj_vert
        else:
            print("Vertex "+v+" does not exist!")

    #WORKS
    def edge_cost(self,v1,v2):
        if self.find_edge(v1,v2) is not None:
            return self.edges[self.find_edge(v1,v2)].weight
        else:
            print("Edge from "+v1+" to "+v2+" does not exist!")

    #WORKS
    def path_cost(self,vert_list):
        distance = 0
        for i in range (0,len(vert_list) - 1):
            distance += self.edge_cost(vert_list[i],vert_list[i+1])
        return distance

    #WORKS
    def adjacent_to(self,v1,v2):
        if (self.find_vertex(v1) is not None) and (self.find_vertex(v2) is not None):
            if self.find_edge(v1,v2) is not None:
                return True
            else:
                return False
        else:
            return False

class AdjMatrix(Graph):
    def __init__(self,graph_desc=None,properties=None):
        super().__init__(graph_desc,properties)
        self.matrix = []                       #2d array reperesenting adjacency matrix

    #WORKS
    def add_vertex(self,name):
        #if the name isn't already in the graph
        for v in self.vertices:
            if v.name == name:
                return None

        #append new vertex
        self.vertices.append(Vertex(self,name))
        
        #increase size of 2d array by one
        temp = [x[:] for x in [[0] * len(self.vertices)] * len(self.vertices)]
        for r in range (0,len(self.vertices)-1):
            for c in range (0,len(self.vertices)-1):
                temp[r][c] = self.matrix[r][c]
        self.matrix = temp           

    #WORKS
    def delete_vertex(self,name):
        #if the vertex actually exist
        if self.find_vertex(name) is not None:
            #decrease size of 2d array by one
            for r in range (0,len(self.vertices)):
                del self.matrix[r][self.find_vertex(name)]
            
            del self.matrix[self.find_vertex(name)]

            #remove vertex from vertex list, then shift all memebers to the left
            del self.vertices[self.find_vertex(name)]
            #self.vertices.remove(name)

    #WORKS
    def add_edge(self,v1,v2,weight=None):
        if weight is None:
            weight = -1

        #update v1 and v2 to be the indexes for the vertices
        v1_i = self.find_vertex(v1)
        v2_i = self.find_vertex(v2)

        #check to see if vertices actually exist, if not, add them
        if v1_i is None:
            self.add_vertex(v1)
            v1_i = self.find_vertex(v1)
        if v2_i is None:
            self.add_vertex(v2)
            v2_i = self.find_vertex(v2)
        
        #if edge doens't already exist, add to matrix
        if self.find_edge(v1,v2) == None:
            self.matrix[v1_i][v2_i] = weight
            if 'digraph' not in self.properties:
                self.matrix[v2_i][v1_i] = weight

    #WORKS
    def delete_edge(self,v1,v2):
        
        #update v1 and v2 to be the indexes for the vertices
        v1_i = self.find_vertex(v1)
        v2_i = self.find_vertex(v2)

        if v1_i != None and v2_i != None:
            #delete edge from matrix
            self.matrix[v1_i][v2_i] = 0
            if 'digraph' not in self.properties:
                self.matrix[v2_i][v1_i] = 0

    #WORKS
    def all_edges(self,spec):
        all_edges=[]
        if spec == ['name']:
            for r in range(len(self.vertices)):
                for c in range(len(self.vertices)):
                    if self.matrix[r][c] > 0:
                        all_edges.append([self.vertices[r].name,self.vertices[c].name,self.matrix[r][c]]) 
                    elif self.matrix[r][c] == -1:
                        all_edges.append([self.vertices[r].name,self.vertices[c].name,None])
        elif spec == ['edge']:
            for r in range(len(self.vertices)):
                for c in range(len(self.vertices)):
                    if self.matrix[r][c] > 0:
                        all_edges.append(Edge(self.vertices[r].name,self.vertices[c].name,self.matrix[r][c])) 
                    elif self.matrix[r][c] == -1:
                        all_edges.append(Edge(self.vertices[r].name,self.vertices[c].name,None))
        return all_edges

    #WORKS
    def find_edge(self,v1,v2,weight=None):
        if self.find_vertex(v1) != None and self.find_vertex(v2) != None:
            if (self.matrix[self.find_vertex(v1)][self.find_vertex(v2)] > 0) or (self.matrix[self.find_vertex(v1)][self.find_vertex(v2)] == -1):
                return True
            else:
                return None
        else:
            return None

    #WORKS
    def incident_edges(self,vertex):
        if self.find_vertex(vertex) is not None:
            edge_list = []
            for c in range (0, len(self.vertices)):
                if self.matrix[self.find_vertex(vertex)][c] > 0:
                    edge_list.append([vertex,self.vertices[c].name])
            return edge_list
        else:
            print("Vertex "+vertex+" does not exist!")

    #WORKS
    def adjacent_vertices(self,v):
        if self.find_vertex(v) is not None:
            adj_vert = []
            for c in range (0, len(self.vertices)):
                if (self.matrix[self.find_vertex(v)][c] > 0) or (self.matrix[self.find_vertex(v)][c] == -1):
                    adj_vert.append(self.vertices[c].name)
            return adj_vert
        else:
            print("Vertex "+v+" does not exist!")

    #WORKS
    def edge_cost(self,v1,v2):
        #update v1 and v2 to be the indexes for the vertices
        v1_i = self.find_vertex(v1)
        v2_i = self.find_vertex(v2)
        if v1_i != None and v2_i != None:
            return self.matrix[v1_i][v2_i]

    #WORKS
    def path_cost(self,vert_list):
        distance = 0
        for i in range (0,len(vert_list) - 1):
            distance += self.edge_cost(vert_list[i],vert_list[i+1])
            #if graph is not weighted
            if distance == -1:
                return None
        return distance

    #WORKS
    def adjacent_to(self,v1,v2):
        if (self.find_vertex(v1) is not None) and (self.find_vertex(v2) is not None):
            if self.matrix[self.find_vertex(v1)][self.find_vertex(v2)] > 0:
                return True
            else:
                return False
        else:
            return False


#Driver Code

g = AdjMatrix(['graph'])
g.add_vertex('first')
g.add_edge('first','second',3)
g.add_vertex('second')
g.add_vertex('third')
#g.all_vertices()
#g.add_edge('first','second')
g.add_vertex('third')
g.add_edge('third','second',3)
g.add_edge('third','first',1)
g.add_edge('third','second')
g.to_gv()
a = g.to_list()
new_graph = AdjMatrix(a)
new_graph.to_gv()
#g.dft('third').to_gv()
#g.print_vert_dft()
#print(g.find_edge('first','second'))
#print(g.incident_edges('second'))
#print(g.adjacent_vertices('first'))
#print(g.adjacent_to('first','second'))
#print(g.adjacent_to('first','third'))
#print(g.incident_to('first',['first','second']))
#print(g.incident_to('third',['first','third']))
#print(g.path_cost(['first','second','third','first']))
#print(g.to_list())
#a = g
#a.to_gv()
#print(g.edge_cost("first","second"))'
#g.delete_vertex("second")
#g.delete_edge('second','third')
#g.delete_vertex("first")
#print(g.all_vertices(['name']))
#print(g.all_vertices(['vert']))
#g.to_gv()