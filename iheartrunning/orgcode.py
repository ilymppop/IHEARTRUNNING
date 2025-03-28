import pygame
import math

pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 100
FPS = 60

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I ♥ RUNNING")

# Load Images
bg = pygame.image.load('img/загрузка (2).jpg').convert()
bg_width = bg. get_width()
gaymer_img = pygame.image.load('img/Pixel Racoon.jpg')
obstacle_img = pygame.image.load('img/Cestino pixel art.jpg')

# define game variabiles 
scroll = 0
tiles = math.ceil(WIDTH / bg_width) + 1


# Resize Images
gaymer_img = pygame.transform.scale(gaymer_img, (65, 70))
obstacle_img = pygame.transform.scale(obstacle_img, (60, 65))

# Player Settings
gaymer_x = 50
gaymer_y = HEIGHT - GROUND_HEIGHT - gaymer_img.get_height()
gaymer_speed = 15
gaymer_jump = False
jump_height = 18
gravity = 1
velocity_y = 0

# Obstacle Settings
obstacle_x = WIDTH
obstacle_y = HEIGHT - GROUND_HEIGHT - obstacle_img.get_height()
obstacle_speed = 10

# Score
score = 0

# Clock
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    clock.tick(FPS)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gaymer_x -= gaymer_speed
    if keys[pygame.K_RIGHT]:
        gaymer_x += gaymer_speed
    if keys[pygame.K_SPACE] and not gaymer_jump:
        gaymer_jump = True
        velocity_y = -jump_height

    # Apply Gravity
    if gaymer_jump:
        gaymer_y += velocity_y
        velocity_y += gravity
        if gaymer_y >= HEIGHT - GROUND_HEIGHT - gaymer_img.get_height():
            gaymer_y = HEIGHT - GROUND_HEIGHT - gaymer_img.get_height()
            gaymer_jump = False

    # Move Obstacle
    obstacle_x -= obstacle_speed
    if obstacle_x < -obstacle_img.get_width():
        obstacle_x = WIDTH  # Reset obstacle position
        score += 1  # Increase score

    # Collision Detection
    gaymer_rect = pygame.Rect(gaymer_x, gaymer_y, gaymer_img.get_width(), gaymer_img.get_height())
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_img.get_width(), obstacle_img.get_height())

    if gaymer_rect.colliderect(obstacle_rect):
        running = False  # End game if collision occurs

    # Draw Everything
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    screen.blit(gaymer_img, (gaymer_x, gaymer_y))
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Scroll
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # Display Score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (250, 250, 250))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# Game Over Screen
game_over = True
while game_over:
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 253, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

pygame.quit()
