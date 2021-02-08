import pygame


class Setting():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 0.5
        self.ship_limit = 3
        background = pygame.image.load('C:/Users/Pavel/PycharmProjects/ Alien_invasion/images/background.bmp')
        background_rect = background.get_rect()
        # Параметры пули
        self.bullet_speed_factor = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 40
        # Настройка пришельцев
        self.alien_speed_factor = 0.15
        self.fleet_drop_speed = 10
        # fleet_direction 1 оозночает движение вправо - 1 влево
        self.fleet_direction = 1
        # Темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_setting()
        # темп увеличения стоймости пришелцев
        self.score_scale = 1.1
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """Инициализирует настройки, изменяющиеся в процессе игры"""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 0.5
        self.alien_speed_factor = 0.15

        # fleet_direction = 1 обохначет движение вправо, а -1 влево
        self.fleet_direction = 1

        # Посчет очков
        self.alien_points = 50

    def increase_speed(self):
        """величивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
