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


MAX_T = 1000  # max trials (for one episode)


def sarsa(env, num_episodes, eps0=0.5, alpha=0.5):
    """ On-policy Sarsa algorithm per Chapter 6.4 (with exploration rate decay) """
    assert type(env.action_space) == gym.spaces.Discrete
    assert type(env.observation_space) == gym.spaces.tuple.Tuple

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

    history = [0] * num_episodes
    for episode in range(num_episodes):
        # Reset the environment
        state = env.reset()
        state_idx = state[0:2]
        #  TODO replace by action = env.action_space.sample()
        action = np.random.choice(n_action, p=policy[state_idx[0], state_idx[1]])

        done = False
        while not done and history[episode] < MAX_T:
            idx_x = state_idx[0]
            idx_y = state_idx[1]
            # Step the environment forward and check for termination
            next_state, reward, done, _ = env.step(action)
            next_state_idx = next_state[0:2]
            next_state_idx_x = next_state_idx[0]
            next_state_idx_y = next_state_idx[1]
            #  TODO replace by action = env.action_space.sample()
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
            history[episode] += 1

    return q, policy, history
