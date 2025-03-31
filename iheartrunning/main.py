import pygame
import sqlite3

pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 100
FPS = 60

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("I ♥ RUNNING")

# Database Setup
conn = sqlite3.connect("game.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)''')
conn.commit()

def save_score(name, score):
    cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

def get_top_scores():
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
    return cursor.fetchall()

def get_player_name():
    name = ""
    active = True
    font = pygame.font.Font(None, 48)
    while active:
        screen.fill((0, 0, 0))
        prompt_text = font.render("Enter your name: " + name, True, (255, 255, 255))
        screen.blit(prompt_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10:
                    name += event.unicode
    return name

def show_start_screen():
    font = pygame.font.Font(None, 72)
    running = True
    while running:
        screen.fill((0, 0, 0))
        title_text = font.render("I HEART RUNNING", True, (255, 255, 255))
        instruction_text = pygame.font.Font(None, 36).render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(title_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(instruction_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
    return False

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
            self.x = WIDTH
            self.passed = False

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

def game_over_screen(player_name, final_score):
    font = pygame.font.Font(None, 72)
    while True:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 0))
        score_text = pygame.font.Font(None, 48).render(f"{player_name}: {final_score}", True, (255, 255, 255))
        restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - 120, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main_game_loop()
                return

def main_game_loop():
    if not show_start_screen():
        return
    player_name = get_player_name()
    player = GameObjectFactory.create_object("player")
    obstacle = GameObjectFactory.create_object("obstacle")
    background = GameObjectFactory.create_object("background")
    score = 0
    clock = pygame.time.Clock()
    running = True
    paused = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
        if not paused:
            player.move()
            player.apply_gravity()
            obstacle.move()
            background.move()
            if not obstacle.passed and player.x > obstacle.x + obstacle.img.get_width():
                score += 1
                obstacle.passed = True
            if pygame.Rect(player.x, player.y, player.img.get_width(), player.img.get_height()).colliderect(
                    pygame.Rect(obstacle.x, obstacle.y, obstacle.img.get_width(), obstacle.img.get_height())):
                save_score(player_name, score)
                game_over_screen(player_name, score)
                return
            background.draw()
            screen.blit(player.img, (player.x, player.y))
            screen.blit(obstacle.img, (obstacle.x, obstacle.y))
            pygame.display.flip()

main_game_loop()
conn.close()
