import copy

def import_maze(maze_filename):
    """
    Import the maze in text file to get necessary information
    
    maze_size: tuple (width,height)
    wall_positions: set of tuples
    prize_list: set of tuples
    start_position: tuple
    """
    prize_list = []
    start_position = (0,0)
    wall_positions = []
    with open(maze_filename,'r') as mazefile:
        original = mazefile.read().split('\n')
        height = len(original)
        width = len(original[0])
        maze_size = (len(original[0]),len(original)) #width * height
        for j in range(len(original)):
            for i in range(len(original[j])):
                if original[j][i] == '%':
                    wall_positions.append((i,j))
                elif original[j][i] == 'P':
                    start_position = (i,j)
                elif original[j][i] == '.':
                    prize_list.append((i,j))
    # print(prize_list)
    # print(_positions)
    return maze_size, wall_positions, prize_list, start_position


class StateRep():
    def __init__(self, position, move_sequence, prize_list):
        """
        position: tuple
        prize_list: set of tuples
        move_sequence: array
        """
        self.position = position
        self.move_sequence = move_sequence
        self.prize_list = prize_list


def transition (state, action, maze_size, wall_positions, prize_list, start_position, expanded_node_list):
    """
    Return new state

    state: StateRep instance
    action: [W, E, S, N]
    """
    x,y = 0,0
    if action == 'W':
        x = -1
    elif action == 'E':
        x = 1
    elif action == 'S':
        y = 1
    elif action == 'N':
        y = -1
    else:
        raise KeyError('Invalid action')
    
    anticipated_position = (state.position[0]+x, state.position[1]+y)

    #hit wall or repeated move or out_of_range position
    if ((anticipated_position in wall_positions) or 
       (anticipated_position in expanded_node_list)):# or
       #(anticipated_position[0] > (maze_size[0]-1) or anticipated_position[1] > (maze_size[1]-1)) or
       #(anticipated_position[0] < 0 or anticipated_position[1] < 0)) :
    
        return None
    #update state    
    new_state = copy.deepcopy(state)
    new_state.position = anticipated_position
    new_state.move_sequence.append(anticipated_position)
    #hit the prize
    if anticipated_position in state.prize_list:
        new_state.prize_list.remove(anticipated_position)

    return new_state


def goal_test(state):
    """Return True if all prizes are collected"""
    if len(state.prize_list) == 0:
        return True
    return False
