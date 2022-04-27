import gym
import numpy as np


def run_episode(env, policy=None, render=True):
    """ Follow policy through an environment's episode and return an array of collected rewards """
    assert type(env.action_space) == gym.spaces.Discrete
    assert type(env.observation_space) == gym.spaces.tuple.Tuple

    # env.reset() returns observation
    # observation, reward, done, _ = env.step(action)
    # state = observation[0:2]
    state = env.reset()
    if render:
        env.render()

    done = False
    rewards = []
    while not done:
        state_ridx = state[0:2]
        action = np.argmax(policy[state_ridx])
        state, reward, done, info = env.step(action)
        rewards += [reward]

        if render:
            env.render()

    if render:
        import matplotlib.pyplot as plt
        plt.show()

    return rewards


def sarsa(env, num_episodes, eps0=0.5, alpha=0.5):
    """ On-policy Sarsa algorithm per Chapter 6.4 (with exploration rate decay) """
    assert type(env.action_space) == gym.spaces.Discrete
    assert type(env.observation_space) == gym.spaces.tuple.Tuple

    # Env size
    x_dims = env.observation_space.spaces[0].n
    y_dims = env.observation_space.spaces[1].n
    maze_size = tuple((x_dims, y_dims))

    # Number of discrete actions
    n_action = env.action_space.n
    size_x = maze_size[0]
    size_y = maze_size[1]
    # Initialize action-value function - Q-table
    q = np.zeros([size_x, size_y, n_action], dtype=np.float)

    # check the sum of probabilities
    ones = np.ones([size_x, size_y], dtype=np.float)
    # Initialize policy to equal-probable random
    policy = np.ones([size_x, size_y, n_action], dtype=np.float) / n_action

    # Dictionary for states from tuples to int
    states_indexes = states_dict(env)

    history = [0] * num_episodes
    for episode in range(num_episodes):
        # Reset the environment
        state = env.reset()
        state_ridx = state[0:2]
        idx_x = state_ridx[0]
        idx_y = state_ridx[1]
        action = np.random.choice(n_action, p=policy[idx_x, idx_y])

        done = False
        while not done:
            idx_x = state_ridx[0]
            idx_y = state_ridx[1]
            # Step the environment forward and check for termination
            next_state, reward, done, info = env.step(action)
            next_state_ridx = next_state[0:2]
            # return self.np_random.randint(self.n)
            # next_action = env.action_space.sample()
            next_state_idx_x = next_state_ridx[0]
            next_state_idx_y = next_state_ridx[1]
            next_action = np.random.choice(n_action, p=policy[next_state_idx_x, next_state_idx_y])

            # Update q values
            q[idx_x, idx_y, action] += alpha * (reward + q[next_state_idx_x, next_state_idx_y, next_action]
                                                - q[idx_x, idx_y, action])

            # Extract eps-greedy policy from the updated q values
            eps = eps0 / (episode + 1)
            policy[idx_x, idx_y, :] = eps / n_action
            policy[idx_x, idx_y, np.argmax(q[state_ridx])] = 1 - eps + eps / n_action
            assert np.allclose(np.sum(policy, axis=2), ones)

            # Prepare the next q update
            state_ridx = next_state_ridx
            action = next_action
            history[episode] += 1

    return q, policy, history


def states_dict(env):
    states = dict()
    state_idx = 0
    for state in env.get_all_states():
        key = (state.x, state.y)
        states[key] = state_idx
        state_idx += 1
    return states
