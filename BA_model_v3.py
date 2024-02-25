#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:44:48 2023

NEW BA MODEL

@author: liz
"""

class BA_model: #starts with a starter network of m+1 nodes

    def __init__(self, m, mtype = 'PA', sn = 'normal'):
        self.m = m 
        self.end_edges = make_starter_network_edges(m) 
        self.node_count = m+1
        self.node_list = list(np.arange(m+1))
        self.mtype = mtype
        
        if sn == 'superhub':
            self.end_edges = []
            for i in range (500):
                for j in range(m):
                    self.end_edges.append(i)
            for j in range (500-m-1):
                self.end_edges.append(0)
            self.node_count = 500
            self.node_list = list(np.arange(500+1))
            
        if sn == 'sparse':
            self.end_edges = []
            for i in range(100*m):
                for j in range (m):
                    self.end_edges.append(i)
            self.node_count = 5*m
            self.node_list = list(np.arange(5*m+1))
        
        if mtype == 'EV': 
            
            self.end_edges = list(np.concatenate((make_starter_network_edges(m), make_starter_network_edges(m)), axis = None))
            new_edges_list = []
            for i in range (m):
                for j in range (m+1):
                    self.end_edges.append(self.node_count+i)
                new_edges_list.append(self.node_count+i)
                
            self.node_count += m
            self.node_list = list(np.arange(2*m+1))
            
            self.connected_edges = set()
            for n1 in self.node_list [:-m]:
                for n2 in self.node_list [:-m]:
                    if n1>n2:
                        self.connected_edges.add((n1, n2))
                    if n2>n1:
                        self.connected_edges.add((n2, n1))

                for n2 in self.node_list [m+1:]:
                    if n1>n2:
                        self.connected_edges.add((n1,n2))
                    if n2>n1:
                        self.connected_edges.add((n2,n1)) #make sure the bigger n first

        
    def connected_edges(self):
        return self.connected_edges
    
    def end_edges(self):
        return self.end_edges
    
    def add_node(self):
        
        if self.mtype == 'PA':
            self.node_count += 1
            self.node_list.append(self.node_count)
            new_edges = []
            while len(new_edges) < self.m:
                n = random.choice(self.end_edges)
                if n not in new_edges:
                    new_edges.append(n)
                    self.end_edges.append(n)  
            for i in range (self.m):
                self.end_edges.append(self.node_count)
                
        if self.mtype == 'RA': #random attachment
            self.node_count += 1
            self.node_list.append(self.node_count)
            new_edges = []
            while len(new_edges) < self.m:
                n = random.choice(self.node_list)
                if n not in new_edges:
                    new_edges.append(n)
                    self.end_edges.append(n)  
            for i in range (self.m):
                self.end_edges.append(self.node_count)
                
        if self.mtype == 'EV': #existing vertices 
            self.node_count += 1
            self.node_list.append(self.node_count-1)
            r = int(self.m/3)
            
            #add edge between existing vertex with PA
            new_edges_e = []
            while len(new_edges_e) < (self.m-r)*2:
                n1 = random.choice(self.end_edges)
                n2 = random.choice(self.end_edges)
                if n1>n2:
                    checker = (n1,n2)
                if n2>n1:
                    checker = (n2,n1)
                if n1 != n2 and checker not in self.connected_edges:
                    self.connected_edges.add(checker)
                    new_edges_e.append(n1)
                    new_edges_e.append(n2)
                    
            
            #add edges for new vertex
            new_edges = []
            
            while len(new_edges) < r:
                n = random.choice(self.node_list[:-1])
                if n not in new_edges:
                    new_edges.append(n)
                    self.end_edges.append(n) #add new connection to end_edges
                    self.connected_edges.add((self.node_count-1, n))
            
            for i in range (r): # adding new node to end_edges
                self.end_edges.append(self.node_count-1)
            
            for i in new_edges_e: #adding existing vertices to end_edges
                self.end_edges.append(i)
            
                
    def run(self, nums):
        for i in range(nums):
            self.add_node()
    
    def get_degrees(self, return_node = False):
        node, degree = logbin (self.end_edges, 1, normalisation = False, zeros = True)
        if return_node == True:
            return degree, node
        if return_node == False:
            return degree
    
#%% 

BA = BA_model(3, 'EV')
print("connected edges:", BA.connected_edges, ' len: ', (len(BA.connected_edges)))
print("end edges:", BA.end_edges)

BA.run(1)
print("connected edges:", BA.connected_edges, ' len: ', (len(BA.connected_edges)))
print("end edges:", BA.end_edges)

print("k-dist", BA.get_degrees())

#%%

BA = BA_model(3, 'EV')
print("unconnected edges:",len( BA.unconnected_edges))
print("end edges:", BA.end_edges)
BA.add_node()
print("unconnected edges:", BA.unconnected_edges)
print("endedges:", BA.end_edges)
BA.add_node()
print("unconnected edges:", BA.unconnected_edges)
print("endedges:", BA.end_edges)

#%%

#in initialisation
            #make list of unconnected edges
            self.unconnected_edges = []
            result = [(i, j) for i in new_edges_list for j in new_edges_list if i != j]
            for res in result:
                if res[0]<res[1]:
                    self.unconnected_edges.append(res)



        if self.mtype == 'EV': #existing vertices model
            self.node_count += 1
            self.node_list.append(self.node_count-1)
            r = int(self.m/3)
            #add edges to existing nodes
            new_edges_e = []
            while len(new_edges_e) < r*2:
                n1 = random.choice(self.end_edges)
                n2 = random.choice(self.end_edges)
                if (n1,n2) in BA.unconnected_edges:
                    new_edges_e.append(n1)
                    new_edges_e.append(n2)
                    BA.unconnected_edges.remove((n1,n2)) #remove edge from unconnected edge list
                if (n2,n1) in BA.unconnected_edges:
                    new_edges_e.append(n1)
                    new_edges_e.append(n2)
                    BA.unconnected_edges.remove((n2,n1))
            #add new node
            new_edges = []
            node_tracker = list(np.arange(self.node_count))
            while len(new_edges) < self.m-r:
                n = random.choice(self.node_list[:-1])
                if n not in new_edges:
                    new_edges.append(n)
                    self.end_edges.append(n) #add new connection to end_edges
                    node_tracker.remove(n)
            result = [(i, j) for i in node_tracker for j in [self.node_count-1] if i != j]
            #print(node_tracker)
            for i in result:
                BA.unconnected_edges.append(i)
                    
            for i in range (self.m-r): # adding new node to end_edges
                self.end_edges.append(self.node_count-1)
            
            for i in new_edges_e: #adding existing vertices to end_edges
                self.end_edges.append(i)



#%%
k_array = []

BA = BA_model(3, mtype = 'EV')
BA.run(10000)
k_array.append(BA.get_degrees())

x, y = logbin (np.asarray(k_array[0], dtype='int'), 1.03)

plt.loglog(x,y, 'o')





#%%

nodes = BA.end_edges
x, y = logbin (nodes, 1, normalisation = False, zeros = True)
plt.loglog(x,y)
y=np.asarray(y, dtype='int')

x1, y1 = logbin(y, 1.3)
    
plt.loglog(x1,y1)
#%%
# initializing the lists
list_1 = [10]
list_2 = [4,5,6]

# making pairs
result = [(i, j) for i in list_1 for j in list_2 if i != j]

# printing the result
print(result)
result2=[]
for res in result:
    if res[0]>res[1]:
        result2.append(res)
print(result2)

result2.append((1,2))
print(result2)
    
    
    
    
    