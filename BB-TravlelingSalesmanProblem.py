####################################################################################
# Traveling Salesman Problem
# Solution Using Branch and Bound Algorithm.
# -----------------------------------------------------------
# Mark Barros
# CS3310 - Design and Analysis of Algorithms
# Cal Poly Pomona: Spring 2021
####################################################################################


# These are necessary imports. -----------------------------------------------------
import math
import csv # For reading csv files

# This holds the final minimum weight of shortest tour. ----------------------------
maxsize = float('inf')
  
# This copies the temporary solution to the final solution. ------------------------
def copyToFinal(curr_path):
    final_path[:nodes + 1] = curr_path[:]
    final_path[nodes] = curr_path[0]
  
# This finds the minimum edge cost haveing an end at the vertex i. -----------------
def firstMin(adj, i):
    min = maxsize
    for k in range(nodes):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
    return min
  
# This finds the second minimum edge cost having an end at the vertex i. -----------
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(nodes):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif(adj[i][j] <= second and 
             adj[i][j] != first):
            second = adj[i][j]
    return second
  
# This is where the magic happens. -------------------------------------------------
def TSPRec(adj, curr_bound, curr_weight, level, curr_path, visited):
    # curr_path[]: where the solution is being stored which
    #              would later be copied to final_path[]
    # curr_bound: lower bound of the root node
    # curr_weight: stores the weight of the path so far
    # level: current level while moving in the search space tree

    global final_res
      
    # This handles the base case (which is when all
    # nodes have been covered once).
    if level == nodes:
        # Check if there is an edge from last vertex
        # in path back to the first vertex.
        if adj[curr_path[level - 1]][curr_path[0]] != 0:    
            # curr_res holds the total weight of the gotten solution
            curr_res = curr_weight + adj[curr_path[level - 1]] [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return
  

    # This handles the recursive case.
    # For any other level iterate for all vertices to
    # build the search tree recursively.
    for i in range(nodes):
        # Consider next vertex if it is not same
        # (diagonal entry in adjacency matrix and not visited already)
        if (adj[curr_path[level-1]][i] != 0 and visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]
  
            # There is a different computation of curr_bound
            # for level 2 from the other levels.
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) \
                                + firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) \
                                + firstMin(adj, i)) / 2)
  
            # curr_bound + curr_weight is the actual lower
            # bound for the node arrived at.
            # If current lower bound < final_res, it is
            # necessary to explore the node further.
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True
                # recurse
                TSPRec(adj, curr_bound, curr_weight, level \
                       + 1, curr_path, visited)
  
            # Otherwise prune the node by resetting all the
            # changes to curr_weight and curr_bound.
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp
  
            # It is also necessary to reset the visited array.
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True
  
# This sets up the final path. -----------------------------------------------------
def TSP(adj):
      
    # Calculate initial lower bound for the root node using the formula:
    # 1/2 * (sum of first min + second min) for all edges.
    # Also initialize the curr_path and visited array.
    curr_bound = 0
    curr_path = [-1] * (nodes + 1)
    visited = [False] * nodes
  
    # Compute the initial bound.
    for i in range(nodes):
        curr_bound += (firstMin(adj, i) + secondMin(adj, i))
  
    # Round off the lower bound to an integer.
    curr_bound = math.ceil(curr_bound / 2)
  
    # Start at vertex 1 so the first vertex in curr_path[] is 0.
    visited[0] = True
    curr_path[0] = 0
  
    # Make a call to TSPRec for curr_weight equal to 0 and level 1.
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


# This is where the program execution begins. --------------------------------------
if __name__ == '__main__':

    # These are the necessary variables.
    values = []
    nodes = []
    matrix = []

    # This opens the input file as a csv.
    input_file = open('input.txt', 'r')
    reader = csv.reader(input_file)

    # This reads in the values.
    for row in reader:
        values.append(row)
 
    # This retrieves the number of nodes.
    nodes = values[0]
    nodes = list(map(int, nodes))
    nodes = int(nodes.pop(0))
    values.pop(0) # Discard the top value.

    # This retrieves the matrix values.
    matrix = [[int(int(j)) for j in i] for i in values]

    count = 0
    while(count < nodes):
        
        # final_path: stores the final solution
        # (i.e., the path of the salesman)
        final_path = [None] * (nodes + 1)
  
        # visited: keeps track of the already
        # visited nodes in a particular path.
        visited = [False] * nodes
  
        # Acquire the final minimum weight of the shortest tour.
        final_res = maxsize
  
        # This invokes the magic.
        TSP(matrix)

        count += 1

    # This is the output header.
    print("---------------------------------------------------------------")
    print("The Traveling Salesman Problem - By Mark Barros")
    print("---------------------------------------------------------------")

    # This outputs to the console the number of nodes
    # and the matrix values
    print("The matrix has", nodes, "nodes. It's values are:\n")
    for row in matrix:
        print("\t\t", *row)
    print("\n---------------------------------------------------------------")
    print("Solution: Path Taken for the optimal tour: ", end = ' ')
    for i in range(nodes + 1):
        print(final_path[i], end = ' ')
    print("\n\t\t  Length of the optimal tour:      ", final_res)
    print("---------------------------------------------------------------")

    # End of Module. ###############################################################