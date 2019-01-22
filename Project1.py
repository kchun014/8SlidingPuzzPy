# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:13:47 2018

@author: Kau
"""

import heapq as hq
import copy
import sys
import time

#keep track of states already expanded
Track = set()
#keep track of max number of items in the queuem and expanded nodes.
num_exp = 0;
num_queue = 0;

sys.stdout = open('output.txt', 'w')
def EXPAND(puzzle, operators): #expands queue, based on valid operators
    state = puzzle.state
    actionbool = operators
    
    dummy_state = [0]
    
    push_vals = []
    #check if valid options, then check if already explored.
    #if explored, append a dummy state which is evaluated and ignored
    #if not explored, will push to queue and to the set, for repeated state tracking
    if actionbool[0]:
        appendval = Puzzle.move_up(state)
        temp = tuple(appendval)
#        print(temp)
        if temp not in Track:
#            print(temp)
            Track.add(temp)
            push_vals.append(appendval)
        else:
            push_vals.append(dummy_state)
            
    if actionbool[1]:
        appendval = Puzzle.move_down(state)
        temp = tuple(appendval)
        if temp not in Track:    
#            print(temp)
            Track.add(temp)
            push_vals.append(appendval)
        else:
            push_vals.append(dummy_state)
        
    if actionbool[2]:
        appendval = Puzzle.move_left(state)
        temp = tuple(appendval)
#        print(temp)
        if temp not in Track:
            Track.add(temp)
            push_vals.append(appendval)
        else:
            push_vals.append(dummy_state)
        
    if actionbool[3]:
        appendval = Puzzle.move_right(state)
        temp = tuple(appendval)
#        print(temp)
        if temp not in Track:
            Track.add(temp)
            push_vals.append(appendval)
        else:
            push_vals.append(dummy_state)
    return (puzzle, push_vals)

def Uniform_Cost(queue, expanded_nodes):
    for i in range(len(expanded_nodes[1])):
        if len(expanded_nodes[1][i]) != 1:
            #Declare copy of puzzle, append values as necessary
            new_puzzle = copy.deepcopy(expanded_nodes[0])
            new_puzzle.addNode(1, expanded_nodes[1][i])
            hq.heappush(queue, (new_puzzle.cost, new_puzzle))
    return queue

def Misplaced_Cost(state):
    cost = 0
    for index, value in enumerate(state):
        if (((index + 1) != value) and value != 8):
            cost += 1
    return cost

def Misplaced_Tile(queue, expanded_nodes):
#    print(expanded_nodes[1])
    for i in range(len(expanded_nodes[1])):
        #TODO: try to figure out how to ignore a list with one value
      if len(expanded_nodes[1][i]) != 1:
            #Declare copy of puzzle, append values as necessary
            new_puzzle = copy.deepcopy(expanded_nodes[0])
            new_puzzle.state = expanded_nodes[1][i]
            hN = Misplaced_Cost(new_puzzle.state);
            new_puzzle.addNode(hN, expanded_nodes[1][i])
            hq.heappush(queue, (new_puzzle.cost, new_puzzle))
    return queue

def Manhattan_Cost(state):
    cost = 0
    for index, value in enumerate(state):
        #get diff for each value. i.e. 1 if values are 1 and 2, regardless of order.
        #Ignore 0.
        if(value != 0):
            x = abs(index + 1 - value)
            #If 3 away, is actually 1 away, if remainder is also 1 away, outputs number of spaces away
            cost += (int)(x / 3) + (int)(x % 3)
    return cost

def Manhattan(queue, expanded_nodes):
#    print(expanded_nodes[1])
    for i in range(len(expanded_nodes[1])):
        if len(expanded_nodes[1][i]) != 1:
            #Declare copy of puzzle, append values as necessary
            new_puzzle = copy.deepcopy(expanded_nodes[0])
            new_puzzle.state = expanded_nodes[1][i]
            hN = Manhattan_Cost(new_puzzle.state);
            #update depth in the new node
            new_puzzle.addNode(hN, expanded_nodes[1][i])
            hq.heappush(queue, (new_puzzle.cost, new_puzzle))
    return queue

class Puzzle:
    def __init__(self, start, goal):
        self.goal = goal
        self.state = start
        #Stores G(n), H(n), state
        self.depth = 0 #acts as G(n)
        self.cost = 0 #acts as h(n)
        self.solution = [(self.depth, self.cost, start)]
        self.max_queue = 0
        

    def __lt__(self, cost2):
        return self.cost < cost2.cost
    
    def addNode(self, addedCost, newState):
        self.state = newState
        self.depth += 1
        old_cost = self.cost
        self.cost = self.cost + addedCost
        self.solution.append((old_cost, addedCost, newState))
        
    
    def can_move(self):
        zero_location = self.state.index(0)
        #determines what actions are actually valid
        actionbool = [False, False, False, False]
        #cannot move up, if already on top row
        if zero_location >= 3:
            actionbool[0] = True
        #cannot move down, if already on bottom row
        if zero_location <= 5:
            actionbool[1] = True
        #cannot move left, if already on left
        if(zero_location != 0 and zero_location != 3 and zero_location != 6):
            actionbool[2] = True
        #cannot move right, if already on right
        if(zero_location != 2 and zero_location != 5 and zero_location != 8):
            actionbool[3] = True
        return actionbool    
    #code actions, move up, down, left, right, check is above. Passed in state is a LIST.
    def move_up(state):
        zero_location = state.index(0)
        copy = state.copy()
        copy[zero_location], copy[zero_location-3] = state[zero_location-3], state[zero_location]
        return copy
    
    def move_down(state):
        zero_location = state.index(0)
        copy = state.copy()
        copy[zero_location], copy[zero_location+3] = state[zero_location+3], state[zero_location]
        return copy
    
    def move_left(state):
        zero_location = state.index(0)
        copy = state.copy()
        copy[zero_location], copy[zero_location-1] = copy[zero_location-1], copy[zero_location]
        return copy
    
    def move_right(state):
        zero_location = state.index(0)
        copy = state.copy()
        copy[zero_location], copy[zero_location+1] = copy[zero_location+1], copy[zero_location]
        return copy
        
#function general-search(problem, QUEUEING-FUNCTION)  
#nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE)) 
#loop do
# if EMPTY(nodes) then return "failure" 
#   node = REMOVE-FRONT(nodes) 
# if problem.GOAL-TEST(node.STATE) succeeds then return node
#    nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))  
# end

def AStarAlgorithm(Problem, Queueing_Function):
#nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE)) 
    q = []
    hq.heappush(q, (0, Problem))
    global num_exp 
    global num_queue
    num_exp = 0
    num_queue = 1;
    #loop infinitely until queue empty or not
    while(True):
# if EMPTY(nodes) then return "failure" 
        if len(q) == 0:
            print("Failure!")
            Problem.solution = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            return Problem #indicator for no solution
#   node = REMOVE-FRONT(nodes) 
        #will be tuple, with (current list, f(n) [cost], path)
        current_puzzle = hq.heappop(q)[1]
        num_exp += 1
# if problem.GOAL-TEST(node.STATE) succeeds then return node
        if(current_puzzle.goal == current_puzzle.state):
            return current_puzzle
#    nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        if Queueing_Function == 1: 
            q = Uniform_Cost(q, EXPAND(current_puzzle, current_puzzle.can_move()))
        elif Queueing_Function == 2:
            q = Misplaced_Tile(q, EXPAND(current_puzzle, current_puzzle.can_move()))
        elif Queueing_Function == 3:
            q = Manhattan(q, EXPAND(current_puzzle, current_puzzle.can_move()))
        else:
            print("Wrong algorithm number!")
            return current_puzzle #give error if somehow another thing is inputted
        if len(q) > num_queue:
            num_queue = len(q)
    if Problem.state.array_equals(Problem.goal):
        return current_puzzle

def main():
    global num_queue
    print("Welcome to Kau Chung's 8-puzzle solver.")
    sys.stdout.write("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.\n")
    puzznum = int(input())
    if(puzznum == 2):
        print("Enter your puzzle, use a zero to represent the blank")
        print("Enter the first row, use a space or tabs between numbers")
        #Input first row
        row1 = [int(x) for x in input().split()]
        print("Enter the second row, use a space or tabs between numbers")
        #Input second row
        row2 = [int(x) for x in input().split()]
        print("Enter the third row, use a space or tabs between numbers")
        #Input third row
        row3 = [int(x) for x in input().split()]
        start = row1 + row2 + row3
    else:
        start = [1, 2, 3, 4, 8, 0, 7, 6, 5]
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    print("Enter your choice of algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* with the Misplaced Tile heuristic")
    sys.stdout.write("3. A* with the Manhattan Distance heuristic\n")
    
    algnum = int(input()) #take input to get algnum
    puzzle = Puzzle(start, goal)
    start_time = time.time()
    solution_puzzle = AStarAlgorithm(puzzle, algnum)
    end_time = time.time()
    solution = solution_puzzle.solution
    error = True;
    #parse for whether solution exists
    for x in solution:
        if x != 0:
            error = False;
    if(not error):
        #output solution
        print("Expanding state:")
        print(start[0:3])
        print(start[3:6])
        print(start[6:])
        if solution[1] != 0:
            for i in solution[1:]:
                print("The best state to expand with g(n) = " + str(i[0]) + " and h(n) = " + str(i[1]) + " is...")
                print(i[2][0:3])
                print(i[2][3:6])
                if i[2] != goal:
                    print(str(i[2][6:]) + " Expanding this node...")
                else:
                    print(str(i[2][6:]) + " Solution found!")
        print("Number of nodes explored: " + str(num_exp))
        print("The maximum number of nodes in the queue at any given time was " + str(num_queue) + ".")
        print("The depth of the goal node was " + str(solution_puzzle.depth))
        print("The time it took to run the algorithm was: " + str(end_time-start_time) + " seconds.")
        f = open("output.csv", "a+")
        f.write("Puzzle, " + str(start) + ", algnum, " + str(algnum) + ", time, " + str(end_time - start_time) + ", space, " + str(num_queue) + "\n")
if __name__ == "__main__":
    main()    