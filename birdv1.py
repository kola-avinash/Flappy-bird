import sys
import pygame
import random
# from policy import get_state

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

def get_state():
    bird_state = [bird.y, bird.velocity]  # Example: Bird's position and velocity
    pipe_state = []  # Example: Distance to the nearest pipe
    for pipe in pipes:
        if pipe.x > bird.x:
            pipe_state.append(pipe.x - bird.x)
    if not pipe_state:
        pipe_state.append(SCREEN_WIDTH)  # If no pipes ahead, consider a distant pipe
    return bird_state + pipe_state

# Function to display score
def display_score():
    score_surface = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    restart = False  # Initialize restart flag
    states = []
    actions = []
    rewards = []
    while not restart:
        state = get_state()
        print(state)
        states.append(state)
        # action = policy_network(state)  # Sample action from policy network
        # reward = 1 if bird is alive else -1  # Define reward
        for event in pygame.event.get():
            state = get_state()
            states.append(state)
            if event.type == pygame.QUIT:
                running = True
                restart = False # Exit restart loop if user quits
                print(states)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Main game logic here...

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

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

        # Check for collisions
        for pipe in pipes:
            if (bird.x < pipe.x + PIPE_WIDTH and bird.x + BIRD_WIDTH > pipe.x and
                (bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + GAP)):
                running = False
                restart = True

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        display_score()
        pygame.display.update()

        # Cap the frame rate
        clock.tick(30)
    
    print(states)

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
        clock.tick(30)
        
# Quit Pygame
pygame.quit()
