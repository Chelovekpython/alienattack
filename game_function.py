import sys
import pygame
from Bullet import Bullet
from Alien import Alien
from time import sleep


def get_number_aliens_x(ai_setting, alien_width, ):
    """Вычисляет количестов пришельцев в ряду"""
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_setting, ship_height, alien_height):
    """Определяет количество рядов на экране"""
    avaible_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaible_space_y / (2 * alien_height) + 1)
    return number_rows


def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещяет его в ряду"""
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_setting, screen, ship, aliens):
    """Создает флот пришельцев"""
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    """бработка нажатий на клаву-мышь"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, stats, ai_setting, screen, ship, bullets)
        if event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки начать"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            ai_setting.initialize_dynamic_setting
            pygame.mouse.set_visible(False)  # Скрывает мышку если игра активна
            stats.reset_stats()
            stats.game_active = True
            # сброс игровой статистики
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            # Очитска списка пришельцев и пуль
            aliens.empty()
            bullets.empty()

            # Создание нового флота и размещение корабля в центре
            create_fleet(ai_setting, screen, ship, aliens)
            ship.center_ship()
            sb.prep_ships()


def check_keydown_events(event, stats, ai_setting, screen, ship, bullets):
    """обработка зажатия кнопки"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:  # при нажатие пробела стрельба
        fire_bullet(ai_setting, screen, ship, bullets)
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_p:
        stats.game_active = True
        pygame.mouse.set_visible(False)


def check_keyup_events(event, ship):
    """обработка нажатие кнопки"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран"""

    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    sb.show_score()

    # Кнопка "Начать" отображается в том случае, если игра неактивна
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """Обновляет текущию позицию пули и уничтожает старые"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 and bullet.rect2.bottom <= 0 and bullet.rect3.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_setting, screen, stats, sb, ship, aliens, bullets):
    # проверака попаданий пуль пришельцев
    # при попадание уничтожает пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, ship, aliens)


def fire_bullet(ai_setting, screen, ship, bullets):
    """Запускает снаряд если лимит выстрелов не превышен"""
    if len(bullets) < ai_setting.bullet_allowed:
        new_bullets = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullets)


def check_fleet_edges(ai_setting, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    """Опускает весь флот и меняет напрвление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """Проверяет достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Корабль подбит")
        ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
    # проверка пришельцев у нижний границы
    check_alien_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """Обрабатывает столкновения корабля с пришельцем"""
    # Уменьшение ship_left
    if stats.ship_left > 0:
        stats.ship_left -= 1
        stats.ships_left -= 1
        # Оновление игровой информации
        sb.prep_ships()
        # Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещения корабля в центре уничтожении корабля
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()

        # Пауза перед рестартом
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, добраись ли пришельцы до нижний границы экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд"""
    records = open('C:/Users/Pavel/PycharmProjects/ Alien_invasion/records.txt', 'r+')
    if stats.score > int(records.read()):
        records = open('C:/Users/Pavel/PycharmProjects/ Alien_invasion/records.txt', 'w')
        records.write(str(stats.score))
        sb.prep_high_score()
        sb.prep_score()
        sb.show_score()