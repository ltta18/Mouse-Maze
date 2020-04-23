from maze_functions import *

action_list = ['W','E','S','N']

def heuristic_astar(current_position, prize_position, path_cost):
    """
    Finds the heuristic for the a-star-search algorithm.
    """

    return abs(current_position[0]-prize_position[0]) + abs(current_position[1]-prize_position[1]) + path_cost

def multi_astar(maze_size, wall_positions, prize_list, start_position):
    """
    Performs the a-star search on the maze
    and returns the sequence of moves and the list of expanded nodes

    expanded_node_list: set - stores all expanded nodes since set has O(1) lookup time on average
    expanded_node_num: int - number of expanded nodes
    frontier: list - stores nodes to expand since we need to sort the list based on the heuristic values every time we loop
    prize_in_order: list - stores reached prize in order 
    last_prize_num: int - to check if the number of prizes have changed
    prize_position: tuple - the position of the prize we currently want to reach 
    heuristic_prize_list: list - stores all prizes sorted by the heuristic values
    """

    expanded_node_list = set()
    expanded_node_num = 0

    #create heuristic prize list and sort in reversed order
    heuristic_prize_list = []
    for prize in prize_list:
        heuristic_prize_list.append([prize,heuristic_astar(start_position, prize,0)])
    heuristic_prize_list.sort(reverse=True, key=lambda lst: lst[1])
    prize_position = heuristic_prize_list[-1][0]

    #add the start position to the frontier
    frontier = [] 
    frontier.append([StateRep(start_position, [], prize_list), heuristic_astar(start_position, prize_position, 0)])
    
    last_prize_num = len(prize_list)
    prize_in_order = []

    while(len(frontier)!=0):
        #expand the node with the lowest heuristic value in the frontier & increase the number of expanded nodes by 1
        frontier.sort(reverse=True, key=lambda lst: lst[1])
        current_state = frontier.pop()[0]
        expanded_node_num += 1

        #check if the current state meets the goal
        if goal_test(current_state):
            return current_state.move_sequence,expanded_node_num, prize_in_order

        #if we reach a prize in current state,
        #reset expanded_node_list and frontier and recalculate heuristic values for every unreached prize
        #update prize_in_order, heuristic_prize_list, and prize_position
        if len(current_state.prize_list) < last_prize_num:
            last_prize_num = len(current_state.prize_list)
            expanded_node_list.clear()
            frontier.clear()
            prize_in_order.append(heuristic_prize_list.pop())

            for i in range(len(heuristic_prize_list)):
                heuristic_prize_list[i][1] = heuristic_astar(current_state.position, heuristic_prize_list[i][0], len(current_state.move_sequence))
                heuristic_prize_list.sort(reverse=True, key=lambda lst: lst[1])
                prize_position = heuristic_prize_list[-1][0]
            heuristic_prize_list.sort(reverse=True, key=lambda lst: lst[1]) 
            prize_position = heuristic_prize_list[-1][0] 
            
        #expand the current node in 4 directions using transition function
        #append the new states to the frontier if valid
        for action in action_list:
            new_state = transition(current_state, action, maze_size, wall_positions, prize_list, current_state.position, expanded_node_list)
            if new_state:
                frontier.append([new_state, heuristic_astar(new_state.position, prize_position, len(new_state.move_sequence))])
                expanded_node_list.add(new_state.position)
    return None


def print_solution(maze_filename, maze_output):
    """
    Prints the solution to the output.
    """

    #import the maze to get information and get the solution by search algorithm
    maze_size, wall_positions, prize_list, start_position = import_maze(maze_filename)
    solution = multi_astar(maze_size, wall_positions, prize_list, start_position)
    prize_in_order = solution[2]
    prize_sequence = ['0', '1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i',
    'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    prize_th = 0

    with open(maze_output, 'w') as output:
        for j in range(maze_size[1]):
            for i in range(maze_size[0]):
                position = (i, j)
                if position == start_position:
                    output.write("P")
                elif position in wall_positions:
                    output.write("%")
                elif position in prize_in_order:
                    prize_th = prize_in_order.index(position)
                    output.write(prize_sequence[prize_th])
                elif position in solution[0] and position not in prize_in_order:
                    output.write("#")
                else:
                    output.write(" ")
            output.write("\n")
    print(len(solution[0]),solution[1])


if __name__ == "__main__":
    print_solution('multiprize-medium.txt','maze_output_medium.txt')
    print_solution('multiprize-tiny.txt','multi_maze_output_tiny.txt')
    print_solution('multiprize-small.txt', 'multi_maze_output_small.txt')