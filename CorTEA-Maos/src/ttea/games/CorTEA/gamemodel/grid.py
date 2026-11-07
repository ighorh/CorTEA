from typing import List, Optional, Tuple

import pygame
from ttea.games.CorTEA.gameutil import GameSettings


class Grid:
    """Grade de quadrados: geometria e detecção de posição.

    As cores de cada quadrado mudam a cada rodada e ficam na ``Atividade``.
    """

    def __init__(self):
        self.colunas = GameSettings.COLUNAS
        self.linhas = GameSettings.LINHAS
        self.tam_quad = GameSettings.TAM_QUAD
        self.espaco = GameSettings.ESPACO
        self.offset_x = GameSettings.OFFSET_X
        self.offset_y = GameSettings.OFFSET_Y
        self.largura = GameSettings.LARGURA_GRADE
        self.altura = GameSettings.ALTURA_GRADE

        # Área total ocupada pela grade
        self.area = pygame.Rect(
            self.offset_x, self.offset_y, self.largura, self.altura
        )

        # Lista de (índice, retângulo) de cada quadrado, linha a linha
        self.quadrados: List[Tuple[int, pygame.Rect]] = []
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                indice = (linha * self.colunas) + coluna
                x = self.offset_x + coluna * (self.tam_quad + self.espaco)
                y = self.offset_y + linha * (self.tam_quad + self.espaco)
                self.quadrados.append(
                    (indice, pygame.Rect(x, y, self.tam_quad, self.tam_quad))
                )

    def retangulo(self, indice: int) -> "pygame.Rect":
        return self.quadrados[indice][1]

    def indice_em(self, posicao) -> Optional[int]:
        """Retorna o índice do quadrado sob a posição, ou None."""
        for indice, retangulo in self.quadrados:
            if retangulo.collidepoint(posicao):
                return indice
        return None
