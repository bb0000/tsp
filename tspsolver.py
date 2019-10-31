#!/usr/bin/env python
# coding: utf-8

import math
import sys

#read input file
ls = []
filename = sys.argv[1]
f = open(filename,"r")
if f.mode == "r":
    content = f.readlines()
    flen = len(content)
    for i in range(1, flen):
        tmp=content[i].split(" ")
        ls.append(tmp)
num = int(content[0])


#calculate distance of two cities
def dis(x1,y1,x2,y2): 
    return math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))


#calculate f function
def c(self, visit,init):
    result = 0
    if len(visit) == 1:
        result += init.get_weight(self)
    for i in range(len(visit)-1):
        result += visit[i].get_weight(visit[i+1])
        result += self.get_weight(visit[len(visit)-1])
    return result

def h(unvisit, self, init, ls):
    if len(unvisit) == 1:
        return init.get_weight(self)
    slen = len(unvisit)
    unvisit_copy = []
    for i in unvisit:
        if i != self:
            unvisit_copy.append(i)
    near_cur = 10000000
    near_init = 10000000
    for j in range(len(unvisit_copy)):
        if self.get_weight(unvisit_copy[j]) < near_cur:
            near_cur = self.get_weight(unvisit_copy[j])
        if init.get_weight(unvisit_copy[j]) < near_init:
            near_init = init.get_weight(unvisit_copy[j])
    return near_cur + near_init + mst(unvisit_copy,ls)


#get union of two sets
def get_unvisit(visit, g):
    result = []
    for i in g:
        if i not in visit:
            result.append(i)
    return result



def mst(unvisit,ls):
    s = Graph()#subgraph
    slen = len(unvisit)#subgraph size
    sls = []#subgraph list
    for i in unvisit:
        for j in range(len(ls)):
            if i.get_id() == ls[j][0]:
                sls.append(ls[j])
    
    for m in range(int(slen)):
        s.add_vertex(sls[m][0])
    
    for n in range(int(slen)):
        for p in range(n+1,int(slen)):
            s.add_edge(sls[n][0], sls[p][0], dis(int(sls[n][1]),int(sls[n][2]),int(sls[p][1]),int(sls[p][2])))
    
    sub_edges = []
    for v in s:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            sub_edges.append([vid,wid,v.get_weight(w)])
    sublen = len(sub_edges)
    new_sub = []
    for c in sub_edges:
        if c not in new_sub:
            new_sub.append(c)
    new_sub.sort(key=takeweight)
    newlen = int(len(new_sub)/2)
    new_sub2 = []
    for g in range(newlen):
        new_sub2.append(new_sub[g*2])
    ##until now, we have a sorted list of edges of subgraph
    ##then we want to impement mst
    mstls=[]
    disset = []
    result = 0
    for h in unvisit:
        t = []
        t.append(h.get_id())
        disset.append(t)
    for x in new_sub2:
        if len(mstls)==len(unvisit):
            break
        ls1 = find(x[0],disset)
        ls2 = find(x[1],disset)
        if (len(ls1)!=0 and len(ls2)!=0):
            if ls1 == ls2:
                continue
            else:
                disset.remove(ls1)
                disset.remove(ls2)
                disset.append(u(ls1,ls2))
                mstls.append(x[0])
                mstls.append(x[1])
                result += x[2]
    return result



def takeweight(elem):
    return elem[2]



def u(ls1,ls2):
    for i in ls2:
        ls1.append(i)
    return ls1



def find(x,ls):
    for i in ls:
        for j in i:
            if x == j:
                return i
    return []


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
    
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    
    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight
    
    def get_connections(self):
        return self.adjacent.keys()
    
    def get_id(self):
        return self.id
    
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
    
    def __iter__(self):
        return iter(self.vert_dict.values())
    
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex
    
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
            if to not in self.vert_dict:
                self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

class Node:
    def __init__(self, name, f,ls):
        self.visit = [] # list of vertexs
        self.name = name
        self.f_value = f
        self.valid = True
        self.visit = ls
    
    def set_path(self,ls):
        self.visit = ls
    
    def set_valid(self,b):
        self.valid = b
    
    def get_name(self):
        return self.name
    
    def get_f(self):
        return self.f_value
    
    def get_valid(self):
        return self.valid
    
    def get_path(self):
        return self.visit

if __name__ == '__main__':
    
    g = Graph()
    for i in range(int(num)):
        g.add_vertex(ls[i][0])
    for j in range(int(num)):
        for s in range(j+1,int(num)):
            g.add_edge(ls[j][0], ls[s][0], dis(int(ls[j][1]),int(ls[j][2]),int(ls[s][1]),int(ls[s][2])))
    visit = []
    unvisit = []
    result = 0
    for v in g:
        unvisit.append(v)
    init = unvisit[0]
    visit.append(init)
    unvisit.pop(0)
    passed = []
    root = Node(init.get_id(),0,[])
    passed.append(root)
    root.set_valid(False)
    while(True):
        if len(unvisit) == 0:
            visit.append(init)
            break
        
        for z in unvisit:
            tmp_f = c(z,visit,init)+h(unvisit,z,init,ls)
            tmp = Node(z.get_id(),tmp_f,visit)
            passed.append(tmp)
        
        minimum = 1000000
        for m in range(int(len(passed))):
            if passed[m].get_valid() == True:
                if passed[m].get_f() < minimum:
                    minimum = passed[m].get_f()
                    mindex = m
        passed[mindex].set_valid(False)
        
        visit = []
        for k in range(int(len(passed[mindex].get_path()))):
            visit.append(passed[mindex].get_path()[k])
        for f in g:
            if passed[mindex].get_name() == f.get_id():
                visit.append(f)
        unvisit = get_unvisit(visit, g)
    print("the optimal route is:")
    for l in visit:
        print(l.get_id())
    print("the number of generated nodes is:")
    print (len(passed))
#return len(passed)
