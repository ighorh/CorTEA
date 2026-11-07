import pygame

from ttea.games.kartea.gameutil import GameSettings
# from settings import *
from ttea.games.kartea.gameutil.alphablit import alpha_blit


class UI:
    """Classe utilitária responsável por desenhar textos e botões na interface do jogo."""

    @staticmethod
    def draw_text(
        surface: pygame.Surface,
        text: str,
        pos: tuple,
        color: tuple,
        font=GameSettings.FONTS["medium"],
        pos_mode: str = "top_left",
        shadow: bool = False,
        shadow_color: tuple = (0, 0, 0),
        shadow_offset: int = 2,
    ):
        """
        Desenha texto na tela com opção de sombra.

        Args:
            surface (pygame.Surface): Superfície onde desenhar
            text (str): Texto a ser renderizado
            pos (tuple): Posição (x, y)
            color (tuple): Cor do texto
            font: Fonte do pygame
            pos_mode (str): "top_left" ou "center"
            shadow (bool): Se deve desenhar sombra
            shadow_color (tuple): Cor da sombra
            shadow_offset (int): Deslocamento da sombra
        """
        label = font.render(text, True, color)
        label_rect = label.get_rect()

        if pos_mode == "top_left":
            label_rect.x, label_rect.y = pos
        elif pos_mode == "center":
            label_rect.center = pos

        # Desenha sombra (se ativada)
        if shadow:
            label_shadow = font.render(text, True, shadow_color)
            alpha_blit(
                surface,
                label_shadow,
                (label_rect.x - shadow_offset, label_rect.y + shadow_offset),
            )

        # Desenha o texto principal
        alpha_blit(surface, label, label_rect)

    @staticmethod
    def button(
        surface: pygame.Surface,
        pos_x: int,
        pos_y: int,
        text: str = None,
        click_sound: pygame.mixer.Sound = None,
    ) -> bool:
        """
        Desenha um botão e retorna True se ele foi clicado.

        Args:
            surface (pygame.Surface): Superfície onde desenhar
            pos_x (int): 0 = centro, 1 = esquerda, 2 = direita
            pos_y (int): Posição Y do botão
            text (str): Texto do botão (opcional)
            click_sound (pygame.mixer.Sound): Som a tocar ao clicar

        Returns:
            bool: True se o botão foi pressionado neste frame
        """
        # Define a posição horizontal do botão
        if pos_x == 1:  # esquerda
            rect = pygame.Rect(
                (
                    GameSettings.SCREEN_WIDTH // 4
                    - GameSettings.BUTTONS_SIZES[0] // 2,
                    pos_y,
                ),
                GameSettings.BUTTONS_SIZES,
            )
        elif pos_x == 2:  # direita
            rect = pygame.Rect(
                (
                    3 * GameSettings.SCREEN_WIDTH // 4
                    - GameSettings.BUTTONS_SIZES[0] // 2,
                    pos_y,
                ),
                GameSettings.BUTTONS_SIZES,
            )
        else:  # centro (padrão)
            rect = pygame.Rect(
                (
                    GameSettings.SCREEN_WIDTH // 2
                    - GameSettings.BUTTONS_SIZES[0] // 2,
                    pos_y,
                ),
                GameSettings.BUTTONS_SIZES,
            )

        # Verifica se o mouse está sobre o botão
        on_button = rect.collidepoint(pygame.mouse.get_pos())

        # Define a cor do botão
        color = (
            GameSettings.COLORS["buttons"]["second"]
            if on_button
            else GameSettings.COLORS["buttons"]["default"]
        )

        # Desenha sombra do botão
        pygame.draw.rect(
            surface,
            GameSettings.COLORS["buttons"]["shadow"],
            (rect.x - 6, rect.y - 6, rect.w, rect.h),
        )

        # Desenha o botão principal
        pygame.draw.rect(surface, color, rect)

        # Desenha o texto dentro do botão (se houver)
        if text is not None:
            UI.draw_text(
                surface,
                text,
                rect.center,
                GameSettings.COLORS["buttons"]["text"],
                pos_mode="center",
                shadow=True,
                shadow_color=GameSettings.COLORS["buttons"]["shadow"],
            )

        # Verifica clique do mouse
        if on_button and pygame.mouse.get_pressed()[0]:
            if click_sound is not None:
                click_sound.play()
            return True

        return False
