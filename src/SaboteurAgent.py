from agents import Agent, NO_OP
import heapq

class SaboteurAgent(Agent):
    def get_action(self, env):
        move = NO_OP
        if self.is_on_edge:
            return move
        else:
            nearest_fragile_edge, path, cost = self.find_nearest_fragile_edge(env)
            if nearest_fragile_edge:
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

    def update(self, env):
        if self.is_on_edge:
            self.edge_wight -= 1
            if self.edge_wight == 0:
                if (self.location, self.next_location) in env.graph.fragile_edges:
                    env.graph.remove_fragile_edges((self.location, self.next_location))
                    env.graph.add_blocked_edges((self.location, self.next_location))
                self.is_on_edge = False
                self.location = self.next_location
        self.display()
        self.time += 1

    def find_nearest_fragile_edge(self, env):
        # Find the nearest fragile edge based on current location
        nearest_fragile_edge = None
        min_distance = float('inf')
        path_min_len = float('inf')
        path = ([], min_distance)
        def compare_cost_len_path(path1, path2):
            if path1[1] < path2[1]:
                return True
            elif path1[1] == path2[1] and len(path1[0]) < len(path2[0]):
                return True
            return False

        for fragile_edge in env.graph.fragile_edges_:
            path = self.shortest_path(self.location, fragile_edge, env)
            if path and compare_cost_len_path(path, (path_min_len, min_distance)):
                path_min_len = len(path[0]) - 1
                min_distance = path[1]
                nearest_fragile_edge = fragile_edge
        return nearest_fragile_edge, path[0], path[1]

    def shortest_path(self, start, target_edge, env):
        # Dijkstra's algorithm for shortest path
        target_v1, target_v2 = target_edge
        pq = [(0, start, [])]
        visited = set()
        while pq:
            cost, vertex, path = heapq.heappop(pq)
            if vertex in visited:
                continue
            visited.add(vertex)
            path = path + [vertex]
                
            for neighbor, weight in env.graph.edges[vertex].items():
                if (vertex == target_v1 and neighbor == target_v2) or (vertex == target_v2 and neighbor == target_v1):
                    return path + [neighbor], cost + weight
                if (vertex, neighbor) not in env.graph.blocked_edges:
                    heapq.heappush(pq, (cost + weight, neighbor, path))
        return [], 0
