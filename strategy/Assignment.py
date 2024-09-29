import numpy as np

def role_assignment(teammate_positions, formation_positions): 
    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#
    
    assert len(teammate_positions) == len(formation_positions), "Mismatch in num teammates and formation positions."
    
    #construct cost matrix
    cost_matrix = construct_cost_matrix(teammate_positions, formation_positions)
    
    # Apply cost assignment alg
    row_ind, col_ind = hungarian_algorithm(cost_matrix)

    # Example
    point_preferences = {}
    for i in range(len(row_ind)):
        point_preferences[row_ind[i] + 1] = formation_positions[col_ind[i]]

    return point_preferences

def hungarian_algorithm(cost_matrix):
    # Step 1: Subtract row minimums
    for i in range(len(cost_matrix)):
        cost_matrix[i] -= np.min(cost_matrix[i])

    # Step 2: Subtract column minimums
    for j in range(len(cost_matrix[0])):
        cost_matrix[:, j] -= np.min(cost_matrix[:, j])

    # Step 3: Cover all zeros with minimum number of lines
    iterations = 0
    while True:
        zero_matrix = cost_matrix == 0
        row_cover = [False] * len(cost_matrix)
        col_cover = [False] * len(cost_matrix[0])

        # Mark rows with no zeros
        for i in range(len(cost_matrix)):
            if not any(zero_matrix[i]):
                row_cover[i] = True

        # Mark columns where a zero is present in a covered row
        for j in range(len(cost_matrix[0])):
            for i in range(len(cost_matrix)):
                if row_cover[i] and zero_matrix[i, j]:
                    col_cover[j] = True

        # Count the number of lines (row/col covers)
        lines_count = sum(row_cover) + sum(col_cover)
        if lines_count >= len(cost_matrix):
            break

        # Step 4: Adjust the matrix if the minimum number of covering lines < n
        min_val = np.inf
        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[0])):
                if not row_cover[i] and not col_cover[j]:
                    min_val = min(min_val, cost_matrix[i, j])

        # Step 5: Adjust cost matrix
        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[0])):
                if not row_cover[i] and not col_cover[j]:
                    cost_matrix[i, j] -= min_val
                if row_cover[i] and col_cover[j]:
                    cost_matrix[i, j] += min_val

        iterations += 1
        if iterations > 1000:  # safeguard
            break

    # Step 6: Find the optimal assignment
    row_ind, col_ind = [], []
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            if cost_matrix[i, j] == 0:
                row_ind.append(i)
                col_ind.append(j)

    return row_ind, col_ind

def construct_cost_matrix(teammate_positions, formation_positions):
    num_teammates = len(teammate_positions)
    cost_matrix = np.zeros((num_teammates, num_teammates))
    
    # calcu euclidean dist btwn teammates and formation positions
    for i in range(num_teammates):
        for j in range(num_teammates):
            cost_matrix[i, j] = np.linalg.norm(teammate_positions[i] - formation_positions[j])
    
    return cost_matrix



def pass_reciever_selector(player_unum, teammate_positions, final_target):
    
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#

    # Example
    pass_reciever_unum = player_unum + 1                  #This starts indexing at 1, therefore player 1 wants to pass to player 2
    
    if pass_reciever_unum != 12:
        target = teammate_positions[pass_reciever_unum-1] #This is 0 indexed so we actually need to minus 1 
    else:
        target = final_target 
    
    return target


## test
teammate_positions = np.array([
    [-13, 0], [-10, -2], [-11, 3], [-8, 0], [-3, 0],
    [0, 1], [2, 0], [3, 3], [8, 0], [9, 1], [12, 0]
])

formation_positions = np.array([
    [-13, 0], [-10, -2], [-11, 3], [-8, 0], [-3, 0],
    [0, 1], [2, 0], [3, 3], [8, 0], [9, 1], [12, 0]
])

assignment = role_assignment(teammate_positions, formation_positions)
print(assignment)
