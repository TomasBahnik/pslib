#!/usr/bin/env python3
import copy
import os
import random

import sys
import time

import kuimaze

GRAD = (0, 0)
SKIP = False
SAVE_EPS = False
VERBOSITY = 0

GRID_WORLD4 = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0]],
               [[255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 255, 255]],
               [[0, 0, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
               [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]

GRID_WORLD3 = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0]],
               [[255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 0, 0]],
               [[0, 0, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]

PROBS = [0.8, 0.1, 0.1, 0]
R0 = -0.04
# R(s) < –1.6284
R1 = -1.8
# – 0.4278 < R(s) < – 0.0850
R2 = -0.3
# – 0.0221 < R(s) < 0
R3 = -0.015
REWARD_NORMAL_STATE = R0
REWARD_GOAL_STATE = 1
REWARD_DANGEROUS_STATE = -1

GRID_WORLD3_REWARDS = [[REWARD_NORMAL_STATE, REWARD_NORMAL_STATE, REWARD_NORMAL_STATE, REWARD_GOAL_STATE],
                       [REWARD_NORMAL_STATE, 0, REWARD_NORMAL_STATE, REWARD_DANGEROUS_STATE],
                       [REWARD_NORMAL_STATE, REWARD_NORMAL_STATE, REWARD_NORMAL_STATE, REWARD_NORMAL_STATE]]

DEFAULT_DISCOUNT_FACTOR = 0.9999
DEFAULT_EPSILON = 0.03


def wait_n_or_s():
    def wait_key():
        '''
        returns key pressed ... works only in terminal! NOT in IDE!
        '''
        result = None
        if os.name == 'nt':
            import msvcrt
            result = msvcrt.getch()
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


def get_visualisation_values(dictvalues):
    if dictvalues is None:
        return None
    ret = []
    for key, value in dictvalues.items():
        # ret.append({'x': key[0], 'y': key[1], 'value': [value, value, value, value]})
        ret.append({'x': key[0], 'y': key[1], 'value': value})
    return ret


def init_policy(problem):
    policy = dict()
    for state in problem.get_all_states():
        key = (state.x, state.y)
        if problem.is_goal_state(state):
            policy[key] = None
            continue
        actions = [action for action in problem.get_actions(state)]
        policy[key] = random.choice(actions)
    return policy


def init_utils(problem):
    """
    Initialize all state utilities to zero except the goal states
    :param problem: problem - object, for us it will be kuimaze.Maze object
    :return: dictionary of utilities, indexed by state coordinates
    """
    utils = dict()
    x_dims = problem.observation_space.spaces[0].n
    y_dims = problem.observation_space.spaces[1].n

    for x in range(x_dims):
        for y in range(y_dims):
            utils[(x, y)] = 0

    for state in problem.get_all_states():
        utils[(state.x, state.y)] = state.reward  # problem.get_state_reward(state)
    return utils


def actions_except_terminal_states(problem, s):
    return [None] if problem.is_terminal_state(s) else problem.get_actions(s)


def expected_utility(a, s, U, problem):
    """The expected utility of doing a in state s, according to the problem and utilities."""
    return sum(prob_s_a * U[(s_prime.x, s_prime.y)] for (s_prime, prob_s_a) in problem.get_next_states_and_probs(s, a))


def q_value(problem, state, a, U, discount_factor):
    if not a:
        return state.reward
    res = 0
    # get_next_states_and_probs returns state not kuimaze.maze.weighted_state
    for s_prime, p in problem.get_next_states_and_probs(state, a):
        key = (s_prime.x, s_prime.y)
        res += p * (state.reward + discount_factor * U[key])
    return res


def value_iteration(problem, discount_factor=DEFAULT_DISCOUNT_FACTOR, epsilon=DEFAULT_EPSILON):
    """Solving an MDP by value iteration"""

    U1 = init_utils(problem)
    # U1 = {(s.x, s.y): 0 for s in problem.get_all_states()}
    while True:
        U = copy.deepcopy(U1)
        delta = 0
        for s in problem.get_all_states():
            key = (s.x, s.y)
            # get_actions(s) does not take care of terminal states
            actions = actions_except_terminal_states(problem, s)
            U1[key] = max(q_value(problem, s, a, U, discount_factor) for a in actions)
            delta = max(delta, abs(U1[key] - U[key]))
        accuracy = epsilon * (1 - discount_factor) / discount_factor
        if delta <= accuracy:
            return U


def find_policy_via_value_iteration(problem, discount_factor=DEFAULT_DISCOUNT_FACTOR, epsilon=DEFAULT_EPSILON):
    """Given an MDP and a utility function U, determine the best policy,
    as a mapping from state to action."""
    U = value_iteration(problem, discount_factor, epsilon)
    pi = init_policy(problem)
    for s in problem.get_all_states():
        key = (s.x, s.y)
        if problem.is_terminal_state(s):
            pi[key] = None
        else:
            pi[key] = max(problem.get_actions(s), key=lambda a: q_value(problem, s, a, U, discount_factor))
    return pi


def policy_evaluation(pi, U, problem, discount_factor, k=10):
    """Return an updated utility mapping U from each state in the MDP to its
    utility, using an approximation (modified policy iteration)."""

    for i in range(k):
        for ws in problem.get_all_states():  # returns weighted state with reward
            s = (ws.x, ws.y)
            r_s = ws.reward
            if problem.is_terminal_state(ws):
                U[s] = r_s
            else:
                U[s] = r_s + discount_factor * expected_utility(pi[s], ws, U, problem)
    return U


def find_policy_via_policy_iteration(problem, discount_factor=DEFAULT_DISCOUNT_FACTOR):
    U = init_utils(problem)
    pi = init_policy(problem)
    while True:
        U = policy_evaluation(pi, U, problem, discount_factor)
        unchanged = True
        for s in problem.get_all_states():
            key = (s.x, s.y)
            # use problem.get_actions(s) ?
            a_star = max(actions_except_terminal_states(problem, s),
                         key=lambda a: q_value(problem, s, a, U, discount_factor))
            # use max over actions of expected_utility ?
            if q_value(problem, s, a_star, U, discount_factor) > q_value(problem, s, pi[key], U, discount_factor):
                pi[key] = a_star
                unchanged = False
        if unchanged:
            return pi


def compare_policies(problem, p1, p2):
    if len(p1) != len(p2):
        return False
    x_dims = problem.observation_space.spaces[0].n
    y_dims = problem.observation_space.spaces[1].n
    d = x_dims * y_dims - len(p1)
    print("Dims of problem={}, length of policies={}. diff={}".format((x_dims, y_dims), len(p1), d))
    diff_count = 0
    for p_k in policy_p_i.keys():
        if p1[p_k] != p2[p_k]:
            diff_count += 1
            print("key {} : p1={}, p2={}".format(p_k, p1[p_k], p2[p_k]))
    if diff_count > 0:
        print("diff count {}".format(diff_count))
        return False
    return True


if __name__ == "__main__":
    # map_rel = 'maps_difficult/maze50x50.png'
    # map_rel = 'maps_difficult/maze50x50_22.png'
    # map_rel = 'maps/easy/easy1.bmp'
    # map_rel = 'maps/normal/normal12.bmp'
    map_rel = 'maps/normal/normal11.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), map_rel)
    # Initialize the maze environment
    # env = kuimaze.MDPMaze(map_image=GRID_WORLD3, probs=PROBS, grad=GRAD, node_rewards=GRID_WORLD3_REWARDS)
    # env = kuimaze.MDPMaze(map_image=GRID_WORLD3, probs=PROBS, grad=GRAD, node_rewards=None)
    env = kuimaze.MDPMaze(map_image=MAP, probs=PROBS, grad=GRAD, node_rewards=None)
    env.reset()
    gamma = DEFAULT_DISCOUNT_FACTOR
    eps = 0.001

    print("MAP {}".format(map_rel))
    t0 = time.perf_counter()
    policy_p_i = find_policy_via_policy_iteration(env, discount_factor=gamma)
    delta = time.perf_counter() - t0
    print("policy_iteration : g={}, e={}, {} sec".format(gamma, eps, delta))

    t0 = time.perf_counter()
    policy_v_i = find_policy_via_value_iteration(env, discount_factor=gamma, epsilon=eps)
    delta = time.perf_counter() - t0
    print("value_iteration : g={}, e={}, {} sec".format(gamma, eps, delta))

    p_equals = compare_policies(env, policy_p_i, policy_v_i)
    print("policies equals : {}".format(p_equals))

    env.visualise(get_visualisation_values(policy_p_i))
    env.render()
    # wait_n_or_s()
    time.sleep(10)
    sys.exit(0)
