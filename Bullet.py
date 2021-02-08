import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        """Создает пули в текущий позиции корабля"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Создание пули и сохранение её позиции
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height) # далее идут 3 пули
        self.rect2 = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect3 = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.rect2.centerx = ship.rect.centerx   # привязка пуль к кораблю
        self.rect2.top = ship.rect.top

        self.rect3.centerx = ship.rect.centerx
        self.rect3.top = ship.rect.top


        # Позиция пули хранитеться в вещественном формате
        self.y = float(self.rect.y)
        self.x = float(self.rect2.x)

        self.x2 = float(self.rect3.x)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Процесс стрельбы"""
        self.y -= self.speed_factor  # перемещение пули в пространстве по координате y
        self.rect.y = self.y

        self.x -= self.speed_factor # выстрел влево
        self.rect2.x = self.x
        self.rect2.y = self.y



        self.rect3.x = self.x    # выстрел вправо
        self.x2 += self.speed_factor
        self.rect3.y = self.y  # Сделано для второй пули впаво и влево
        self.rect3.x = self.x2




    def draw_bullet(self):
        """Вывооди пули на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        #pygame.draw.rect(self.screen, self.color, self.rect2)
        #pygame.draw.rect(self.screen, self.color, self.rect3)