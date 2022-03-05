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

        self.g = math.inf
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

        while len(frontier) > 0:
            # sort by evaluation function
            frontier.sort(key=lambda node: node.f)
            # remove and get node with smallest f
            current_node = frontier[0]
            # test if goal is reached or not, if yes then return the path
            if current_node == end_node:
                return return_path(current_node)
            frontier.pop(0)
            expanded = self.environment.expand(current_node.state)
            for child in expanded:
                step_cost = child[1]
                child_node = Node()
                tentative_g = current_node.g + step_cost
                if tentative_g < child_node.g:
                    state = child[0]
                    child_node = Node(current_node, state)
                    child_node.g = tentative_g
                    child_node.h = euclidean_distance(child_node, end_node)
                    child_node.f = tentative_g + child_node.h
                    if child_node not in frontier:
                        frontier.append(child_node)
            # show environment GUI
            # TODO DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            self.environment.render()
            # sleep for demonstration
            # TODO DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            # time.sleep(0.1)
        return None


if __name__ == '__main__':
    MAP = sys.argv[1]  # 'maps/normal/normal8.bmp'
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)  # For using random map set: map_image=None
    agent = Agent(env)

    path = agent.find_path()
    print(path)
    env.set_path(path)  # set path it should go from the init state to the goal state
    if SAVE_PATH:
        env.save_path()  # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()  # save rendered image to eps
    env.render(mode='human')
    time.sleep(8)
    sys.exit(0)
