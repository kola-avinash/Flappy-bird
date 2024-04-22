import pygame
import random

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

# Function to display score
def display_score():
    score_surface = SCORE_FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

# Function to check if restart button is clicked
def is_restart_clicked(mouse_pos):
    restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    return restart_rect.collidepoint(mouse_pos)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    restart = False  # Initialize restart flag
    
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                restart = True  # Exit restart loop if user quits
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_restart_clicked(mouse_pos):
                    # Reset variables
                    bird = Bird()
                    pipes = []
                    score = 0
                    restart = True  # Exit restart loop if restart button clicked
                    # Reset bird position
                    bird.y = SCREEN_HEIGHT // 2
                    
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

    # Game over message
    game_over_font = pygame.font.Font(None, 48)
    game_over_surface = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Restart feature
    restart_font = pygame.font.Font(None, 36)
    restart_surface = restart_font.render("Restart", True, (0, 0, 0))
    restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    # Draw game over message and restart button
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.update()

    # Restart loop
    while restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_restart_clicked(mouse_pos):
                    # Reset variables
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
