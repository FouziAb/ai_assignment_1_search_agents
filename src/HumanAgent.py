from agents import Agent, NO_OP

class HumanAgent(Agent):
    def get_action(self, env):
        if self.is_on_edge:
            return NO_OP
        else:
            while True:
                try:
                    choose_list = [k for k, _ in env.graph.edges[self.location].items()]
                    print(f"for NO_OP choose -1. to move to next vertex choose {choose_list}")
                    move = int(input("Enter your move (vertex): "))
                    if move not in choose_list:
                        raise Exception("Invalid move! Please try again")
                    break
                except KeyboardInterrupt:
                    exit(1)
                except Exception as e:
                    print(f"Invalid move! Please try again")
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

