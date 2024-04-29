import birdv1
from birdv1 import *
import random

# Define Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 0.1
NUM_EPISODES = 10

# Initialize Q-table
q_table = {}

def state_to_string(state):
    return str(tuple(state))

def initialize_q_table():
    for x in range(-600 , 600 + 1):
        for v in range(-10, 32+1):
            for d in range(0, 400 + 1):
                state = (x, v, d)
                q_table[state_to_string(state)] = [0, 0]  # Q-values for flap and don't flap



def choose_action(state):
    if random.random() < EXPLORATION_RATE:
        return random.choice([0, 1])  # Explore: choose randomly between flap (1) and don't flap (0)
    else:
        return q_table[state_to_string(state)].index(max(q_table[state_to_string(state)]))  # Exploit: choose action with highest Q-value

def update_q_table(state, action, reward, next_state):
    q_value = q_table[state_to_string(state)][action]
    max_next_q_value = max(q_table[state_to_string(next_state)])
    new_q_value = q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q_value - q_value)
    q_table[state_to_string(state)][action] = new_q_value

def run(bird):
    birdv1
    
def policy_network(bird):
    initialize_q_table()
    action = choose_action(birdv1.get_state())
    print(action)
    for episode in range(NUM_EPISODES):
        state = birdv1.get_state()
        total_reward = 0
        done = False
        while not done:
            action = choose_action(state)
            print(action)
            if action == 1:
                bird.flap()
            bird.update()
            next_state = birdv1.get_state()
            reward = 1 if bird.collided else 0
            total_reward += reward
            update_q_table(state, action, reward, next_state)
            # print(q_table)
            state = next_state
            done = bird.collided
            print(done)
        print(f"Episode {episode + 1}: Total Reward = {total_reward}")


# Main function
if __name__ == '__main__':

    run()



