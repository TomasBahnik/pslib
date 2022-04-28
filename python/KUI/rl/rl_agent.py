#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
A sandbox for playing with the HardMaze
@author: Tomas Svoboda
@contact: svobodat@fel.cvut.cz
@copyright: (c) 2017, 2018
'''

import os
import sys
import time
from time import sleep

import numpy as np

import kuimaze

# PROBS = [0.8, 0.1, 0.1, 0]
PROBS = [1, 0, 0, 0]
GRAD = (0, 0)
SKIP = False
VERBOSITY = 2

GRID_WORLD3 = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0]],
               [[255, 255, 255], [0, 0, 0], [255, 255, 255], [0, 255, 0]],
               [[0, 0, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]


# MAP = GRID_WORLD3


def wait_n_or_s():
    def wait_key():
        """
        returns key pressed ... works only in terminal! NOT in IDE!
        """
        result = None
        if os.name == 'nt':
            import msvcrt
            # https://cw.felk.cvut.cz/forum/thread-3766-post-14959.html#pid14959
            result = chr(msvcrt.getch()[0])
        else:
            import termios
            fd = sys.stdin.fileno()

            oldterm = termios.tcgetattr(fd)
            newattr = termios.tcgetattr(fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)
            try:
                result = sys.stdin.read(1)
            except IOError:
                pass
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        return result

    '''
    press n - next, s - skip to end ... write into terminal
    '''
    global SKIP
    x = SKIP
    while not x:
        key = wait_key()
        x = key == 'n'
        if key == 's':
            SKIP = True
            break


def get_visualisation(table):
    ret = []
    for i in range(len(table[0])):
        for j in range(len(table)):
            ret.append({'x': j, 'y': i, 'value': [table[j][i][0], table[j][i][1], table[j][i][2], table[j][i][3]]})
    return ret


def get_visualisation_values(dictvalues):
    if dictvalues is None:
        return None
    ret = []
    for key, value in dictvalues.items():
        ret.append({'x': key[0], 'y': key[1], 'value': value})
    return ret


def get_greedy_policy(q_table):
    pi = dict()
    # TODO handle terminal and obstacle states as in MDP
    for y in range(len(q_table[0])):  # grid y
        for x in range(len(q_table)):  # grid x
            key = (x, y)
            action_values = q_table[x, y]
            max_action_value = np.argmax(action_values)
            # str representation od action for visualization
            action = kuimaze.maze.ACTION(max_action_value)
            # action = max_action_value
            pi[key] = action
    return pi


def sarsa(env, num_episodes, eps0=0.5, alpha=0.5, max_trials=1000):
    """ On-policy Sarsa algorithm (with exploration rate decay) """

    # Env size
    x_dims = env.observation_space.spaces[0].n
    y_dims = env.observation_space.spaces[1].n

    # Number of discrete actions
    n_action = env.action_space.n
    # Initialize action-value function - Q-table
    q = np.zeros([x_dims, y_dims, n_action], dtype=float)

    # check the sum of probabilities
    ones = np.ones([x_dims, y_dims], dtype=float)
    # Initialize policy to equal-probable random
    policy = np.ones([x_dims, y_dims, n_action], dtype=float) / n_action

    for episode in range(num_episodes):
        # Reset the environment
        state = env.reset()
        state_idx = state[0:2]
        action = np.random.choice(n_action, p=policy[state_idx[0], state_idx[1]])

        done = False
        trials = 0
        while not done and trials < max_trials:
            trials += 1
            idx_x = state_idx[0]
            idx_y = state_idx[1]
            # Step the environment forward and check for termination
            next_state, reward, done, _ = env.step(action)
            next_state_idx = next_state[0:2]
            next_state_idx_x = next_state_idx[0]
            next_state_idx_y = next_state_idx[1]
            next_action = np.random.choice(n_action, p=policy[next_state_idx_x, next_state_idx_y])

            # Update q values
            q[idx_x, idx_y, action] += alpha * (reward + q[next_state_idx_x, next_state_idx_y, next_action]
                                                - q[idx_x, idx_y, action])

            # Extract eps-greedy policy from the updated q values
            eps = eps0 / (episode + 1)
            max_action_value = np.argmax(q[idx_x, idx_y])
            policy[idx_x, idx_y, :] = eps / n_action
            policy[idx_x, idx_y, max_action_value] = 1 - eps + eps / n_action
            assert np.allclose(np.sum(policy, axis=2), ones)

            # Prepare the next q update
            state_idx = next_state_idx
            action = next_action
    return q, policy


if __name__ == "__main__":
    # map_rel = 'maps_difficult/maze50x50.png'
    # map_rel = 'maps_difficult/maze50x50_22.png'
    # map_rel = 'maps/easy/easy1.bmp'
    # map_rel = 'maps/normal/normal12.bmp'
    map_rel = 'maps/normal/normal11.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), map_rel)
    # Initialize the maze environment
    env = kuimaze.HardMaze(map_image=MAP, probs=PROBS, grad=GRAD)
    # TODO replace num of episodes by time limit
    num_episodes = 1000
    eps0 = 0.5  # 0.5 default
    t0 = time.perf_counter()
    q_table, policy = sarsa(env, num_episodes=num_episodes, eps0=eps0)
    delta = time.perf_counter() - t0
    print("sarsa : episodes{}, eps0={}, {} sec".format(num_episodes, eps0, delta))
    if VERBOSITY > 0:
        # env.visualise(get_visualisation(q_table))
        greedy_policy = get_greedy_policy(q_table)
        # print("policy {}".format(greedy_policy))
        env.visualise(get_visualisation_values(greedy_policy))
        env.render()
        sleep(20)
    sys.exit(0)

