import unittest
import pygame
from unittest.mock import patch

# Mock Pygame's image loading to prevent errors in testing
pygame.init()
pygame.display.set_mode((1, 1))

# Import game objects (assuming they are in a module named game)
from main import Player, Obstacle, Background

class TestGameObjects(unittest.TestCase):
    
    def setUp(self):
        self.player = Player()
        self.obstacle = Obstacle()
        self.background = Background()
    
    def test_player_initial_position(self):
        self.assertEqual(self.player.x, 50)
        self.assertEqual(self.player.y, 400 - 100 - self.player.img.get_height())
    
    def test_player_movement(self):
        initial_x = self.player.x
        with patch('pygame.key.get_pressed', return_value={pygame.K_RIGHT: True}):
            self.player.move()
        self.assertGreater(self.player.x, initial_x)
    
    def test_player_jump(self):
        self.player.jumping = False
        self.player.move()
        self.assertTrue(self.player.jumping or self.player.velocity_y <= 0)
    
    def test_obstacle_movement(self):
        initial_x = self.obstacle.x
        self.obstacle.move()
        self.assertLess(self.obstacle.x, initial_x)
    
    def test_obstacle_reset(self):
        self.obstacle.x = -10
        self.obstacle.move()
        self.assertEqual(self.obstacle.x, 800)
    
    def test_background_scrolling(self):
        initial_scroll = self.background.scroll
        self.background.move()
        self.assertLess(self.background.scroll, initial_scroll)
    
    def test_background_reset(self):
        self.background.scroll = -self.background.width
        self.background.move()
        self.assertEqual(self.background.scroll, 0)

if __name__ == "__main__":
    unittest.main()
