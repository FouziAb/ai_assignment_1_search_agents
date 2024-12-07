from collections import defaultdict

class Graph:
    def __init__(self):
        self.N = 0
        self.vertex = []
        self.edges = defaultdict(dict)
        self.blocked_edges = []
        self.fragile_edges = []

    def set_number_of_vertex(self, number):
        self.N = number
        self.vertex = [i for i in range(1, number + 1)]

    def add_egde(self, edge, weight):
        self.edges[edge[0]][edge[1]] = weight
        self.edges[edge[1]][edge[0]] = weight

    def add_blocked_egde(self, edge):
        self.blocked_edges.add(edge)
        self.blocked_edges.add((edge[1], edge[0]))
    
    def add_fragile_edges(self, edge):
        self.fragile_edges.add(edge)
        self.fragile_edges.add((edge[1], edge[0]))

    def remove_fragile_edges(self, edge):
        self.fragile_edges.remove(edge)
        self.fragile_edges.remove((edge[1], edge[0])) 