import heapq

INFINITY = float("inf")
NO_OP = -1

# Dijkstra's algorithm for shortest paths
def dijkstra(graph, start, blocked_edges):
    distances = {v: INFINITY for v in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            edge = (current_vertex, neighbor)
            if edge not in blocked_edges and (neighbor, current_vertex) not in blocked_edges:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    return distances

# Agent class
class Agent:
    def __init__(self, agent_id, agent_type, start_v):
        self.id = agent_id
        self.type = agent_type
        self.location = start_v
        self.next_location = None
        self.is_on_edge = False
        self.time = 0
        self.score = 0
        self.next_act_time = 0
        self.packages = []

    def has_task(self):
        return len(self.packages) != 0 
    
    def on_edge(self):
        return self.time < self.next_act_time
    
    def act(self, env):
        raise NotImplementedError
    
    def display(self):
        print(f"\tagent_id: {self.id}, type: {self.type}:")
        print(f"\tlocation: {self.location}, next location {self.next_location}")
        if not self.packages:
            print(f"\tcarrying package: None")
        else:
            for i in range(len(self.packages)):
                print(f"\t{i}. {self.packages[i].id}")
