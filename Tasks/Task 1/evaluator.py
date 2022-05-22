import gridworld_template as gt
import gridworld_large_template as lgt
import numpy as np
import matplotlib.pyplot as plt
import learner_template as lt
import learner_large_template as llt
from sklearn.metrics import mean_squared_error as mse
import h5py

# Actions
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
ACTIONS = [LEFT, RIGHT, UP, DOWN]

def small_pick_state():
    all_states = lt.q_all_states()
    matrix = gt.matrix
    i = np.random.choice(len(all_states))
    s = all_states[i]

    #(y,x)
    map_id = matrix[s[0]][s[1]]

    if map_id == 2 or map_id == 4:
        while True:
            i = np.random.choice(len(all_states))
            s = all_states[i]
            map_id = matrix[s[0]][s[1]]
            if map_id != 2 and map_id != 4:
                break

    return s


def large_pick_state():
    all_states = llt.q_all_states()
    matrix = lgt.matrix
    i = np.random.choice(len(all_states))
    s = all_states[i]

    # (y,x)
    map_id = matrix[s[0]][s[1]]

    if map_id == 2 or map_id == 4:
        while True:
            i = np.random.choice(len(all_states))
            s = all_states[i]
            map_id = matrix[s[0]][s[1]]
            if map_id != 2 and map_id != 4:
                break

    return s

def small_eval(q_star, random_state):

    state = random_state
    terminal = (19,19)
    state_history = [state]
    reward_history = []
    states = lt.q_all_states()
    num_actions = 4

    i = 0
    q = {}
    for s in states:
        q[s] = {}
        for a in range(num_actions):
            q[s][a] = q_star[i]
            i += 1

    while state != terminal:
        action = lt.max_q(q, state)
        next_s, map_effect_id = lt.transition(state, action)
        r = lt.reward(state, action, map_effect_id)
        reward_history.append(r)
        state_history.append(next_s)
        state = next_s
        print(state)

    r_sum = sum(reward_history)
    return state_history, r_sum

def large_eval(q_star, random_state):

    state = random_state
    terminal = (24,49)
    state_history = [state]
    reward_history = []
    states = llt.q_all_states()
    num_actions = 4

    i = 0
    q = {}
    for s in states:
        q[s] = {}
        for a in range(num_actions):
            q[s][a] = q_star[i]
            i += 1

    while state != terminal:
        action = llt.max_q(q, state)
        next_s, map_effect_id = llt.transition(state, action)
        r = llt.reward(state, action, map_effect_id)
        reward_history.append(r)
        state_history.append(next_s)
        state = next_s
        print(state)

    r_sum = sum(reward_history)
    return state_history, r_sum

def random_runs_large(runs, q_star):

    picked_states = []
    rewards = []

    for i in range(runs):
        random_state = large_pick_state()

        if random_state in picked_states:
            while True:
                random_state = large_pick_state()
                if random_state not in picked_states:
                    break
        picked_states.append(random_state)
        state_history, r_sum = large_eval(q_star, random_state)
        rewards.append(r_sum)

    return rewards


def random_runs_small(runs, q_star):
    picked_states = []
    rewards = []

    for i in range(runs):
        random_state = small_pick_state()

        if random_state not in picked_states:
            while True:
                random_state = small_pick_state()
                if random_state not in picked_states:
                    break
        picked_states.append(random_state)
        state_history, r_sum = small_eval(q_star, random_state)
        rewards.append(r_sum)

    return rewards

def std_dev(reward_hist):

    max_reward = 100 * np.ones(len(reward_hist))
    x = sum(np.abs(reward_hist-max_reward)**2)
    std = (x/(len(reward_hist)-1))**0.5

    return std

def error(r1, r2):

    max_reward = 100*np.ones(len(r1))
    small_grid_error = np.abs(max_reward - r1)/100
    large_grid_error = np.abs(max_reward - r2)/100

    max_small_grid_error = np.amax(small_grid_error)
    min_small_grid_error = np.amin(small_grid_error)

    max_large_grid_error = np.amax(large_grid_error)
    min_large_grid_error = np.amin(large_grid_error)

    return min_small_grid_error, max_small_grid_error, min_large_grid_error, max_large_grid_error

def random_plot(runs, r1, r2):

    r = []

    for i in range(runs):
        r.append(i)

    plt.plot(r, r2, label="large-grid: gamma = 1, e = 0.03", color="red", marker=".", linestyle="None")
    plt.plot(r, r1, label="small-grid: gamma = 1, e = 0.03", color="blue", marker=".", linestyle="None")
    plt.axhline(y=100, color="blue", linestyle="-", lw=3, label="small grid: maximum reward")
    plt.axhline(y=100, color="red", linestyle="--", lw=3, label="large grid: maximum reward")
    plt.xlabel("Run")
    plt.ylabel("Reward")
    plt.title("Q-Learning: Total Rewards per Run Over 100 Random States")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    h5f = h5py.File('q_star.h5', 'r')
    q_large = h5f['q_optim2'][:]
    q_small = h5f['q_optim1'][:]
    h5f.close()

    r1 = random_runs_small(100, q_small)
    r2 = random_runs_large(100, q_large)
    random_plot(100, r1, r2)

    std_small = std_dev(r1)
    std_large = std_dev(r2)
    print("Small Grid Standard Deviation =", std_small)
    print("Large Grid Standard Deviation =", std_large)

    min_small_grid_error, max_small_grid_error, min_large_grid_error, max_large_grid_error = error(r1, r2)
    print("Min Small Grid Error =", min_small_grid_error)
    print("Max Small Grid Error =", max_small_grid_error)
    print("Min Large Grid Error =", min_large_grid_error)
    print("Max Large Grid Error =", max_large_grid_error)

    max_reward = 100 * np.ones(len(r1))
    small_grid_mse = mse(max_reward,r1)
    large_grid_mse = mse(max_reward, r2)
    print("Small Grid MSE =", small_grid_mse)
    print("Large Grid MSE =", large_grid_mse)