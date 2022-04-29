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
VERBOSITY = 0

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
    # HardMaze does not have is_goal_state function policy on goal state is not None
    for y in range(len(q_table[0])):  # grid y
        for x in range(len(q_table)):  # grid x
            key = (x, y)
            action_values = q_table[x, y]
            max_action_value = np.argmax(action_values)
            # str representation od action for visualization
            # action = kuimaze.maze.ACTION(max_action_value)
            action = max_action_value
            pi[key] = action
    return pi


DEFAULT_TIME_LIMIT_SEC = 18


def sarsa(problem, time_limit_sec=DEFAULT_TIME_LIMIT_SEC, eps0=0.5, alpha=0.5, max_trials=1000):
    """ On-policy Sarsa algorithm with exploration rate decay """
    t0 = time.perf_counter()
    # Env size
    x_dims = problem.observation_space.spaces[0].n
    y_dims = problem.observation_space.spaces[1].n

    # Number of discrete actions
    n_action = problem.action_space.n
    # Initialize action-value function - Q-table
    q = np.zeros([x_dims, y_dims, n_action], dtype=float)

    # check the sum of probabilities
    ones = np.ones([x_dims, y_dims], dtype=float)
    # Initialize policy to equal-probable random
    eps_greedy_policy = np.ones([x_dims, y_dims, n_action], dtype=float) / n_action

    delta = time.perf_counter() - t0
    episode = 0  # needed for decay
    while delta < time_limit_sec:
        episode += 1
        # Reset the environment
        state = problem.reset()
        state_idx = state[0:2]
        action = np.random.choice(n_action, p=eps_greedy_policy[state_idx[0], state_idx[1]])

        done = False
        trials = 0
        while not done and trials < max_trials:
            trials += 1
            idx_x = state_idx[0]
            idx_y = state_idx[1]
            # Step the environment forward and check for termination
            next_state, reward, done, _ = problem.step(action)
            next_state_idx = next_state[0:2]
            next_state_idx_x = next_state_idx[0]
            next_state_idx_y = next_state_idx[1]
            # random choice from range(n_action) with probabilities p
            next_action = np.random.choice(n_action, p=eps_greedy_policy[next_state_idx_x, next_state_idx_y])

            # temporary difference update q values
            q[idx_x, idx_y, action] += alpha * (reward + q[next_state_idx_x, next_state_idx_y, next_action]
                                                - q[idx_x, idx_y, action])

            # Extract eps-greedy policy from the updated q values
            eps = eps0 / (episode + 1)
            max_action_value = np.argmax(q[idx_x, idx_y])
            eps_greedy_policy[idx_x, idx_y, :] = eps / n_action
            eps_greedy_policy[idx_x, idx_y, max_action_value] = 1 - eps + eps / n_action
            # check if eps-greedy policy probabilities sum to ~1
            assert np.allclose(np.sum(eps_greedy_policy, axis=2), ones)

            # Prepare the next q update
            state_idx = next_state_idx
            action = next_action
        delta = time.perf_counter() - t0
    return q, eps_greedy_policy, episode


# time_limit_sec : default = 20 is max by assigment but not always optimal
def learn_policy(problem, time_limit_sec=DEFAULT_TIME_LIMIT_SEC):
    eps0 = 0.5  # 0.5 default
    alpha = 0.5  # 0.5 default
    # t0 = time.perf_counter()
    q_table, eps_greedy_policy, episodes = sarsa(problem, time_limit_sec=time_limit_sec, eps0=eps0, alpha=alpha)
    # duration = time.perf_counter() - t0
    # print("sarsa : episodes={}, eps0={}, alpha={}, duration={} sec".format(episodes, eps0, alpha, duration))
    return get_greedy_policy(q_table)


# some badly learned policies might go into loop. Use max steps
def main_sample(problem, max_steps=1000, time_limit_sec=DEFAULT_TIME_LIMIT_SEC):
    t0 = time.perf_counter()
    pi = learn_policy(problem, time_limit_sec=time_limit_sec)  # limit 20 sec
    duration = time.perf_counter() - t0
    print("sarsa : duration={} sec".format(duration))
    obv = env.reset()
    state = obv[0:2]
    is_done = False
    total_reward = 0
    step = 0
    while not is_done and step < max_steps:
        step += 1
        action = int(pi[state])
        obv, reward, is_done, _ = env.step(action)
        next_state = obv[0:2]
        total_reward += reward
        state = next_state

    print("total reward = {} in {} steps".format(total_reward, step))
    return pi


if __name__ == "__main__":
    t_l = float(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TIME_LIMIT_SEC
    m_s = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
    # map_rel = 'maps_difficult/maze50x50.png'
    # map_rel = 'maps_difficult/maze50x50_22.png'
    # map_rel = 'maps/easy/easy2.bmp'
    # map_rel = 'maps/normal/normal6.bmp'
    # map_rel = 'maps/normal/normal7.bmp'
    # map_rel = 'maps/normal/normal10.bmp'
    map_rel = 'maps/normal/normal11.bmp'
    # map_rel = 'maps/normal/normal12.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), map_rel)
    # Initialize the maze environment
    env = kuimaze.HardMaze(map_image=MAP, probs=PROBS, grad=GRAD)
    print("map={}".format(map_rel))
    print("max_steps={}, time_limit_sec={}".format(m_s, t_l))
    greedy_policy = main_sample(env, max_steps=m_s, time_limit_sec=t_l)
    if VERBOSITY > 0:
        # env.visualise(get_visualisation(q_table))
        env.visualise(get_visualisation_values(greedy_policy))
        env.render()
        sleep(10)
    sys.exit(0)
