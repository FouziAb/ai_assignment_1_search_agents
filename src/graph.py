from collections import defaultdict

class Graph:
    def __init__(self):
        self.N = 0
        self.vertex = []
        self.edges = defaultdict(dict)
        self.edges_ = []
        self.blocked_edges = []
        self.fragile_edges = []

    def set_number_of_vertex(self, number):
        self.N = number
        self.vertex = [i for i in range(1, number + 1)]

    def add_egde(self, edge, weight):
        self.edges_.append((edge[0], edge[1], weight))
        self.edges[edge[0]][edge[1]] = weight
        self.edges[edge[1]][edge[0]] = weight

    def add_blocked_edges(self, edge):
        self.blocked_edges.append(edge)
        self.blocked_edges.append((edge[1], edge[0]))
    
    def add_fragile_edges(self, edge):
        self.fragile_edges.append(edge)
        self.fragile_edges.append((edge[1], edge[0]))

    def remove_fragile_edges(self, edge):
        self.fragile_edges.remove(edge)
        self.fragile_edges.remove((edge[1], edge[0]))

    def display(self):
        print(f"Graph vertex: {self.vertex}")

        print(f"Egdes:\n node1 node2 weight")
        for n1, n2, w in self.edges_:
            print(f"V{n1} V{n2} {w}")

        print("Blocked egdes:\n node1 node2")
        for n1, n2 in self.blocked_edges:
            print(f"V{n1} V{n2}")

        print("Fragile egdes:\n node1 node2")
        for n1, n2 in self.fragile_edges:
            print(f"V{n1} V{n2}")