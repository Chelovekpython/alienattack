import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('C:/Users/Pavel/PycharmProjects/ Alien_invasion/images/ship.bmp')
        self.image.set_colorkey((230, 230, 230))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx

        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
      #  super(Ship, self).__init__()

    def update(self):
        """Обновляет позицию корабля с учетом флагов"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if self.moving_right:
                self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            if self.moving_left:
                self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top < 1200:
            self.bottom -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < 800:
            self.bottom += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        self.screen.blit(self.image, self.rect)  # а blit ли проблема с фоном

    def center_ship(self):
        """Размещает корабль в центре снизу"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
