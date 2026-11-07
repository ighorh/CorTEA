from typing import TYPE_CHECKING, Optional

import pygame

from ttea.games.kartea.gameutil import GameSettings
from ttea.games.kartea.gameutil.alphablit import alpha_blit

if TYPE_CHECKING:
    from ttea.games.kartea.gamemodel import Target


class Line:
    """Representa uma linha (segmento) da estrada no sistema pseudo-3D."""

    def __init__(self):
        # Posição 3D
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0

        # Posição projetada 2D
        self.X: float = 0.0
        self.Y: float = 0.0
        self.W: float = 0.0

        self.scale: float = 0.0  # Escala de projeção
        self.curve: float = 0.0
        self.clip: float = 0.0

        # Sprite lateral esquerdo (árvore)
        self.spriteX: float = 0.0
        self.sprite: Optional[pygame.Surface] = None
        self.sprite_rect: Optional[pygame.Rect] = None

        # Sprite lateral direito (árvore)
        self.sprite2X: float = 0.0
        self.sprite2: Optional[pygame.Surface] = None
        self.sprite2_rect: Optional[pygame.Rect] = None

        # Target / Obstáculo
        self.targetX: float = 0.0
        self.target: Optional["Target"] = None
        self.target_rect: Optional[pygame.Rect] = None

    def project(self, camX: float, camY: float, camZ: float):
        """Projeta a posição 3D para coordenadas 2D na tela."""
        self.scale = GameSettings.CAMERA_DEPTH / (self.z - camZ)
        self.X = (
            (1 + self.scale * (self.x - camX)) * GameSettings.SCREEN_WIDTH / 2
        )
        self.Y = (
            (1 - self.scale * (self.y - camY)) * GameSettings.SCREEN_HEIGHT / 5
        )
        self.W = (
            self.scale
            * GameSettings.ROAD_WIDTH
            * GameSettings.SCREEN_WIDTH
            / 2
        )

    def drawSprite(self, draw_surface: pygame.Surface):
        """Desenha o sprite lateral esquerdo (árvore esquerda)."""
        if self.sprite is None:
            return

        w = self.sprite.get_width()
        h = self.sprite.get_height()

        destX = (
            self.X + self.scale * self.spriteX * GameSettings.SCREEN_WIDTH / 2
        )
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.spriteX
        destY += destH * -1

        clipH = destY * self.spriteX
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        if destW > (2 * w):
            return

        scaled_sprite = pygame.transform.scale(self.sprite, (destW, destH))
        alpha_blit(draw_surface, scaled_sprite, (destX, destY))

    def drawSprite2(self, draw_surface: pygame.Surface):
        """Desenha o sprite lateral direito (árvore direita)."""
        if self.sprite2 is None:
            return

        w = self.sprite2.get_width()
        h = self.sprite2.get_height()

        destX = (
            self.X + self.scale * self.sprite2X * GameSettings.SCREEN_WIDTH / 2
        )
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.sprite2X
        destY += destH * -1

        clipH = destY * self.sprite2X
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        if destW > (2 * w):
            return

        scaled_sprite = pygame.transform.scale(self.sprite2, (destW, destH))
        alpha_blit(draw_surface, scaled_sprite, (destX, destY))

    def drawTarget(self, draw_surface: pygame.Surface):
        """Desenha o alvo ou obstáculo associado a esta linha."""
        if self.target is None:
            return

        w = self.target.images[0].get_width()
        h = self.target.images[0].get_height()

        # Define posição lateral na pista conforme a road atual
        if self.target.current_road == 0:
            self.targetX = -2.25
        elif self.target.current_road == 1:
            self.targetX = -0.5
        else:
            self.targetX = 1.25

        destX = (
            self.X + self.scale * self.targetX * GameSettings.SCREEN_WIDTH / 2
        )
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.targetX
        destY += destH * -1

        # Atualiza posição do target
        self.target.define_pos(destX, destY)

        # Clipping
        clipH = destY + destH - self.clip
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        if destW > 1.5 * w:
            return

        # Desenha o target escalado
        scaled_sprite = pygame.transform.scale(
            self.target.images[0], (destW, destH)
        )
        alpha_blit(draw_surface, scaled_sprite, (destX, destY))

        # Desenha hitbox se estiver ativada
        if GameSettings.DRAW_HITBOX:
            self.target.draw_hitbox(draw_surface)
