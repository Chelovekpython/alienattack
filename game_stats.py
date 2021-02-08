class GameStats():
    """Отслеживания статистики игры"""

    def __init__(self, ai_setting):
        """Инициализируем статистику"""
        self.ai_setting = ai_setting
        self.reset_stats()
        self.ai_setting = ai_setting
        self.reset_stats()
        self.high_score = 0

        # Игра запускается в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        """Инициализирууем статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
        self.ships_left = self.ai_setting.ship_limit

