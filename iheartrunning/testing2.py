import unittest
import pygame
from main import Player, Obstacle, Background, WIDTH, HEIGHT, GROUND_HEIGHT

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player()
        self.obstacle = Obstacle()
        self.background = Background()

    def test_player_initial_position(self):
        self.assertEqual(self.player.x, 50)
        self.assertEqual(self.player.y, HEIGHT - GROUND_HEIGHT - self.player.img.get_height())

    def test_player_movement(self):
        self.player.x = 100
        self.player.speed = 10
        self.player.move()
        self.assertIn(self.player.x, range(90, 111))  # Проверяем движение

    def test_player_jump(self):
        self.player.jumping = False
        self.player.velocity_y = 0
        self.player.jump_height = 18
        self.player.move()
        self.assertFalse(self.player.jumping)  # Перед прыжком
        
        # Эмулируем нажатие пробела
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
        self.player.move()
        self.assertTrue(self.player.jumping)  # После прыжка

    def test_obstacle_movement(self):
        initial_x = self.obstacle.x
        self.obstacle.move()
        self.assertLess(self.obstacle.x, initial_x)  # Объект движется влево

    def test_background_movement(self):
        initial_scroll = self.background.scroll
        self.background.move()
        self.assertLess(self.background.scroll, initial_scroll)  # Фон прокручивается

if __name__ == "__main__":
    unittest.main()
