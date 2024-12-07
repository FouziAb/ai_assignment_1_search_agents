import heapq

INFINITY = float("inf")

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
        self.time = 0
        self.next_act_time = 0
        self.carrying_package  = None

    def has_task(self):
        return self.carrying_package is not None
    
    def on_edge(self):
        return self.time < self.next_act_time
    
    def act(self, env):
        raise NotImplementedError
    
    def display(self):
        return f"agent_id: {self.id}, type: {self.type}, location: {self.location}, carrying_package: {self.carrying_package}, time: self.time"

# Human Agent
class HumanAgent(Agent):
    def act(self, state):
        graph, packages, blocked_edges, fragile_edges, time = state
        print(f"Current location: {self.location}")
        print(f"State of the world: {state}")
        move = input("Enter your move (vertex): ")
        return int(move)

# Greedy Agent
class GreedyAgent(Agent):
    def act(self, env):
        if self.on_edge():
            print(f"Agent {self.type} moving")
            self.time += 1
        # If carrying a package, deliver it
        elif self.carrying_package:
            target = self.carrying_package['dest_v']
            if self.location == target:
                # Deliver package
                print(f"Agent {self.type} delivered package to {target}.")
                env.packages_delivered += 1
                self.time += 1
                self.carrying_package = None
            else:
                # Move toward delivery location
                self.location = self.move_toward(target, env)
        else:
            # If not carrying a package, pick one up if available
            for package in env.active_packages:
                if package['start_v'] == self.location:
                    print(f"Agent {self.type} picked up package at {self.location}.")
                    self.carrying_package = package
                    env.active_packages.remove(package)
                    self.time += 1
                    return

            # Move toward nearest package
            nearest_package = self.find_nearest_package(env)
            if nearest_package:
                self.location = self.move_toward(nearest_package['start_v'], env)

    def move_toward(self, target, env):
        # Find shortest path to the target and move one step toward it
        path = self.shortest_path(self.location, target, env)
        print(path)
        if path and len(path) > 1:
            next_vertex = path[1]
            if (self.location, next_vertex) in env.fragile_edges:
                env.fragile_edges.remove((self.location, next_vertex))
                env.fragile_edges.remove((next_vertex, self.location))
                env.blocked_edges.add((self.location, next_vertex))
                env.blocked_edges.add((next_vertex, self.location))

            print(f"Agent {self.type} moved from {self.location} to {next_vertex}.")
            self.next_act_time = self.time + env.graph[self.location][next_vertex]
            self.time += 1
            print(f"Agent {self.type} moved from {self.location} to {next_vertex}. {self.time}  {self.next_act_time}")
            return next_vertex
        return self.location

    def shortest_path(self, start, target, env):
        # Dijkstra's algorithm for shortest path
        pq = [(0, start, [])]
        visited = set()
        while pq:
            cost, vertex, path = heapq.heappop(pq)
            if vertex in visited:
                continue
            visited.add(vertex)
            path = path + [vertex]
            if vertex == target:
                return path
            for neighbor, weight in env.graph[vertex].items():
                if (vertex, neighbor) not in env.blocked_edges:
                    heapq.heappush(pq, (cost + weight, neighbor, path))
        return []

    def find_nearest_package(self, env):
        # Find the nearest package based on current location
        nearest_package = None
        min_distance = float('inf')
        for package in env.active_packages:
            path = self.shortest_path(self.location, package['start_v'], env)
            if path and len(path) - 1 < min_distance:
                min_distance = len(path) - 1
                nearest_package = package
        return nearest_package

class SaboteurAgent(Agent):
    def move(self, state):
        graph, packages, blocked_edges, fragile_edges, time = state
        # Target nearest fragile edge
        target = None
        min_distance = INFINITY
        for edge in fragile_edges:
            if edge not in blocked_edges:
                dist = dijkstra(graph, self.location)[edge[0]]
                if dist < min_distance:
                    min_distance = dist
                    target = edge[0]

        if target is not None:
            # Compute shortest path and move to the next step
            path = dijkstra(graph, self.location)
            next_step = min(graph[self.location], key=lambda v: path[v])
            return next_step
        else:
            return None  # No-op