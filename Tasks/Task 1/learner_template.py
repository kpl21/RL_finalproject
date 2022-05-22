import numpy as np
import pygame as pg
import matplotlib.pyplot as plt
import gridworld_template as gt
import learner_large_template as llt
import evaluator as ev
import time
import h5py

START = (0,0)   # start state
GOAL = (19,19)    # goal state
# Actions
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3
ACTIONS = [LEFT, RIGHT, UP, DOWN]
nA = len(ACTIONS)
WIDTH = 20
nS = 400      # number of states

def map_effect(s, a):
    y,x = s[0], s[1]
    y_effect,x_effect = 0,0
    map_effect_id = 0

    # wind
    if gt.matrix[y, x] == 1:

        windy = [-1, 0, 1]
        wind = np.random.choice(windy)

        if a == LEFT or a == RIGHT:
            x_effect, y_effect = wind, 0
        elif a == UP or a == DOWN:
            x_effect, y_effect = 0, wind

        map_effect_id = 1

    # lava
    elif gt.matrix[y, x] == 3:
        map_effect_id = 3

    # hole
    elif gt.matrix[y, x] == 4:
        map_effect_id = 4

    return y_effect, x_effect, map_effect_id

def transition(s, a):
    '''transition function'''
    y,x = s[0], s[1]
    y_effect, x_effect, map_effect_id = map_effect(s,a)

    #hole
    if map_effect_id == 4:
        y,x = 0,0
        next_s = (y,x)
        return next_s, map_effect_id

    # regular movement
    if a == RIGHT:
        x = min(max(x + x_effect + 1, x), WIDTH - 1)

    elif a == LEFT:
        x = max(min(x + x_effect - 1, x), 0)

    elif a == UP:
        y = max(min(y + y_effect - 1, y), 0)

    elif a == DOWN:
        y = min(max(y + y_effect + 1, y), WIDTH - 1)

    if gt.matrix[y, x] == 2:
        y,x = s[0], s[1]

    next_s = (y,x)

    return next_s, map_effect_id

def reward(s, a, map_effect_id):
    '''reward function'''
    # lava
    if map_effect_id == 3:
        return -5
    # hole
    elif map_effect_id == 4:
        return -10
    # goal
    if s == (19,18) and a == RIGHT:
        return 100
    # goal
    elif s == (18,19) and a == DOWN:
        return 100

    else:
        return -0.25

def random_agent():
    '''this is a random walker
    your smart algorithm will replace this'''
    s = START
    T = [s]
    R = [0]
    is_tp = False
    while s != GOAL:
        a = np.random.choice(ACTIONS)
        #print("action =", a)
        next_s, map_effect_id = transition(s, a)
        #print("map_effect_id =", map_effect_id)
        r = reward(s, a, map_effect_id)
        R.append(r)
        T.append(next_s)
        s = next_s
        #print("next state =",next_s)
    return T, R


def q_all_states():
    states = []

    for height in range(20):
        for width in range(20):
            states.append((height, width))
    return states

def max_q(q, state):
    max_q = -100000
    max_action = 0
    pick_option = []
    pick_action = []

    for a, q in q[state].items():

        if q >= max_q:
            max_q = q
            max_action = a
            max_val = (max_q, max_action)
            pick_option.append(max_val)

    for i in range(len(pick_option)):

        if pick_option[i][0] == max_q:
            pick_action.append(pick_option[i][1])

    action = np.random.choice(pick_action)
    return action

def q_epsilon_greedy(q, state, e, num_actions):
    p = np.random.rand()

    if p < e:
        next_action = np.random.choice(range(num_actions))

    else:
        next_action = max_q(q, state)

    return next_action

def q_learning(const,eps):
    alpha_val = [0, 1]

    if const not in alpha_val:
        return 0

    num_actions = 4

    states = q_all_states()

    start = (0, 0)
    almost_goal = [(19,18), (18,19)]
    terminal = (19, 19)

    q = {}
    for s in states:
        q[s] = {}
        for a in range(num_actions):
            q[s][a] = 0

    q_optim = {}
    total_reward = []
    timesteps = []
    final_state_history = []

    for episodes in range(eps):
        state = start
        reward_hist = []

        t = 0

        s_visited = {}
        for s in states:
            s_visited[s] = {}
            for visited in range(1):
                s_visited[s][visited] = 0

        while True:
            s_visited[state][visited] += 1
            n = s_visited[state][visited]
            #e = 1 / n ** 0.5
            e = 0.03

            if const == 0:
                alpha = 1 / n
            elif const == 1:
                alpha = 1 / n ** 0.8

            action = q_epsilon_greedy(q, state, e, num_actions)
            next_state, map_effect_id = transition(state, action)

            r = reward(state, action, map_effect_id)

            reward_hist.append(r)

            if next_state == terminal:

                q[state][action] += alpha * (r - q[state][action])
                total_reward.append(sum(reward_hist))
                timesteps.append(t)
                print(episodes, t)
                q_optim = q

                if episodes == eps - 1:
                    final_state_history.append(state)
                    if state in almost_goal:
                        final_state_history.append(next_state)

                break

            else:

                next_action = max_q(q, next_state)
                q[state][action] += alpha * (r + 1 * q[next_state][next_action] - q[state][action])

                if episodes == eps - 1:
                    final_state_history.append(state)
                state = next_state
                t += 1

    return q_optim, final_state_history, timesteps, total_reward

def random_q_learning(const,eps):
    alpha_val = [0, 1]

    if const not in alpha_val:
        return 0

    num_actions = 4

    states = q_all_states()

    almost_goal = [(19,18), (18,19)]
    terminal = (19, 19)

    q = {}
    for s in states:
        q[s] = {}
        for a in range(num_actions):
            q[s][a] = 0

    q_optim = {}
    total_reward = []
    timesteps = []
    final_state_history = []

    for episodes in range(eps):
        state = ev.small_pick_state()
        reward_hist = []

        t = 0

        s_visited = {}
        for s in states:
            s_visited[s] = {}
            for visited in range(1):
                s_visited[s][visited] = 0

        while True:
            s_visited[state][visited] += 1
            n = s_visited[state][visited]
            #e = 1 / n ** 0.5
            e = 0.03

            if const == 0:
                alpha = 1 / n
            elif const == 1:
                alpha = 1 / n ** 0.8

            action = q_epsilon_greedy(q, state, e, num_actions)
            next_state, map_effect_id = transition(state, action)

            r = reward(state, action, map_effect_id)

            reward_hist.append(r)

            if next_state == terminal:

                q[state][action] += alpha * (r - q[state][action])
                total_reward.append(sum(reward_hist))
                timesteps.append(t)
                print(episodes, t)
                q_optim = q

                if episodes == eps - 1:
                    final_state_history.append(state)
                    if state in almost_goal:
                        final_state_history.append(next_state)

                break

            else:

                next_action = max_q(q, next_state)
                q[state][action] += alpha * (r + 1 * q[next_state][next_action] - q[state][action])

                if episodes == eps - 1:
                    final_state_history.append(state)
                state = next_state
                t += 1

    return q_optim, final_state_history, timesteps, total_reward

def animate(Trajectory):
    '''
    a function that can pass information to the 
    pygame gridworld environment for visualizing 
    agent's moves
    '''
    start_y, start_x = Trajectory[0][0], Trajectory[0][1]
    pg.init()  # initialize pygame
    screen = pg.display.set_mode((gt.WIDTH + 2, gt.HEIGHT + 2))  # set up the screen
    pg.display.set_caption("Agent AI")  # add a caption
    bg = pg.Surface(screen.get_size())  # get a background surface
    bg = bg.convert()
    bg.fill(gt.bg_color)
    screen.blit(bg, (0, 0))
    clock = pg.time.Clock()
    agent = gt.Agent(start_y, start_x, screen, True)  # instantiate an agent
    agent.show(gt.agent_color)
    pg.display.flip()
    run = True
    animate_run = True
    while run:
        clock.tick(60)
        for event in pg.event.get():
            # print(agent.x, agent.y)
            if event.type == pg.QUIT:
                run = False

            elif animate_run is True:

                animate_run = False

                for state in range(len(Trajectory)+1):

                    if Trajectory[state] == (19,19):
                        break

                    if gt.matrix[Trajectory[state][0],Trajectory[state][1]] == 4:
                        agent.x = gt.WIDTH//30 + gt.WIDTH//60 - gt.CENTER - agent.w//2 + start_x * gt.cellSize
                        agent.y = gt.WIDTH//30 + gt.WIDTH//60 - gt.CENTER - agent.h//2 + start_y * gt.cellSize

                    else:

                        if Trajectory[state][0] > Trajectory[state+1][0] or Trajectory[state][0] < Trajectory[state + 1][0]:
                            displacement_y = int(Trajectory[state + 1][0]) - int(Trajectory[state][0])
                            #print(displacement_y)
                            displacement_y = displacement_y * gt.cellSize
                            agent.h_move(displacement_y)

                        elif Trajectory[state][1] > Trajectory[state + 1][1] or Trajectory[state][1] < Trajectory[state + 1][1]:
                            displacement_x = int(Trajectory[state + 1][1]) - int(Trajectory[state][1])
                            #print(displacement_x)
                            displacement_x = displacement_x * gt.cellSize
                            agent.w_move(displacement_x)

                        elif Trajectory[state][0] == Trajectory[state+1][0] and Trajectory[state][1] == Trajectory[state+1][1]:
                            agent.w_move(0)

                    screen.blit(bg, (0, 0))
                    gt.draw_grid(screen)
                    agent.show(gt.agent_color)
                    pg.display.flip()
                    pg.display.update()
                    time.sleep(0.1)
        screen.blit(bg, (0, 0))
        gt.draw_grid(screen)
        agent.show(gt.agent_color)
        pg.display.flip()
        pg.display.update()
        time.sleep(0.1)
    pg.quit()

def dq_runs(eps, runs):

    q = []
    timesteps = []
    rewards = []

    for i in range(runs):
        #result = q_learning(0, eps)
        result = random_q_learning(0, eps)
        print(i)
        qs_values = list(result[0].values())
        q_values = []

        for a in range(len(qs_values)):
            for b in range(len(qs_values[a])):
                q_values.append(qs_values[a][b])

        q.append(q_values)
        if i == runs-1:
            traj = result[1]
        timesteps.append(result[2])
        rewards.append(result[3])

    q = np.mean(np.asarray(q), axis=0)
    print(q)
    return q, traj, timesteps, rewards

def plot_timesteps(eps, timesteps1, timesteps2):
    episodes = []

    for i in range(eps):
        episodes.append(i)

    plt.plot(episodes, np.mean(np.asarray(timesteps2), axis=0), label="large-grid: gamma = 1, e = 0.03", color="red")
    plt.plot(episodes, np.mean(np.asarray(timesteps1), axis=0), label="small-grid: gamma = 1, e = 0.03", color="blue")
    plt.xlabel("Episodes")
    plt.ylabel("Timesteps")
    plt.title("Q-Learning: Timesteps per Episode Over 50 Runs")
    #plt.title("Q-Learning: Timesteps per Episode Over 10000 Random States")
    plt.legend()
    plt.show()

def plot_rewards(eps, cum_rewards1, cum_rewards2):
    episodes = []

    for i in range(eps):
        episodes.append(i)

    plt.plot(episodes, np.mean(np.asarray(cum_rewards2), axis=0), label="large-grid: gamma = 1, e = 0.03", color="red")
    plt.plot(episodes, np.mean(np.asarray(cum_rewards1), axis=0), label="small-grid: gamma = 1, e = 0.03", color="blue")
    plt.axhline(y=100, color="green", linestyle="--")
    plt.xlabel("Episodes")
    plt.ylabel("Rewards")
    plt.title("Q-Learning: Total Rewards per Episode Over 50 Runs")
    #plt.title("Q-Learning: Total Rewards per Episode Over 10000 Random States")
    plt.legend()
    plt.show()

if __name__=="__main__":

    #(0,0) initial state, 1000 eps x 50 runs
    # q2, traj2, timesteps2, rewards2 = llt.dq_runs(1000, 50)
    # q1, traj1, timesteps1, rewards1 = dq_runs(1000, 50)
    #plot_timesteps(1000, timesteps1, timesteps2)
    #plot_rewards(1000, rewards1, rewards2)
    # h5f = h5py.File('traj1-2.h5', 'w')
    # h5f.create_dataset('traj_large', data=traj2)
    # h5f.create_dataset('traj_small', data=traj1)
    # h5f.close()

    # animate
    # h5f = h5py.File('traj1-2.h5', 'r')
    # traj_large = h5f['traj_large'][:]
    # traj_small = h5f['traj_small'][:]
    # h5f.close()
    # traj_large = [tuple(x) for x in traj_large]
    # traj_small = [tuple(y) for y in traj_small]
    # animate(traj_small)
    # llt.animate(traj_large)

    #make sure to use the random_q func, 300k training for eval
    q_optim2, final_state_history2, timesteps2, total_reward2 = llt.dq_runs(300000, 1)
    q_optim1, final_state_history1, timesteps1, total_reward1 = dq_runs(300000, 1)
    h5f = h5py.File('q_star.h5', 'w')
    h5f.create_dataset('q_optim2', data=q_optim2)
    h5f.create_dataset('q_optim1', data=q_optim1)
    h5f.close()


