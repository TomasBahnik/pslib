#!/usr/bin/python3

import math
import sys
import time

import kuimaze


class Node:
    """
        Search node class
        g(n) is path cost from start node to the (current node) n (the cost to reach the node n)
        h(n) estimated cost of the cheapest path from the state at node n to a goal state
        f(n) = g(n) + h(n) estimated cost of the cheapest solution through node n
    """

    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.state == other.state


def euclidean_distance(node1, node2):
    return math.sqrt(((node1.state[0] - node2.state[0]) ** 2 + (node1.state[1] - node2.state[1]) ** 2))


def return_path(end_node):
    n = end_node
    ret_val = [n.state]
    while n.parent is not None:
        ret_val.append(n.parent.state)
        n = n.parent
    return list(reversed(ret_val))


# function UNIFORM-COST-SEARCH(problem) returns a solution, or failure
#   node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
#   frontier ← a priority queue ordered by PATH-COST, with node as the only element
#   explored ← an empty set
#   loop do
#     if EMPTY?(frontier) then return failure
#     node ← POP(frontier) /* chooses the lowest-cost node in frontier */
#     if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
#     add node.STATE to explored
#     for each action in problem.ACTIONS(node.STATE) do
#       child ← CHILD-NODE(problem,node,action)
#       if child.STATE is not in explored or frontier then
#           frontier ← INSERT(child,frontier)
#       else if child.STATE is in frontier with higher PATH-COST then
#           replace that frontier node with child


class Agent(kuimaze.BaseAgent):
    """
    Simple example of agent class that inherits kuimaze.BaseAgent class
    """

    def __init__(self, environment):
        self.environment = environment

    def find_path(self):
        """
        Method that must be implemented by you.
        Expects to return a path_section as a list of positions [(x1, y1), (x2, y2), ... ].
        """
        observation = self.environment.reset()  # must be called first, it is necessary for maze initialization
        start_node = Node(None, tuple(observation[0][0:2]))
        end_node = Node(None, tuple(observation[1][0:2]))
        start_node.h = euclidean_distance(start_node, end_node)
        start_node.g = 0
        start_node.f = start_node.g + start_node.h
        end_node.g = end_node.h = end_node.f = 0
        frontier = [start_node]  # init by start node
        explored = []

        while True:
            if len(frontier) == 0:
                return None
            # sort by evaluation function
            frontier.sort(key=lambda node: node.f)
            # remove and get node with smallest f
            current_node = frontier.pop(0)
            # test if goal is reached or not, if yes then return the path
            if current_node == end_node:
                return return_path(current_node)
            explored.append(current_node)
            expanded = self.environment.expand(current_node.state)
            for child in expanded:
                state = child[0]
                child_node = Node(current_node, state)
                step_cost = child[1]
                child_node.g = step_cost + current_node.g
                child_node.h = euclidean_distance(child_node, end_node)
                child_node.f = child_node.g + child_node.h
                # if child.STATE is not in explored or frontier then
                # frontier ← INSERT(child,frontier)
                if (child_node not in explored) and (child_node not in frontier):  # state is used for comparison
                    frontier.append(child_node)
                # else if child.STATE is in frontier with higher PATH-COST then
                # TODO check len must be 0 or 1
                elif len([node for node in frontier if child_node == node and node.f > child_node.f]) > 0:
                    # replace that frontier node with child
                    frontier_states = [x.state for x in frontier]
                    state_idx = frontier_states.index(child_node.state)
                    frontier[state_idx] = child_node
            # show environment GUI
            # TODO DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            # if SHOW:
            #     self.environment.render()
            # sleep for demonstration
            # TODO DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            # time.sleep(0.01)


SHOW = None  # enables env GUI and show the resulting image for SHOW sec
if __name__ == '__main__':
    MAP = sys.argv[1]  # 'maps/normal/normal11.bmp'
    SHOW = int(sys.argv[2]) if len(sys.argv) > 2 else None
    GRAD = (0, 0)
    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)  # For using random map set: map_image=None
    agent = Agent(env)
    t0 = time.perf_counter()
    path = agent.find_path()
    delta = time.perf_counter() - t0
    print("{} : path len {}, takes {} sec".format(MAP, len(path), delta))
    print("path\n{}".format(path))
    if SHOW:
        env.set_path(path)  # set path it should go from the init state to the goal state
        env.render(mode='human')
        time.sleep(SHOW)
