import sys
import pygame
import random
import json


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
BIRD_COLOR = (255, 0, 0)
PIPE_COLOR = (0, 255, 0)
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
PIPE_WIDTH = 50
GAP = 200
PIPE_VELOCITY = 5
GRAVITY = 0.5
FLAP_STRENGTH = 10
SCORE_FONT = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.passed = False

    def flap(self):
        self.velocity = -FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.rect(screen, BIRD_COLOR, (self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT))

# Define Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(50, SCREEN_HEIGHT - GAP - 50)
        self.passed = False

    def move(self):
        self.x -= PIPE_VELOCITY

    def draw(self):
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.height + GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - GAP))

# Create objects
bird = Bird()
pipes = []
score = 0
collision = False


# Define Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 0.2

# Initialize Q-table
q_table = {}

def state_to_string(state):
    return str(tuple(state))

def initialize_q_table():
    for x in range(0, 600 + 1):
        for v in range(-10, 32 + 1):
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

    

def policy_network(bird):
    state = get_state()
    action = choose_action(get_state())
    if action == 1:
        bird.flap()
    bird.update()
    next_state = get_state()
    reward = 1 if bird.passed else 0
    update_q_table(state, action, reward, next_state)
    state = next_state
    # print(f"Total Reward = {total_reward}")

    
    


def collided():
    return collision

def get_state():
    if bird.y>600:
        bird.y = 600
    elif bird.y<0:
        bird.y = 0
    
    if bird.velocity > 32:
        bird.velocity = 32
    
    bird_state = [int(bird.y), int(bird.velocity)] # Bird's position and velocity
    closest_pipe_distance = SCREEN_WIDTH  # Initialize with a distant pipe
    for pipe in pipes:
        if pipe.x > bird.x:
            closest_pipe_distance = int(min(closest_pipe_distance, pipe.x - bird.x)//2)
            break  
    return bird_state + [closest_pipe_distance]  

# Function to display score
def display_score():
    score_surface = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))
    return score

# Main game loop
running = True
clock = pygame.time.Clock()
episode = 0
initialize_q_table()

while running:
    episode += 1
    restart = False  # Initialize restart flag
    states = []
    total_reward = 0
    print(f"Episode --> {episode}")
    
    
    while not restart:
        state = get_state()
        # print(state)
        states.append(state)
        action = policy_network(bird)  # Sample action from policy network
        for event in pygame.event.get():
            state = get_state()
            states.append(state)
            if event.type == pygame.QUIT:
                running = True
                restart = False # Exit restart loop if user quits
                # with open("qtable.txt", "w") as fp:
                #     json.dump(q_table, fp) 
                # # print(states)
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
        



        # Update bird
        bird.update()

        # Generate pipes
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        # Update pipes and check for score
        for pipe in pipes:
            pipe.move()
            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                pipe.passed = True
                score += 1
                bird.passed = True
                # print(score)
                

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

        # Check for collisions
        for pipe in pipes:
            if (bird.x < pipe.x + PIPE_WIDTH and bird.x + BIRD_WIDTH > pipe.x and
                (bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + GAP)):
                running = False
                restart = True
                bird.collided = True

    

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        display_score()
        pygame.display.update()

        # Cap the frame rate
        clock.tick(0)

    print(f"Score --> {display_score()}")
    # print(states)

    while restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = False
                pygame.quit()
        bird = Bird()
        pipes = []
        score = 0
        running = True
        restart = False
        # Reset bird position
        bird.y = SCREEN_HEIGHT // 2
        clock.tick(0)
        
# Quit Pygame
pygame.quit()
