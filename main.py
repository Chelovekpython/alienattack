import sys
import pygame
from Settings import Setting
from Ship import Ship
import game_function as gf
from pygame.sprite import Group
from Alien import Alien
from game_stats import GameStats
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard


def run_game(): # Основной цикл игры
    pygame.init()
    ai_settings = Setting()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Вторжение пришельцев")
    play_button = Button(ai_settings, screen, "Начать")
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien = Alien(ai_settings, screen)
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    background = pygame.image.load('C:/Users/Pavel/PycharmProjects/ Alien_invasion/images/background.bmp')
    background_rect = background.get_rect()
    stats = GameStats(ai_settings)

    # Создание экземпляров GameStats и Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        #  gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)


run_game()

303
