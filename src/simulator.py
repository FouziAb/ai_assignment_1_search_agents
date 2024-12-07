from collections import defaultdict
from agents import HumanAgent, GreedyAgent, SaboteurAgent
from package import Package
from graph import Graph

def parse_input_file(file_path):
    graph = Graph()
    packages = []
    agents = []
    agent_id = 0

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            parts = line.split()
            if parts[0] == '#N':
                graph.set_number_of_vertex(int(parts[1]))
            elif parts[0].startswith('#E'):
                edge_id, v1, v2, weight, = parts[0], int(parts[1]), int(parts[2]), int(parts[3][1:])
                graph.add_egde((v1, v2), weight)
            elif parts[0].startswith('#P'):
                package_id, start_v, start_time, _, dest_v, deadline = parts[0], int(parts[1][1:]), int(parts[2]), parts[3], int(parts[4][1:]), int(parts[5])
                packages.append(Package(package_id, start_v, start_time, dest_v, deadline))
            elif parts[0] == '#B':
                graph.add_blocked_edges((int(parts[1][1:]), int(parts[2][1:])))
            elif parts[0] == '#F':
                graph.add_fragile_edges((int(parts[1][1:]), int(parts[2][1:])))
            elif parts[0] == "#A":
                agents.append(GreedyAgent(agent_id, 'stupid greedy', int(parts[1][1:])))
                agent_id += 1
            elif parts[0] == "#H":
                agents.append(HumanAgent(agent_id, 'human', int(parts[1][1:])))
                agent_id += 1
            elif parts[0] == "#I":
                agents.append(SaboteurAgent(agent_id, 'interfering', int(parts[1][1:])))
                agent_id += 1

    return graph, packages, agents
    
class Simulator:
    def __init__(self, graph, packages, agents):
        self.graph = graph
        self.packages = packages
        self.agents = agents
        self.num_vertices = num_vertices
        self.active_packages = []
        self.time = 0
        self.packages_delivered = []

    def update_packages(self):
        """Activate packages that are scheduled to appear at the current time."""
        for package in self.packages:
            if package.start_time == self.time:
                self.active_packages.append(package)

    def future_packages(self):
        """Check if packages will appear in the future."""
        for package in self.packages:
            if package.start_time >= self.time:
                return True
        return False

    def remove_expired_packages(self):
        """Remove packages that can no longer be delivered on time."""
        self.active_packages = [
            package for package in self.active_packages
            if self.time <= package.deadline
        ]

    def run(self):
        print(self.packages)
        max_run_time = max(self.packages, key=lambda x: x.deadline).deadline
        while self.future_packages() or self.active_packages or (any(agent.has_task() for agent in self.agents)):
            print(f"Time : {self.time}")
            self.update_packages()
            self.remove_expired_packages()
            for agent in self.agents:
                action = agent.get_action(self)
                self.update_world(agent, action)
            self.time += 1

        '''while self.time <= max_run_time:
            for agent in self.agents:
                state = (self.graph, self.packages, self.blocked_edges, self.fragile_edges, self.time)
                action = agent.move(state)
                if action is not None:
                    agent.location = action
                self.update_world(agent, action)
            self.time += 1
            self.display_state()'''

    def update_world(self, agent, action):
        if action.type == 'no-op':
            agent.time += 1
            return
        elif action.type == 'pick_up':
            pass
        # Handle package pick up and delivery
        for package in self.packages:
            if package['start_v'] == agent.location and not package.get('picked_up'):
                agent.package = package
                package['picked_up'] = True
            if agent.package and agent.package['dest_v'] == agent.location:
                agent.score += 1
                self.packages.remove(agent.package)
        
        # Handle fragile edge blocking
        if agent.type == "saboteur" and action is not None:
            edge = (agent.location, action)
            if edge in self.fragile_edges:
                self.blocked_edges.add(edge)
                self.fragile_edges.remove(edge)

    def display_state(self):
        print(f"Time: {self.time}")
        for agent in self.agents:
            print(f"Agent {agent.type} at {agent.location}, Score: {agent.score}")

# Main execution
if __name__ == "__main__":
    graph, packages, blocked_edges, fragile_edges, agents, num_vertices = parse_input_file("mapd_input.txt")
    simulator = Simulator(graph, packages, blocked_edges, fragile_edges, agents, num_vertices)
    simulator.run()