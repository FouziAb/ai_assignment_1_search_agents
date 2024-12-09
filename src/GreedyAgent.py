from agents import Agent, NO_OP
import heapq

class GreedyAgent(Agent):
    def get_action(self, env):
        move = NO_OP
        if self.is_on_edge:
            return move
        else:
            if self.packages:
                nearest_package, path, cost = self.find_nearest_package(env, False)
                if nearest_package:
                    if len(path) > 1:
                        move = path[1]
            else:
                # Move toward nearest package
                nearest_package, path, cost = self.find_nearest_package(env)
                if nearest_package:
                    if len(path) > 1:
                        move = path[1]
            return move
    
    def start_move(self, env, vertex):
        self.next_location = vertex
        if self.next_location == self.location:
            self.edge_wight = 0
            self.is_on_edge = False
        else:
            self.edge_wight = env.graph.edges[self.location][vertex]
            self.is_on_edge = True

    def update(self):
        if self.is_on_edge:
            self.edge_wight -= 1
            if self.edge_wight == 0:
                self.is_on_edge = False
                self.location = self.next_location
        self.display()
        self.time += 1

    def find_nearest_package(self, env, is_pickup = True):
        # Find the nearest package based on current location
        nearest_package = None
        min_distance = float('inf')
        path_min_len = float('inf')
        path = ([], min_distance)
        def compare_cost_len_path(path1, path2):
            if path1[1] < path2[1]:
                return True
            elif path1[1] == path2[1] and len(path1[0]) < len(path2[0]):
                return True
            return False

        if is_pickup:
            for package in env.active_packages:
                if not package.picked_up:
                    path = self.shortest_path(self.location, package.start_v, env)
                    if path and compare_cost_len_path(path, (path_min_len, min_distance)):
                        path_min_len = len(path[0]) - 1
                        min_distance = path[1]
                        nearest_package = package
        else:
            for package in self.packages:
                path = self.shortest_path(self.location, package.dest_v, env)
                if path and compare_cost_len_path(path, (path_min_len, min_distance)):
                    path_min_len = len(path[0]) - 1
                    min_distance = path[1]
                    nearest_package = package
        return nearest_package, path[0], path[1]

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
                return path, cost
            for neighbor, weight in env.graph.edges[vertex].items():
                if (vertex, neighbor) not in env.graph.blocked_edges:
                    heapq.heappush(pq, (cost + weight, neighbor, path))
        return [], 0
