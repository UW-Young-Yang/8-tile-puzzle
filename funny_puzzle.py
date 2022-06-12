import heapq




def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    from_state_2d = [[0 for i in range(3)] for j in range(3)]
    to_state_2d = [[0 for i in range(3)] for j in range(3)]
    for i in range(9):
        row = i // 3
        col = i % 3
        from_state_2d[row][col] = from_state[i]
        to_state_2d[row][col] = to_state[i]

    distance = 0
    for row in range(3):
        for col in range(3):
            tile = to_state_2d[row][col]
            if tile == 0: continue
            for row2 in range(3):
                for col2 in range(3):
                    search = from_state_2d[row2][col2]
                    if tile == search:
                        distance += abs(row2-row) + abs(col2-col)
                        break
                if tile == search: break
    return distance




def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states = []
    for i in range(len(state)):
        if state[i] != 0:
            if i-3 >= 0 and state[i-3] == 0:
                temp = state[:]
                temp[i-3] = temp[i]
                temp[i] = 0
                succ_states.append(temp)
            if i+3 < len(state) and state[i+3] == 0:
                temp = state[:]
                temp[i+3] = temp[i]
                temp[i] = 0
                succ_states.append(temp)
            if (i-1) % 3 != 2 and i-1 >= 0 and state[i-1] == 0:
                temp = state[:]
                temp[i-1] = temp[i]
                temp[i] = 0
                succ_states.append(temp)
            if (i+1) % 3 != 0 and i+1 < len(state) and state[i+1] == 0:
                temp = state[:]
                temp[i+1] = temp[i]
                temp[i] = 0
                succ_states.append(temp)
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    index_dict = dict()
    curr = state[:]
    g = 0
    h = get_manhattan_distance(curr, goal_state)
    cost = g + h
    pq = []
    visited = []
    b = (cost, curr, (g, h, -1))
    heapq.heappush(pq, b)
    visited.append(curr)
    index_dict[0] = b
    max_queue = 1
    while (len(pq) != 0):
        b = heapq.heappop(pq)
        curr = b[1]
        g = b[2][0]+1
        parent_index = visited.index(curr)
        
        if curr == goal_state: # goal
            result = [b]
            parent_index = b[2][2]
            while parent_index != -1:
                b = index_dict[parent_index]
                parent_index = b[2][2]
                result.insert(0, b)
            for b in result:
                print(f'{b[1]} h={b[2][1]} moves: {b[2][0]}')
            print(f'Max queue length: {max_queue}')
            return 
        moves = get_succ(curr)
        for succ in moves:
            if succ in visited:
                i = visited.index(succ)
                b = index_dict[i]
                if b[2][0] > g:
                    h = b[2][1]
                    cost = g + h
                    b = (cost, succ, (g, h, parent_index))
                    index_dict[i] = b
                    heapq.heappush(pq, b)
            else:
                h = get_manhattan_distance(succ, goal_state)
                cost = g + h
                b = (cost, succ, (g, h, parent_index))
                index_dict[len(visited)] = b
                visited.append(succ)
                heapq.heappush(pq, b)
        max_queue = max(max_queue, len(pq))


if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    import time
    start = time.time()
    solve([7,6,5,4,3,2,1,0,0])
    print(f'Solve spent: {time.time()-start}s')
    # solve([4,3,0,5,1,6,7,2,0])
    # print()
    # solve([2,5,1,4,0,6,7,0,3])
    # print()
