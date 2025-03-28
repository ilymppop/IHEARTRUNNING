import pygame

pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 100
FPS = 60

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I ♥ RUNNING")

# Pause variable
paused = False

# --- FACTORY PATTERN FOR GAME OBJECTS ---
class GameObjectFactory:
    @staticmethod
    def create_object(object_type):
        if object_type == "player":
            return Player()
        elif object_type == "obstacle":
            return Obstacle()
        elif object_type == "background":
            return Background()

# --- PLAYER CLASS ---
class Player:
    def __init__(self):
        self.img = pygame.image.load('img/Pixel Racoon.jpg')
        self.img = pygame.transform.scale(self.img, (65, 70))
        self.x = 50
        self.y = HEIGHT - GROUND_HEIGHT - self.img.get_height()
        self.speed = 15
        self.jumping = False
        self.jump_height = 18
        self.gravity = 1
        self.velocity_y = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.img.get_width():
            self.x += self.speed
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height

    def apply_gravity(self):
        if self.jumping:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.y >= HEIGHT - GROUND_HEIGHT - self.img.get_height():
                self.y = HEIGHT - GROUND_HEIGHT - self.img.get_height()
                self.jumping = False

# --- OBSTACLE CLASS ---
class Obstacle:
    def __init__(self):
        self.img = pygame.image.load('img/Cestino pixel art.jpg')
        self.img = pygame.transform.scale(self.img, (60, 65))
        self.x = WIDTH
        self.y = HEIGHT - GROUND_HEIGHT - self.img.get_height()
        self.speed = 10
        self.passed = False

    def move(self):
        self.x -= self.speed
        if self.x < -self.img.get_width():
            self.x = WIDTH  # Reset position
            self.passed = False

# --- BACKGROUND CLASS ---
class Background:
    def __init__(self):
        self.img = pygame.image.load('img/загрузка (2).jpg').convert()
        self.width = self.img.get_width()
        self.scroll = 0

    def draw(self):
        screen.blit(self.img, (self.scroll, 0))
        screen.blit(self.img, (self.scroll + self.width, 0))

    def move(self):
        self.scroll -= 5
        if abs(self.scroll) >= self.width:
            self.scroll = 0

# Function to reset the game state
def reset_game():
    global player, obstacle, score, running
    player = GameObjectFactory.create_object("player")
    obstacle = GameObjectFactory.create_object("obstacle")
    score = 0
    main_game_loop()

# Main game loop function (to allow restarting)
def main_game_loop():
    global running, score, paused

    # Initialize objects
    player = GameObjectFactory.create_object("player")
    obstacle = GameObjectFactory.create_object("obstacle")
    background = GameObjectFactory.create_object("background")

    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Toggle pause
                    paused = not paused

        if not paused:
            player.move()
            player.apply_gravity()
            obstacle.move()
            background.move()

            # Increase score when player passes the obstacle
            if not obstacle.passed and player.x > obstacle.x + obstacle.img.get_width():
                score += 1
                obstacle.passed = True

            # Collision Detection
            player_rect = pygame.Rect(player.x, player.y, player.img.get_width(), player.img.get_height())
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.img.get_width(), obstacle.img.get_height())

            if player_rect.colliderect(obstacle_rect):
                running = False  # End game if collision occurs

            # Draw Everything
            background.draw()
            screen.blit(player.img, (player.x, player.y))
            screen.blit(obstacle.img, (obstacle.x, obstacle.y))

            # Display Score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, (250, 250, 250))
            screen.blit(score_text, (10, 10))

        else:
            # Display Pause Screen
            font = pygame.font.Font(None, 72)
            pause_text = font.render("Paused", True, (255, 255, 255))
            resume_text = pygame.font.Font(None, 36).render("Press P to Resume", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
            screen.blit(resume_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))

        pygame.display.flip()

    game_over_screen(score)

# Game Over Screen with Score Display
def game_over_screen(final_score):
    global running
    game_over = True

    while game_over:
        screen.fill((0, 0, 0))  # Clear the screen
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 253, 0))
        restart_text = font.render("Press R to Restart", True, (255, 0, 0))
        score_text = pygame.font.Font(None, 48).render(f"Final Score: {final_score}", True, (255, 255, 255))

        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return  # Restart the game

    pygame.quit()

# Start the game
main_game_loop()
