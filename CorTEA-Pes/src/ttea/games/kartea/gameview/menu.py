import sys

import pygame

from ttea.games.kartea.gamemodel import Background, Image
from ttea.games.kartea.gameui import UI
from ttea.games.kartea.gameutil import GameSettings
from ttea.games.kartea.util import KarteaPathConfig

# import settings
# from settings import *
# from background import Background


class Menu:
    """Classe responsável por gerenciar todos os menus e telas de feedback do jogo."""

    def __init__(self, surface):
        self.surface = surface

        # Background do menu
        self.background = Background()
        self.background.background_menu()

        # Som de clique (usado em todos os botões)

        # self.click_sound = pygame.mixer.Sound("Assets/Kartea/Sounds/point.wav")
        self.click_sound = pygame.mixer.Sound(
            # KarteaPathConfig.game_sound("point.wav")
            GameSettings.MENU_CLICK_SOUND
        )

    def draw(self):
        """Desenha o fundo básico do menu."""
        self.background.draw(self.surface)
        fundo = Image.load(
            # KarteaPathConfig.kartea_image(":bottom"),
            # KarteaPathConfig.game_image("fundo.png"),
            # "Assets/Kartea/Fundo.png",
            GameSettings.MENU_BACKGROUND,
            size=(GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT),
        )
        Image.draw(self.surface, fundo, (0, 0))

    def draw_feedback(self):
        """Desenha a tela de feedback com estatísticas do nível."""
        UI.draw_text(
            self.surface,
            "Feedback",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 100),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        UI.draw_text(
            self.surface,
            "Quantidade",
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 100),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        # Pontuação
        UI.draw_text(
            self.surface,
            "Pontuação",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 130),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.score),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 130),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        # Movimentos
        UI.draw_text(
            self.surface,
            "Movimentos",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 160),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.movimento),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 160),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        # Alvos
        UI.draw_text(
            self.surface,
            "Alvos Gerados",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 190),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Alvo),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 190),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        UI.draw_text(
            self.surface,
            "Alvos Colididos",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 220),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Alvo_c),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 220),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        UI.draw_text(
            self.surface,
            "Alvos Desviados",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 250),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Alvo_d),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 250),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        # Obstáculos
        UI.draw_text(
            self.surface,
            "Obst. Gerados",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 280),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Obst),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 280),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        UI.draw_text(
            self.surface,
            "Obst. Desviados",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 310),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Obst_d),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 310),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

        UI.draw_text(
            self.surface,
            "Obst. Colididos",
            ((GameSettings.SCREEN_WIDTH // 2) + 50, 340),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )
        UI.draw_text(
            self.surface,
            str(GameSettings.Obst_c),
            ((GameSettings.SCREEN_WIDTH // 2) + 250, 340),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["medium"],
            shadow=True,
            shadow_color=(255, 255, 255),
        )

    def _handle_inicial_menu(self):
        """Gerencia o menu inicial (tela principal)."""
        UI.draw_text(
            self.surface,
            GameSettings.GAME_TITLE,
            (GameSettings.SCREEN_WIDTH // 2, 120),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["big"],
            shadow=True,
            shadow_color=(255, 255, 255),
            pos_mode="center",
        )

        if UI.button(
            self.surface, 0, 300, "Jogar", click_sound=self.click_sound
        ):
            return "game"

        if UI.button(
            self.surface,
            0,
            300 + GameSettings.BUTTONS_SIZES[1] * 4,
            "Sair",
            click_sound=self.click_sound,
        ):
            pygame.display.quit()
            sys.exit()

        return None

    def _handle_pause_menu(self):
        """Gerencia o menu de pausa."""
        UI.draw_text(
            self.surface,
            "Pause",
            (GameSettings.SCREEN_WIDTH // 2, 120),
            GameSettings.COLORS["title"],
            font=GameSettings.FONTS["big"],
            shadow=True,
            shadow_color=(255, 255, 255),
            pos_mode="center",
        )

        if UI.button(
            self.surface, 0, 300, "Continuar", click_sound=self.click_sound
        ):
            return "game"

        if UI.button(
            self.surface,
            1,
            300 + GameSettings.BUTTONS_SIZES[1] * 2,
            "Retroceder",
            click_sound=self.click_sound,
        ):
            return "prev"

        if UI.button(
            self.surface,
            0,
            300 + GameSettings.BUTTONS_SIZES[1] * 2,
            "Reiniciar",
            click_sound=self.click_sound,
        ):
            return "rest"

        if UI.button(
            self.surface,
            2,
            300 + GameSettings.BUTTONS_SIZES[1] * 2,
            "Avançar",
            click_sound=self.click_sound,
        ):
            return "next"

        if UI.button(
            self.surface,
            0,
            300 + GameSettings.BUTTONS_SIZES[1] * 4,
            "Sair",
            click_sound=self.click_sound,
        ):
            pygame.display.quit()
            sys.exit()

        return None

    def _handle_feedback_menu(self, feedback_type: str):
        """Gerencia as telas de feedback (Feedback_1, Feedback_2, Feedback_3)."""
        if feedback_type == "Feedback_1":
            # trofeu = Image.load("Assets/Kartea/trofeu - 25.png")
            trofeu = Image.load(GameSettings.MENU_FEEDBACK_25)
            Image.draw(self.surface, trofeu, (0, 0))
            action_on_play = "prev"
        elif feedback_type == "Feedback_2":
            # trofeu = Image.load("Assets/Kartea/trofeu - 50.png")
            trofeu = Image.load(GameSettings.MENU_FEEDBACK_50)
            Image.draw(self.surface, trofeu, (0, 0))
            action_on_play = "rest"
        elif feedback_type == "Feedback_3":
            # trofeu = Image.load("Assets/Kartea/trofeu - 75.png")
            trofeu = Image.load(GameSettings.MENU_FEEDBACK_75)
            Image.draw(self.surface, trofeu, (0, 0))
            action_on_play = "next"
        else:
            return None

        self.draw_feedback()

        if UI.button(
            self.surface,
            2,
            300 + GameSettings.BUTTONS_SIZES[1] * 4,
            "Jogar",
            click_sound=self.click_sound,
        ):
            return action_on_play

        if UI.button(
            self.surface,
            1,
            300 + GameSettings.BUTTONS_SIZES[1] * 4,
            "Sair",
            click_sound=self.click_sound,
        ):
            pygame.display.quit()
            sys.exit()

        return None

    def update(self):
        """Atualiza o menu atual e retorna a ação escolhida (game, prev, rest, next, etc.)."""
        self.draw()

        result = None

        if GameSettings.MENU == "Inicial":
            result = self._handle_inicial_menu()

        elif GameSettings.MENU == "Pause":
            result = self._handle_pause_menu()

        elif GameSettings.MENU in ("Feedback_1", "Feedback_2", "Feedback_3"):
            result = self._handle_feedback_menu(GameSettings.MENU)

        return result
