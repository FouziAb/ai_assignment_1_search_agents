from collections import defaultdict

class Graph:
    def __init__(self):
        self.N = 0
        self.vertex = []
        self.edges = defaultdict(dict)
        self.edges_ = []
        self.blocked_edges = []
        self.blocked_edges_ = []
        self.fragile_edges = []
        self.fragile_edges_ = []

    def set_number_of_vertex(self, number):
        self.N = number
        self.vertex = [i for i in range(1, number + 1)]

    def add_egde(self, edge, weight):
        self.edges_.append((edge[0], edge[1], weight))
        self.edges[edge[0]][edge[1]] = weight
        self.edges[edge[1]][edge[0]] = weight

    def add_blocked_edges(self, edge):
        self.blocked_edges_.append(edge)
        self.blocked_edges.append(edge)
        self.blocked_edges.append((edge[1], edge[0]))
    
    def add_fragile_edges(self, edge):
        self.fragile_edges_.append(edge)
        self.fragile_edges.append(edge)
        self.fragile_edges.append((edge[1], edge[0]))

    def remove_fragile_edges(self, edge):
        if edge in self.fragile_edges_:
            self.fragile_edges_.remove(edge)
        elif ((edge[1], edge[0])) in self.fragile_edges_:
            self.fragile_edges_.remove((edge[1], edge[0]))
        self.fragile_edges.remove(edge)
        self.fragile_edges.remove((edge[1], edge[0]))

    def display(self):
        print(f"Graph vertex: {self.vertex}")

        print(f"Egdes:\n\tnode1\tnode2\tweight")
        for n1, n2, w in self.edges_:
            print(f"\tV{n1}\tV{n2}\t{w}")

        print("Blocked egdes:\n\tnode1\tnode2")
        for n1, n2 in self.blocked_edges_:
            print(f"\tV{n1}\tV{n2}")

        print("Fragile egdes:\n\tnode1\tnode2")
        for n1, n2 in self.fragile_edges_:
            print(f"\tV{n1}\tV{n2}")