import math

import pygame
from ttea.games.CorTEA.gameutil import GameSettings


class UI:
    """Classe utilitária responsável por desenhar textos, botões, ícones e
    indicadores de progresso."""

    @staticmethod
    def draw_text(
        surface: pygame.Surface,
        text: str,
        pos: tuple,
        color: tuple,
        font=None,
        anchor: str = "center",
    ):
        """
        Desenha um texto na tela.

        Args:
            surface (pygame.Surface): Superfície onde desenhar
            text (str): Texto a ser renderizado
            pos (tuple): Posição (x, y) do ponto de ancoragem
            color (tuple): Cor do texto
            font: Fonte do pygame (padrão: fonte de texto do jogo)
            anchor (str): Ponto do texto que fica em ``pos``, como
                "center", "midleft", "bottomleft" ou "bottomright"
        """
        if font is None:
            font = GameSettings.FONTS["text"]
        label = font.render(text, True, color)
        surface.blit(label, label.get_rect(**{anchor: pos}))

    @staticmethod
    def button(
        surface: pygame.Surface,
        button: pygame.Rect,
        text: str,
        color: tuple = (35, 35, 35),
        progresso: float = 0.0,
        habilitado: bool = True,
    ):
        """Desenha um botão com sombra e destaque ao passar o mouse.

        ``progresso`` (0 a 1) desenha uma barra de preenchimento enquanto o
        pé do jogador permanece sobre o botão. ``habilitado=False`` desenha
        o botão apagado.
        """
        hovered = habilitado and (
            button.collidepoint(pygame.mouse.get_pos()) or progresso > 0
        )
        shadow = button.move(0, 5)
        fill_color = (255, 255, 255) if hovered else (245, 245, 245)
        border_color = (35, 35, 35) if hovered else (110, 110, 110)
        if not habilitado:
            fill_color = (225, 225, 225)
            border_color = (170, 170, 170)
            color = (150, 150, 150)

        pygame.draw.rect(
            surface,
            (35, 35, 35) if habilitado else (170, 170, 170),
            shadow,
            border_radius=10,
        )
        pygame.draw.rect(surface, fill_color, button, border_radius=10)
        if progresso > 0:
            barra = pygame.Rect(
                button.left + 4,
                button.bottom - 12,
                int((button.width - 8) * progresso),
                8,
            )
            pygame.draw.rect(surface, (0, 170, 70), barra, border_radius=4)
        pygame.draw.rect(surface, border_color, button, 2, border_radius=10)

        UI.draw_text(surface, text, button.center, color)

    @staticmethod
    def key(surface: pygame.Surface, rect, label: str):
        """Desenha o desenho de uma tecla do teclado com o texto dentro."""
        rect = pygame.Rect(rect)
        pygame.draw.rect(surface, (55, 55, 55), rect, border_radius=8)
        pygame.draw.rect(
            surface, (220, 220, 220), rect.inflate(-6, -6), border_radius=5
        )
        UI.draw_text(surface, label, rect.center, (35, 35, 35))

    @staticmethod
    def clarear_cor(cor_rgb: tuple, fator: float = 0.15) -> tuple:
        """Retorna a cor misturada com branco na proporção ``fator``."""
        return UI.misturar(cor_rgb, (255, 255, 255), fator)

    @staticmethod
    def misturar(cor_a: tuple, cor_b: tuple, fator: float) -> tuple:
        """Mistura ``cor_a`` com ``cor_b`` (fator 0 = só A, 1 = só B)."""
        return tuple(
            int(a + (b - a) * fator) for a, b in zip(cor_a[:3], cor_b[:3])
        )

    @staticmethod
    def anel_progresso(
        surface: pygame.Surface,
        centro: tuple,
        raio: int,
        fracao: float,
        largura: int = 8,
    ):
        """Anel que se completa no sentido horário (a partir do topo)."""
        if fracao <= 0:
            return
        fracao = min(1.0, fracao)
        passos = max(2, int(48 * fracao))
        pontos = []
        for i in range(passos + 1):
            ang = -math.pi / 2 + 2 * math.pi * fracao * i / passos
            pontos.append(
                (centro[0] + raio * math.cos(ang), centro[1] + raio * math.sin(ang))
            )
        pygame.draw.lines(surface, (35, 35, 35), False, pontos, largura + 5)
        pygame.draw.lines(surface, (255, 255, 255), False, pontos, largura)

    @staticmethod
    def icone_certo(surface: pygame.Surface, centro: tuple, raio: int = 24):
        """Círculo verde com um "visto" branco (fase concluída)."""
        cx, cy = centro
        pygame.draw.circle(surface, (20, 170, 70), centro, raio)
        pontos = [
            (cx - raio * 0.45, cy + raio * 0.02),
            (cx - raio * 0.12, cy + raio * 0.38),
            (cx + raio * 0.48, cy - raio * 0.35),
        ]
        pygame.draw.lines(surface, (255, 255, 255), False, pontos, 5)

    @staticmethod
    def icone_x(surface: pygame.Surface, centro: tuple, raio: int = 24):
        """Círculo escuro com um "x" branco (fase não concluída)."""
        cx, cy = centro
        pygame.draw.circle(surface, (25, 25, 25), centro, raio)
        d = raio * 0.4
        pygame.draw.line(
            surface, (255, 255, 255), (cx - d, cy - d), (cx + d, cy + d), 5
        )
        pygame.draw.line(
            surface, (255, 255, 255), (cx - d, cy + d), (cx + d, cy - d), 5
        )

    @staticmethod
    def trofeu(surface: pygame.Surface, centro: tuple, escala: float = 1.0):
        """Desenha um troféu simples (tela de conclusão)."""
        cx, cy = centro
        cor = (60, 60, 60)

        def e(v):
            return int(v * escala)

        # taça
        pygame.draw.rect(
            surface,
            cor,
            (cx - e(55), cy - e(80), e(110), e(80)),
            border_bottom_left_radius=e(55),
            border_bottom_right_radius=e(55),
        )
        # alças
        pygame.draw.circle(surface, cor, (cx - e(62), cy - e(45)), e(26), e(10))
        pygame.draw.circle(surface, cor, (cx + e(62), cy - e(45)), e(26), e(10))
        # haste e base
        pygame.draw.rect(surface, cor, (cx - e(10), cy, e(20), e(40)))
        pygame.draw.rect(
            surface, cor, (cx - e(45), cy + e(40), e(90), e(20)), border_radius=e(5)
        )
