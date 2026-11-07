"""classe alvo"""

import random
import time

import pygame

from ttea.games.kartea.gamemodel import Image
from ttea.games.kartea.gameutil import GameSettings


class Target:
    """Classe base que representa um alvo (estrela) no jogo."""

    def __init__(self, r: int = None):
        """
        Inicializa um alvo.

        Args:
            r (int, optional): Índice da pista (0, 1 ou 2). Se None,
            escolhe aleatoriamente.
        """
        # Tamanho do alvo
        size = GameSettings.TARGETS_SIZES

        # Define posição inicial de spawn
        road, start_pos = self.define_spawn_pos(r)

        # Configurações visuais e de posição
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        # self.images = [Image.load("Assets/Kartea/Star.png", size=size)]
        self.images = [Image.load(GameSettings.TARGET_IMAGE, size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0
        self.line = None

    def define_spawn_pos(self, r: int = None):
        """
        Define a pista e posição inicial do alvo.

        Args:
            r (int, optional): Pista desejada (0=esquerda, 1=meio, 2=direita)

        Returns:
            tuple: (road, start_pos)
        """
        if r is not None and 0 <= r <= 2:
            road = r
        else:
            road = random.randint(0, 2)  # 0 esq, 1 meio, 2 dir

        start_pos = GameSettings.OBJ_POS[road]
        return road, start_pos

    def define_pos(self, x: float, y: float):
        """
        Atualiza a posição do retângulo do alvo com base
        nas coordenadas projetadas.
        """
        # Mantém o tamanho atual do rect
        self.rect = pygame.Rect(x, y, self.rect.width, self.rect.height)

    def move(self):
        """
        Movimento padrão do alvo: desce a tela com pequena variação lateral
        dependendo da pista e da velocidade atual.
        """
        ve = GameSettings.TARGETS_MOVE_SPEED
        vel = [0, ve]

        if ve == 1:
            if self.current_pos[1] % 10 == 0:
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]
            elif self.current_pos[1] % 5 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [
                    # Image.load("Assets/Kartea/Star.png", size=self.tam)
                    Image.load(GameSettings.TARGET_IMAGE, size=self.tam)
                ]
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]
            else:
                vel = [0, ve]

        elif ve == 2:
            if self.current_pos[1] % 8 == 0:
                if self.current_road == 0:
                    vel = [-2, ve]
                elif self.current_road == 2:
                    vel = [2, ve]
            elif self.current_pos[1] % 4 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [
                    # Image.load("Assets/Kartea/Star.png", size=self.tam)
                    Image.load(GameSettings.TARGET_IMAGE, size=self.tam)
                ]
                if self.current_road == 0:
                    vel = [-2, ve]
                elif self.current_road == 2:
                    vel = [2, ve]
            else:
                vel = [0, ve]

        elif ve == 3:
            if self.current_pos[1] % 12 == 0:
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            elif self.current_pos[1] % 6 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [
                    # Image.load("Assets/Kartea/Star.png", size=self.tam)
                    Image.load(GameSettings.TARGET_IMAGE, size=self.tam)
                ]
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            else:
                vel = [0, ve]

        elif ve == 4:
            if self.current_pos[1] % 16 == 0:
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            elif self.current_pos[1] % 8 == 0:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [
                    # Image.load("Assets/Kartea/Star.png", size=self.tam)
                    Image.load(GameSettings.TARGET_IMAGE, size=self.tam)
                ]
                if self.current_road == 0:
                    vel = [-1, ve]
                elif self.current_road == 2:
                    vel = [1, ve]
            else:
                vel = [0, ve]

        else:  # velocidade padrão
            if self.current_pos[1] % 10 == 0:
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]
            else:
                self.rect.inflate_ip(3, 3)
                self.tam = (int(self.tam[0] + 3), int(self.tam[1] + 3))
                self.images = [
                    # Image.load("Assets/Kartea/Star.png", size=self.tam)
                    Image.load(GameSettings.TARGET_IMAGE, size=self.tam)
                ]
                if self.current_road == 0:
                    vel = [-3, ve]
                elif self.current_road == 2:
                    vel = [3, ve]

        # Aplica o movimento
        self.rect.move_ip(vel)
        self.current_pos = (
            self.current_pos[0] + vel[0],
            self.current_pos[1] + vel[1],
        )

    def move_to(self, x: float, y: float):
        """
        Movimento direto para uma posição específica (versão sobrecarregada).
        Usado em alguns contextos de atualização de posição.
        """
        vel = [x - self.current_pos[0], y - self.current_pos[1]]
        print("vel: ", vel)
        self.rect.move_ip(vel)
        self.current_pos = (x, y)

    def att_current_pos(self, x: float, y: float):
        """Atualiza diretamente a posição atual (usado pelo background)."""
        self.current_pos = (x, y)

    def animate(self):
        """Troca o frame da animação quando necessário."""
        t = time.time()
        if t > self.animation_timer:
            self.animation_timer = t + GameSettings.ANIMATION_SPEED
            self.current_frame += 1
            if self.current_frame > len(self.images) - 1:
                self.current_frame = 0

    def draw_hitbox(self, surface: pygame.Surface):
        """Desenha a hitbox do alvo (quando ativada)."""
        pygame.draw.rect(surface, (200, 60, 0), self.rect)

    def draw(self, surface: pygame.Surface):
        """Desenha o alvo na tela com animação."""
        self.animate()
        Image.draw(
            surface,
            self.images[self.current_frame],
            self.rect.center,
            pos_mode="center",
        )

        if GameSettings.DRAW_HITBOX:
            self.draw_hitbox(surface)

    def kill(
        self, surface: pygame.Surface, targets: list, sounds: dict
    ) -> int:
        """
        Remove o alvo da lista e retorna a pontuação.

        Retorna:
            10 se o jogador colidiu com o alvo (acerto)
            0 se o alvo saiu da tela por baixo (desvio)
        """
        # triste_fig = image.load('Assets/Kartea/triste.png')
        # feliz_fig = image.load('Assets/Kartea/feliz.png')
        negative_fig = Image.load(GameSettings.NEGATIVE_FEEDBACK_IMAGE)
        positive_fig = Image.load(GameSettings.POSITIVE_FEEDBACK_IMAGE)

        if self.current_pos[1] > GameSettings.SCREEN_HEIGHT:
            # Desviou do alvo (não acertou)
            targets.remove(self)
            sounds["screaming"].play()
            Image.draw(surface, negative_fig, (0, 0))
            # TODO gravar aqui os dados
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    settings.pista,
            #    self.current_road,
            #    "Desviou de Alvo",
            # )
            GameSettings.Alvo_d += 1
            return 0
        else:
            # Colidiu com o alvo (acerto)
            targets.remove(self)
            sounds["slap"].play()
            Image.draw(surface, positive_fig, (0, 0))
            # TODO gravar aqui os dados
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    settings.pista,
            #    self.current_road,
            #    "Colidiu com Alvo",
            # )
            GameSettings.Alvo_c += 1
            return 10
