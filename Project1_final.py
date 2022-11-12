import random 
import copy
class EightPuzzle():
    # Eight puzzle representation with methods for solving
    def __init__(self):
        # Set initial state as the goal state
        #Helper method that acts as the constructor and sets the goal state and the current default state
        random.seed(42)
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    
    def goalCheck(self, state):
        # Helper method
        # Check to see if the given state is the goal state
        return state == self.goal_state
    
    def setGoalState(self):
        # Helper setter method
        # Set the state of the puzzle to the goal state
        self.state = copy.deepcopy(self.goal_state)
        
    def getAvailableActions(self, state):
        #This method returns the list of available moves and location of blank depending on the current state of the puzzle
        #This is a helper method
        #First find the position of the blank tile
        for row_index, row in enumerate(state):
            for column_index, element in enumerate(row):
                if element == 0:
                    blank_row = row_index
                    blank_column = column_index
                    
        available_actions = []
        
        #Find all the available moves of the blank tile from the current state
        if blank_row == 0:
            available_actions.append("down")
        elif blank_row == 1:
            available_actions.extend(("up", "down"))
        elif blank_row == 2:
            available_actions.append("up")
            
        if blank_column == 0:
            available_actions.append("right")
        elif blank_column == 1:
            available_actions.extend(("left", "right"))
        elif blank_column == 2:
            available_actions.append("left")
            
        #random.shuffle(available_actions)
        return available_actions, blank_row, blank_column
    
    def setState(self, state):
        # This method sets the state of the puzzle to a string in the format "b12 345 678"
        if len(state) != 11:
            print("The length of the state is incorrect")            
        #elements added[] is a list to keep track of the elements that have been added to puzzle board
        elements_added = []
            
        #Loop through all possible positions of the state and check if the inputs are legal
        for row_index, row in enumerate (state.split(" ")):
            for column_index, element in enumerate(row):
                
                if element not in ['b', '1','2', '3', '4', '5', '6', '7', '8']:
                    print("Character is not valid", element)
                    break
                else:
                    if element == "b":
                        if element in elements_added:
                            print("blank should only be added once")
                         
                        #Change the blank tile to 0 on the puzzle   
                        else:
                            self.state[row_index][column_index] = 0
                            elements_added.append("b")
                            
                    #Check to see if the input has already been added to the puzzle
                    else:
                        if int (element) in elements_added:
                            print("Tile {} has been added twice".format(element))
                            break
                        
                        else:
                            self.state[row_index][column_index] = int(element)
                            elements_added.append(int(element))
    def printState(self):
        final_state = [] 
        #Display the final state of the board in the format b12 345 678. The puzzle format is added below
        
        # Iterate through the tiles
        for row in self.state:
            for element in row:
                if element == 0:
                    final_state.append("b")
                else:
                    final_state.append(str(element))
        print("".join(final_state[0:3]), "".join(final_state[3:6]), "".join(final_state[6:9]))
        
    def table_print_state(self, state):
        #Print the current state of the board in the format of a puzzle
        print("\nCurrent State")
        for row in (state):
            print("-" * 10)
            print("| {} | {} | {} |".format(*row))
            
    def table_print_solution(self, solution_path):
        # Display the solution path in an puzzle table format
        try:
            for depth, state in enumerate(solution_path[::-1]):
                if depth == 0:
                    print("\nStarting State")
                #If the goal has been reached break out of the loop
                elif depth == (len(solution_path) - 2):
                    print("We have reached the goal")
                    for row_num, row in enumerate(state[0]):
                        print("-" * 13)
                        print("| {} | {} | {} |".format(*row))

                    print("\n")
                    break
                else:
                    print("\n Current node depth: ", depth)
                for row_num, row in enumerate(state[0]):
                    print("-" * 13)
                    print("| {} | {} | {} |".format(*row))
        except:
            print("No solution has been found")
        
                    
    def move(self, state, action):
        # This method moves the tile up, down, left, or right as per the input
        available_actions, blank_row, blank_column = self.getAvailableActions(state)
        
        next_state = copy.deepcopy(state)
        
        if action not in available_actions:
            print("This move is not allowed")

        else:
            if action == "up":
                tile_moved = state[blank_row - 1][blank_column]
                next_state[blank_row][blank_column] = tile_moved
                next_state[blank_row - 1][blank_column] = 0
            elif action == "down":
                tile_moved = state[blank_row + 1][blank_column]
                next_state[blank_row][blank_column] = tile_moved
                next_state[blank_row + 1][blank_column] = 0
            elif action == "right":
                tile_moved = state[blank_row][blank_column + 1]
                next_state[blank_row][blank_column] = tile_moved
                next_state[blank_row][blank_column + 1] = 0
            elif action == "left":
                tile_moved = state[blank_row][blank_column - 1]
                next_state[blank_row][blank_column] = tile_moved
                next_state[blank_row][blank_column - 1] = 0
        return next_state
    
    
    def randomizeState(self, n):
        # Helper method
        # This method takes a random series of moves backwards from the goal state to the solution
        # The method also sets the current state of the puzzle to a legal state that exists
        present_state = (self.goal_state)
        random.seed(42)
        
        for i in range(n):
            available_actions, _, _, = self.getAvailableActions(present_state)
            random_move = random.choice(available_actions)
            present_state = self.move(present_state, random_move)
          
        # Set the state of the puzzle to the random state  
        self.state = present_state
        
    def calculate_h1_heuristic(self, state):
        # This method calculates and returns the h1 heuristic for a current state of the puzzle
        # H1 heuristic = No. of tiles out of place from their final position
        current_state_list = sum(state, [])
        goal_state_list = sum(self.goal_state, [])
        h1 = 0
        
        for i, j in zip(current_state_list, goal_state_list):
            if i!= j:
                h1+=1
        
        return h1
    
    
    def calculate_h2_heuristic(self, state):
        # Helper method that calculates and returns the h2 heuristic for a given state
        # The h2 heuristic for the eight puzzle is defined as the sum of the Manhattan distances of all the tiles
        # Manhattan distance is calculated by absolute value of the x and y difference of the current tile position from its goal state position

        current_tile = {}
        goal_tile = {}
        h2 = 0
        
        # Create dictionaries of the current state and goal state
        for row_index, row in enumerate(state):
            for column_index, element in enumerate(row):
                current_tile[element] = (row_index, column_index)
        
        for row_index, row in enumerate(self.goal_state):
            for column_index, element in enumerate(row):
                goal_tile[element] = (row_index, column_index)
                
        for tile, position in current_tile.items():
            # Do not count the distance of the blank 
            if tile == 0:
                continue
            else:
                # Calculate heuristic as the Manhattan distance (h2)
                goal_position = goal_tile[tile]
                h2 += (abs(position[0] - goal_position[0]) + abs(position[1] - goal_position[1]))

        return h2
    
    def calculate_total_cost(self, node_depth, state, heuristic):
        # Helper method that returns the total cost of a state using the depth and the heuristic
        if heuristic == "h2":
            return node_depth + self.calculate_h2_heuristic(state)
        elif heuristic == "h1":
            return node_depth + self.calculate_h1_heuristic(state)
    
    def Astar_search(self, heuristic="h2", max_nodes=9999, print_solution=True):
        # Performs a-star search
        # Prints the list of solution moves and the solution length when the correct methods from above are added into the command prompt
        # Need a dictionary for the frontier and for the expanded nodes
        frontier = {}
        expanded_nodes = {}
        
        self.starting_state = copy.deepcopy(self.state)
        current_state = copy.deepcopy(self.state)
        # node_index is used for indexing the dictionaries and to keep track of the number of nodes expanded from the current state which can be random or the input
        node_index = 0

        # Set the first element in both dictionaries to the starting state
        # This is the only node that will be in both dictionaries
        expanded_nodes[node_index] = {"state": current_state, "parent": "root", "action": "start",
                                   "total_cost": self.calculate_total_cost(0, current_state, heuristic), "depth": 0}
        
        frontier[node_index] = {"state": current_state, "parent": "root", "action": "start",
                                   "total_cost": self.calculate_total_cost(0, current_state, heuristic), "depth": 0}
        

        invalid = False

        # all_nodes keeps track of all nodes on the frontier and is the priority queue.
        all_frontier = [(0, frontier[0]["total_cost"])]

        # Stop when maximum nodes inputted have been reached
        while not invalid:

            # Get current depth of state for use in total cost calculation
            current_depth = 0
            for node_num, node in expanded_nodes.items():
                if node["state"] == current_state:
                    current_depth = node["depth"]

            # Find available actions leading from the current state of the puzzle
            available_actions, _, _ = self.getAvailableActions(current_state)
            for action in available_actions:
                repeat = False

                # If maximum nodes have been expanded or reached then break out of the loop
                if node_index >= max_nodes:
                    invalid = True
                    print("No Solution Found in first {} nodes generated".format(max_nodes))
                    self.num_nodes_generated = max_nodes
                    break

                # Find the new state corresponding to the action and calculate its total cost
                new_state = self.move(current_state, action)
                new_state_parent = copy.deepcopy(current_state)

                # Check to see if new state has already been expanded then do not added to the frontier
                for expanded_node in expanded_nodes.values():
                    if expanded_node["state"] == new_state:
                        if expanded_node["parent"] == new_state_parent:
                            repeat = True

                # Check to see if new state and parent is on the frontier
                # The same state can be added twice to the frontier if the parent state is different
                for frontier_node in frontier.values():
                    if frontier_node["state"] == new_state:
                        if frontier_node["parent"] == new_state_parent:
                            repeat = True

                # If new state has already been expanded or is in the queue then do not add it to the frontier queue     
                if repeat:
                    continue

                else:
                    # Each action represents another node generated
                    node_index += 1
                    depth = current_depth + 1

                    # Total cost is path length (number of steps from starting state) + heuristic
                    new_state_cost = self.calculate_total_cost(depth, new_state, heuristic)
                    all_frontier.append((node_index, new_state_cost))
                    frontier[node_index] = {"state": new_state, "parent": new_state_parent, "action": action, "total_cost": new_state_cost, "depth": current_depth + 1}

            # Sort all the nodes on the frontier by total cost to ensure the one with the least cost stays at the front
            all_frontier = sorted(all_frontier, key=lambda x: x[1])

            # If the number of nodes generated does not exceed max nodes, find the best node and set the current state to that state
            if not invalid:
                # The best node will be at the front of the queue
                best_node = all_frontier.pop(0)
                best_node_index = best_node[0]
                best_node_state = frontier[best_node_index]["state"]
                current_state = best_node_state

                # Move the node from the frontier to the expanded nodes
                expanded_nodes[best_node_index] = (frontier.pop(best_node_index))
                
                if self.goalCheck(best_node_state):
                    # Create attributes for the expanded nodes and the frontier nodes
                    self.expanded_nodes = expanded_nodes
                    self.frontier = frontier
                    self.num_nodes_generated = node_index + 1

                    # Display the solution path using the additional helper method
                    self.success(expanded_nodes, node_index, print_solution)
                    break

    def solve_beam(self, k=1, max_nodes = 9999, print_solution = True):
        #This method performs the local beam search where k is the number of successors states to consider on each iteration. The evaluation function is h1 + h2 and at each iteration the next set of nodes will be the k closest nodes with lowest scores.add()
        
        self.starting_state = copy.deepcopy(self.state)
        starting_state = copy.deepcopy(self.state)
        
        if starting_state == self.goal_state:
            self.success(node_dict = {}, num_nodes_generated = 0)
        
        all_nodes = {}
        
        node_index = 0
        
        all_nodes [node_index] = {"state": starting_state, "parent": "root", "action": "start"}
        
        starting_score = self.calculate_h1_heuristic(starting_state) + self.calculate_h2_heuristic(starting_state)

        # Available nodes is all the possible states that can be accessed from the current state stored as an (index, score) tuple
        available_nodes = [(node_index, starting_score)]
                
        invalid = False
        valid = False

        while not invalid:
            if node_index >= max_nodes:
                invalid = True
                print("The solution was not found in the first {} generated nodes".format(max_nodes))
                break
            
            successor_nodes = []  # These can be reached from all the available states 
        
            for node in available_nodes:
            
                repeat = False
                present_state = all_nodes[node[0]]["state"]
            
                available_actions, _, _ = self.getAvailableActions(present_state)
            
                for action in available_actions:
                    next_state = self.move(present_state, action)

                    for node_num, node in all_nodes.items():
                        if node["state"] == next_state:
                            if node["parent"] == present_state:
                                repeat = True
                
                    if next_state == self.goal_state:
                        all_nodes[node_index] = {"state": next_state, "parent": present_state, "action": action}
                        self.expanded_nodes = all_nodes
                        self.num_nodes_generated = node_index + 1
                        self.success(all_nodes, node_index, print_solution)
                        valid = True
                        break
                
                    if not repeat:
                        node_index += 1
                        score = (self.calculate_h1_heuristic(next_state) + self.calculate_h2_heuristic(next_state))
                        all_nodes[node_index] = {"state": next_state, "parent": present_state, "action": action}
                        successor_nodes.append((node_index, score))
                    
                    else:
                        continue
        
            # The available nodes are now all the successor nodes sorted by score
            available_nodes = sorted(successor_nodes, key=lambda x: x[1])

            # Choose only the k best successor states
            if k < len(available_nodes):
                available_nodes = available_nodes[:k]
            if valid == True:
                break
                
    def success(self, node_dict, num_nodes_generated, print_solution=True):
        # Helper method
        # Once the solution has been found, prints the solution path and the length of the solution path
        if len(node_dict) >= 1:

            # Find the final node
            for node_num, node in node_dict.items():
                if node["state"] == self.goal_state:
                    final_node = node_dict[node_num]
                    break

            # Generate the solution path from the goal state to the start state
            solution_path = self.generate_solution_path(final_node, node_dict, path=[([[0, 1, 2], [3, 4, 5], [6, 7, 8]], "goal")])
            solution_length = len(solution_path) - 2

        else:
            solution_path = []
            solution_length = 0
        
        self.solution_path = solution_path 

        if print_solution:
            # Display the length of solution and solution path
            print("Solution is below")
            print("Solution Length: ", solution_length)

            # The solution path goes from final to start node. To display sequence of actions, reverse the solution path
            print("Solution Path", list(map(lambda x: x[1], solution_path[::-1])))
            print("Total nodes generated:", num_nodes_generated)
        
    def generate_solution_path(self, node, node_dict, path):
        # Helper method
        # Return the solution path for display from final (goal) state to starting state
        if node["parent"] == "root":
            # If root is found, add the node and then return
            path.append((node["state"], node["action"]))
            return path

        else:
            # If the node is not the root, add the state and action to the solution path
            state = node["state"]
            parent_state = node["parent"]
            action = node["action"]
            path.append((state, action))

            # Find the parent of the node and recurse
            for node_num, expanded_node in node_dict.items():
                if expanded_node["state"] == parent_state:
                    return self.generate_solution_path(expanded_node, node_dict, path)
        