from maze_functions import *

action_list = ['W', 'E', 'S', 'N'] # list of actions

def single_dfs(maze_size, wall_positions, prize_list, start_position):
    """
    Performs depth-first-search on the maze 
    and returns the sequence of moves and the list of expanded nodes

    expanded_node_list: set - stores all expanded nodes since set has O(1) lookup time on average
    expanded_node_num: int - number of expanded nodes
    frontier: stack - stores nodes to expand since we need to expand the newest node every time we loop
    """

    expanded_node_list = set()
    expanded_node_num = 0

    #add the start position to the frontier
    frontier = [StateRep(start_position, [], prize_list)] # stack

    while(len(frontier) != 0):
        #expand the youngest node added to the frontier & increase the number of expanded nodes by 1
        current_state = frontier.pop()
        expanded_node_num += 1

        #check if the current state meets the goal
        if goal_test(current_state):
            return current_state.move_sequence, expanded_node_num

        #expand the current node in 4 directions using transition function
        #append the new states to the frontier if valid
        for action in action_list:
            new_state = transition(current_state, action, maze_size, wall_positions, prize_list, start_position, expanded_node_list)
            if new_state:
                frontier.append(new_state)
                expanded_node_list.add(new_state.position)
    return None


def print_solution(maze_filename, maze_output):
    """
    Prints the solution to the output
    """

    #import the maze to get information and get the solution by search algorithm
    maze_size, wall_positions, prize_list, start_position = import_maze(maze_filename)
    solution = single_dfs(maze_size, wall_positions, prize_list, start_position)

    with open(maze_output, 'w') as output:
        for j in range(maze_size[1]):
            for i in range(maze_size[0]):
                position = (i, j)
                if position == start_position:
                    output.write("P")
                elif position in wall_positions:
                    output.write("%")
                elif position in prize_list:
                    output.write(".")
                elif position in solution[0]:
                    output.write("#")
                else:
                    output.write(" ")
            output.write("\n")
    print(len(solution[0]),solution[1])


if __name__ == '__main__':
    print_solution('1prize-medium.txt','dfs_maze_output-medium.txt')
    print_solution('1prize-large.txt','dfs_maze_output-large.txt')
    print_solution('1prize-open.txt','dfs_maze_output-open.txt')
    
             





















