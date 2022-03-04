#!/usr/bin/python3

import math
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


class Agent(kuimaze.BaseAgent):
    """
    Simple example of agent class that inherits kuimaze.BaseAgent class
    """

    def __init__(self, environment):
        self.environment = environment

    def return_path(self):
        return 0

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
        frontiers = [start_node]  # init by start node
        explored = []

        # Adding a stop condition. This is to avoid any infinite loop and stop
        # execution after some reasonable number of steps
        outer_iterations = 0
        max_iterations = (self.environment._xsize // 2) ** 10

        while len(frontiers) > 0:
            outer_iterations += 1

            if outer_iterations > max_iterations:
                print("too many iterations")
                break

            # sort by evaluation function
            frontiers.sort(key=lambda node: node.f)
            # remove and get node with smallest f
            current_node = frontiers.pop(0)
            explored.append(current_node)

            # test if goal is reached or not, if yes then return the path
            if current_node == end_node:
                return self.return_path()

            # Generate children from all adjacent squares
            # [[(x1, y1), cost], [(x2, y2), cost], ... ]
            expanded = self.environment.expand(current_node.state)

            for child in expanded:
                state = child[0]
                child_node = Node(current_node, state)
                if child_node in explored:
                    continue
                step_cost = child[1]
                child_node.g = step_cost + current_node.g
                child_node.h = euclidean_distance(child_node, end_node)
                child_node.f = child_node.g + child_node.h

                # Child is already in the frontiers and there is lower cost
                # TODO simplify
                if len([node for node in frontiers if child_node == node and child_node.g > node.g]) > 0:
                    continue

                # Add the child to the yet_to_visit list
                frontiers.append(child_node)

            # show environment GUI
            # DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            self.environment.render()
            # sleep for demonstration
            # DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!
            time.sleep(0.5)
        return self.return_path()


if __name__ == '__main__':
    MAP = 'maps/easy/easy3.bmp'
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
    time.sleep(3)
