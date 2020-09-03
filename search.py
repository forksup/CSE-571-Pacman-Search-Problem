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
import searchAgents
import util
import copy


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self, other):
        self.problem = other

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def DFS(Problem, Start, Visited):
    paths = []
    for state in Problem.getSuccessors(Start):
        if (state[0] not in Visited):
            direction = [state[1]];
            Visited.append(state[0])
            result = DFS(Problem, state[0], Visited);
            if (Problem.isGoalState(state[0])):
                return direction;
            if ("" not in result):
                combined = direction + result
                paths.append(combined);
    if (paths):
        return paths[0];
    else:
        return "";


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    return DFS(problem, problem.getStartState(), [])

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # Q Format [Node, Parent]
    if (hasattr(problem,'corners')):
        pathsFinal = PriorityQueue()
        corners = problem.corners
        paths = util.Queue()
        i = 0
        for corner in corners:
            visitedCorners = [corner]
            problem.goal = corner
            result = breadExecute(problem,problem.getStartState())
            paths.push([corner, visitedCorners, result])
        while(len(paths.list) > 0):
            item = paths.pop()
            if(len(item[1]) < 4):
                for corner in corners:
                    if(corner not in item[1]):
                        problem.goal = corner
                        newItem = copy.deepcopy(item)
                        newItem[1].append(corner)
                        newItem[2] = newItem[2] + (breadExecute(problem,newItem[0]))
                        newItem[0] = corner
                        paths.push(newItem)
            else:
                pathsFinal.push([item[2]],len(item))
        return pathsFinal.pop()[0]
    else: return breadExecute(problem,problem.getStartState());

def breadExecute(problem,start):
    """Search the shallowest nodes in the search tree first."""
    # Q Format [Node, Parent]
    Visited = []
    q = [start]
    paths = {start: ""}
    while (len(q) > 0):
        item = q[0]
        if problem.isGoalState(item):
            buildDirection = paths[item]
            directions = []
            while len(buildDirection) > 1:
                directions.append(buildDirection[1])
                buildDirection = paths[buildDirection[0]]
            directions.reverse()
            return directions
        Visited.append(item);
        for state in problem.getSuccessors(item):
            # [Direction, item]
            if state[0] not in Visited:
                q.append(state[0])
                paths[state[0]] = [item, state[1]];
        q.pop(0)
    asdf = ""

from util import PriorityQueue

def uniformCostSearch(problem):
    q = PriorityQueue()
    q.push([[problem.getStartState()], []], 0)
    while (not q.isEmpty()):
        cost = q.heap[0][0]
        item = q.pop()
        if (problem.goal in item[0]):
            return item[1]
        for state in problem.getSuccessors(item[0][-1]):
            if (state[0] not in item[0]):
                newList = copy.deepcopy(item)
                newList[0].append(state[0])
                newList[1] = copy.deepcopy(item[1])
                newList[1].append(state[1])
                q.push(newList, problem.getCostOfActions(newList[1]))
    return []

def nullHeuristic(state, problem):
    return util.manhattanDistance(state, problem.goal)

def ASTAR(problem,start,heuristic=nullHeuristic):
    q = PriorityQueue()
    q.push([[start], []], 0)
    while (not q.isEmpty()):
        cost = q.heap[0][0]
        item = q.pop()
        if (problem.isGoalState(item[0][-1])):
            return item[1]
        for state in problem.getSuccessors(item[0][-1]):
            if (state[0] not in item[0]):
                newList = copy.deepcopy(item)
                newList[0].append(state[0])
                newList[1] = copy.deepcopy(item[1])
                newList[1].append(state[1])
                q.push(newList, problem.getCostOfActions(newList[1])+heuristic(state[0],problem))

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    if(heuristic == searchAgents.cornersHeuristic):
        pathsFinal = PriorityQueue()
        corners = problem.corners
        paths = util.Queue()
        i = 0
        shortestCorner = PriorityQueue()
        for corner in corners:
            problem.goal = corner
            shortestCorner.push(corner, heuristic(problem.getStartState(),problem))
        corner = shortestCorner.pop()
        visitedCorners = [corner]
        problem.goal = corner
        result = ASTAR(problem,problem.getStartState(),heuristic)
        paths.push([corner, visitedCorners, result])
        while(len(paths.list) > 0):
            item = paths.pop()
            if(len(item[1]) < 4):
                shortestCorner = PriorityQueue()
                for corner in corners:
                    if(corner not in item[1]):
                        problem.goal = corner
                        shortestCorner.push(corner,heuristic(item[0],problem))
                if(len(shortestCorner.heap) > 0):
                    corner = shortestCorner.pop()
                    problem.goal = corner
                    newItem = copy.deepcopy(item)
                    newItem[1].append(corner)
                    newItem[2] = newItem[2] + (ASTAR(problem,newItem[0],heuristic))
                    newItem[0] = corner
                    paths.push(newItem)
            else:
                pathsFinal.push([item[2]],len(item))
        return pathsFinal.pop()[0]
    else:
        return ASTAR(problem,problem.getStartState(),heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
