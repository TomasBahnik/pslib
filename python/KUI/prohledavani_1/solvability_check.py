import npuzzle


def is_solvable(env):
    '''
    True or False?
    '''
    env_line = []
    count = 0
    space_idx = int
    try:
        env.read_tile(3, 3)
        for i in range(4):
            for j in range(4):
                if env.read_tile(i, j) is None:
                    env_line.append(16)
                    space_idx = 4 - i
                else:
                    env_line.append(env.read_tile(i, j))
        for i in range(len(env_line)):
            for j in range(i + 1, len(env_line)):
                if env_line[i] > env_line[j]:
                    count += 1
        if count % 2 == 0:
            odd_even_inv = 0  # inversion is even
        else:
            odd_even_inv = 1  # inversion is odd

        if space_idx % 2 == 0:
            odd_even_space_idx = 0  # space idx is even
        else:
            odd_even_space_idx = 1  # space idx is odd

        if odd_even_inv == 0 and odd_even_space_idx == 1:
            return True
        if odd_even_inv == 1 and odd_even_space_idx == 0:
            return True
        else:
            return False
    except:
        for i in range(3):
            for j in range(3):
                if env.read_tile(i, j) is None:
                    env_line.append(9)
                else:
                    env_line.append(env.read_tile(i, j))
        for i in range(len(env_line)):
            for j in range(i + 1, len(env_line)):
                if env_line[i] > env_line[j]:
                    count += 1
        if count % 2 == 0:
            odd_even_inv = 0  # inversion is even
            return True
        else:
            odd_even_inv = 1  # inversion is odd
            return False


if __name__ == "__main__":
    env = npuzzle.NPuzzle(4)  # env = npuzzle.NPuzzle(4)
    env.reset()
    env.visualise()
    # just check
    print(is_solvable(env))
