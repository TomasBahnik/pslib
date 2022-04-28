Implementujte funkci `learn_policy(env)` v souboru rl_agent.py který nahrajte do Brute.
env je tentokrát typu HardMaze. Očekávaným výstupem je policy, slovník klíčovaný stavy, 
hodnoty mohou být z [0,1,2,3], což odpovídá up, right, down, left (N,E,S,W).

Limit na učení na jednom postředí je 20 sekund. 
Nezapomeňte před odevzdáním vypnout vizualizace, viz VERBOSITY v rl_sandbox.py.

Opět budeme používat kostičkový svět. Stahněte si aktualizovaný balík kuimaze_rl.zip.
Vizualizační metody jsou stejné, rovněž i inicializace, ale základní filozofie práce s prostředím je odlišná.
Nemáme mapu a prostředí můžeme prozkoumávat pomocí hlavní metody `env.step(action)`. 
Prostředí-simulátor ví, jaký je aktuální stav. Hledáme co nejlepší cestu ze startu do cíle. 

Chceme cestu s co nejvyšším očekávaným součtem zlevněných odměn = *expected sum of discounted rewards*.

```text
observation, reward, done, _ = env.step(action)
state = observation[0:2]
```

Akci můžete získat třeba náhodným výběrem:

```text
action = env.action_space.sample()
```

Váš kód bude hodnoticím skriptem volán cca takto:

```python
import rl_agent

env = kuimaze.HardMaze(...)  # tady skript vytvoří prostředí
policy = rl_agent.learn_policy(env)  # limit 20 sekund

obv = env.reset()
state = obv[0:2]
is_done = False
total_reward = 0

while not is_done:
    action = int(policy[state])
    obv, reward, is_done, _ = env.step(action)
    next_state = obv[0:2]
    total_reward += reward
    state = next_state
```


SARSA control on-policy
```text
Algorithm parameters: step size alpha (0, 1], small eps > 0
Initialize Q(s, a), for all s in S+, a in A(s), arbitrarily except that Q(terminal, ·) = 0
Loop for each episode:
    Initialize S
    Choose A from S using policy derived from Q (e.g., e-greedy)
    Loop for each step of episode:
        Take action A, observe R, S'
        Choose A' from S' using policy derived from Q (e.g., e-greedy)
        Q(S, A) = Q(S, A) + alpha*[R + gamma*Q(S', A')  - Q(S, A)]
        S = S'; A=A';
    until S is terminal
```

Q-learning: off-policy TD Control
```text
Algorithm parameters: step size alpha (0, 1], small eps > 0
Initialize Q(s, a), for all s in S+, a in A(s), arbitrarily except that Q(terminal, ·) = 0
Loop for each episode:
    Initialize S
    Choose A from S using policy derived from Q (e.g., e-greedy)
    Loop for each step of episode:
        Take action A, observe R, S'
        Choose A from S using policy derived from Q (e.g., e-greedy)
        Q(S, A) = Q(S, A) + alpha*[R + gamma*max_aQ(S, a)  - Q(S, A)]
        S = S'; A=A';
    until S is terminal
```