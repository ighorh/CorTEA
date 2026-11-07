import pygame

from ttea.games.kartea.gamemodel import Image
from ttea.games.kartea.gamemodel.target import Target
from ttea.games.kartea.gameutil import GameSettings


class Obstacle(Target):
    """Classe que representa um obstáculo no jogo. Herda de Target."""

    def __init__(self, r: int = None):
        """
        Inicializa um obstáculo com base na pista (r).

        Args:
            r (int): Índice da pista (0, 1 ou 2) onde o obstáculo
            deve aparecer.
        """
        # Chama o construtor da classe Target para
        super().__init__(r)
        # Define tamanho
        size = GameSettings.OBSTACLE_SIZES

        # Define posição inicial de spawn
        road, start_pos = self.define_spawn_pos(r)

        # Configurações do obstáculo
        self.tam = size
        self.rect = pygame.Rect(start_pos[0], start_pos[1], size[0], size[1])
        # self.images = [Image.load("Assets/Kartea/Obstaculo.png", size=size)]
        self.images = [Image.load(GameSettings.OBSTACLE_IMAGE, size=size)]
        self.current_frame = 0
        self.current_pos = start_pos
        self.current_road = road
        self.animation_timer = 0

    def move(self):
        """Move o obstáculo para baixo com variação lateral dependendo
        da pista e velocidade."""
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
                # self.images = [
                #    Image.load("Assets/Kartea/Obstaculo.png", size=self.tam)
                # ]
                self.images = [
                    Image.load(GameSettings.OBSTACLE_IMAGE, size=self.tam)
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
                # self.images = [
                #    Image.load("Assets/Kartea/Obstaculo.png", size=self.tam)
                # ]
                self.images = [
                    Image.load(GameSettings.OBSTACLE_IMAGE, size=self.tam)
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
                # self.images = [
                #    Image.load("Assets/Kartea/Obstaculo.png", size=self.tam)
                # ]
                self.images = [
                    Image.load(GameSettings.OBSTACLE_IMAGE, size=self.tam)
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
                # self.images = [
                #    Image.load("Assets/Kartea/Obstaculo.png", size=self.tam)
                # ]
                self.images = [
                    Image.load(GameSettings.OBSTACLE_IMAGE, size=self.tam)
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
                # self.images = [
                #    Image.load("Assets/Kartea/Obstaculo.png", size=self.tam)
                # ]
                self.images = [
                    Image.load(GameSettings.OBSTACLE_IMAGE, size=self.tam)
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

    def kill(
        self, surface: pygame.Surface, targets: list, sounds: dict
    ) -> int:
        """
        Remove o obstáculo da lista e retorna pontos.
        - Se saiu da tela por baixo → Desviou (10 pontos)
        - Se colidiu com o carro → Colidiu (0 pontos)
        """
        # triste_fig = Image.load("Assets/Kartea/triste.png")
        # feliz_fig = Image.load("Assets/Kartea/feliz.png")
        negative_fig = Image.load(GameSettings.NEGATIVE_FEEDBACK_IMAGE)
        positive_fig = Image.load(GameSettings.POSITIVE_FEEDBACK_IMAGE)

        if self.current_pos[1] > GameSettings.SCREEN_HEIGHT:
            # Desviou do obstáculo
            targets.remove(self)
            sounds["slap"].play()
            Image.draw(surface, positive_fig, (0, 0))
            # TODO gravar aqui os dados
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    GameSettings.pista,
            #    self.current_road,
            #    "Desviou de Obstaculo",
            # )
            GameSettings.Obst_d += 1
            return 10
        else:
            # Colidiu com o obstáculo
            targets.remove(self)
            sounds["screaming"].play()
            Image.draw(surface, negative_fig, (0, 0))
            # TODO gravar aqui os dados
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    GameSettings.pista,
            #    self.current_road,
            #    "Colidiu com Obstaculo",
            # )
            GameSettings.Obst_c += 1
            return 0
