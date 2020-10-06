# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

"""

Question 1:

 Is the exploration order what you would have expected?

    Yes the order is what I expected. Since it is depth first search, pacman takes the first available move when given 
    several options. The moves are picked in the priority, West, East, South, and North respectively. This is due to
    the order in the get sucessors function:
    
                for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:

    Since we are using a stack which is last in first out this direction is reversed. Meaning at any point of conjunction
    it will take as many west moves as it can until it reaches a conclusion, then began taking east, south, north, etc 
    up the tree.
    

Does Pacman actually go to all the explored squares on his way to the goal?
    
    No Pacman does not. This is due to the fact the environment is known before game launch and we can calculate the 
    best path. With less information the pacman agent would have to explore the dead ends.

 Is this the least cost solution
    
    No this is not the least cost solution. Depth first search does not always return the most optimal solution,
    rather just the first solution path it encounters. A better path finding algorithm like A* finds a better path
    because it considers the cost.
    
Question 3:
    
 What happens on openMaze for the various search strategies?
 
    Depth first search performs very poorly here. It takes quite a while to find the solution and expands many nodes in
    the process. Bread first search works much better and finds the solution relatively quickly. UCS performs better
    by only a small margin, but A* reduces the amount of expanded notes. Below are the counts of expanded nodes:
    
        dfs - N/A inf
        bfs - 683 nodes
        ucs - 682 nodes
        A*  - 535 nodes
        
Question 7:

 Can you solve mediumSearch in a short time?
 
    No it actually takes quite a while! This is a both a good and bad thing as it means my heuristic is consistent.
"""

import util
from util import PriorityQueue
from util import PriorityQueueWithFunction
from util import Stack
from copy import deepcopy
import searchAgents


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def manhattanHeuristic(state, problem):
    return util.manhattanDistance(state, problem.goal)


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return DFS(problem, [[], [problem.getStartState()]])


def DFS(problem, item):
    paths = Stack()

    if problem.isGoalState(item[1][-1]):
        return item[0]

    for state in problem.getSuccessors(item[1][-1]):
        if (not state[0] in item[1]):
            copy = deepcopy(item)
            copy[0].append(state[1])
            copy[1].append(state[0])
            paths.push(copy)

    while not paths.isEmpty():
        directions = DFS(problem, paths.pop())
        if (directions):
            return directions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    visited = [problem.getStartState()]
    parentPath = Stack()
    parentPath.push([[], problem.getStartState()])

    while not parentPath.isEmpty():
        paths = parentPath
        parentPath = Stack()

        while not paths.isEmpty():

            item = paths.pop()

            if problem.isGoalState(item[1]):
                return item[0]

            for state in problem.getSuccessors(item[1]):
                if not state[0] in visited:
                    visited.append(state[0])

                    copy = deepcopy(item)
                    copy[0].append(state[1])
                    copy[1] = state[0]
                    parentPath.push(copy)


def uniformCostSearch(problem):
    # Used PriorityQueue to easily find lowest cost path
    frontier = PriorityQueue()
    visited = []

    # Push the start state with cost 0 to initiate the while loop
    frontier.push(problem.getStartState(), 0)
    frontList = [problem.getStartState()]

    paths = {}
    paths[problem.getStartState()] = []

    while not frontier.isEmpty():

        node = frontier.pop()
        frontList.remove(node)

        if problem.isGoalState(node):
            return paths[node]

        visited.append(node)

        for state in problem.getSuccessors(node):
            # Append move to path history
            path = deepcopy(paths[node])
            path.append(state[1])

            if state[0] not in visited and state[0] not in frontList:
                # Append move to path history
                paths[state[0]] = path

                # Finally push to the PriorityQueue
                frontier.push(state[0], problem.getCostOfActions(path))
                frontList.append(state[0])

            elif state[0] in frontList and problem.getCostOfActions(path) < problem.getCostOfActions(paths[state[0]]):
                frontier.update(state[0], problem.getCostOfActions(path))
                paths[state[0]] = path

    # No possible path to goal
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return ASTAR(problem, problem.getStartState(), heuristic)


def ASTAR(problem, start, heuristic):
    # Used PriorityQueue to easily find lowest cost path
    frontier = PriorityQueue()
    visited = []

    paths = {}
    paths[generateIndex(start)] = []

    frontier.push(start, 0)
    while not frontier.isEmpty():

        node = frontier.pop()
        path = paths[generateIndex(node)]

        if problem.isGoalState(node):
            return path

        visited.append(node)

        for state in problem.getSuccessors(node):
            # Append move to path history
            newPath = deepcopy(path)
            newPath.append(state[1])

            membership = False

            i = 0
            for item in frontier.heap:
                if item[2] == state[0]:
                    membership = True
                    break
                i += 1

            if state[0] not in visited and not membership:
                # Append move to path history

                # Finally push to the PriorityQueue
                frontier.push(state[0], problem.getCostOfActions(newPath) + heuristic(state[0], problem))
                paths[generateIndex(state[0])] = newPath
            elif membership:
                if (problem.getCostOfActions(newPath) + heuristic(state[0], problem)) < frontier.heap[i][0]:
                    frontier.update(state[0], problem.getCostOfActions(newPath) + heuristic(state[0], problem))
                    paths[generateIndex(state[0])] = newPath

    # No possible path to goal
    return []


def generateIndex(array):
    return hash(str(array))
    return hash(array)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
