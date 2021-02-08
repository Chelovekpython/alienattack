import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        """Создаем пришельца"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        # Загрузка изображения пришельца в левом верхнем углу экрана
        self.image = pygame.image.load('C:/Users/Pavel/PycharmProjects/ Alien_invasion/images/alienwww.bmp')
        self.image.set_colorkey((230, 230, 230))
        self.rect = self.image.get_rect()

        # Пришельцыв появляються в правом вершнем углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение позиции пришельца
        self.x = float(self.rect.x)

    def bl(self):
        """Выводить пршельца в текущим положении"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Перемещения пришельцов вправо-влево"""
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Вохращает True если пришелец у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
