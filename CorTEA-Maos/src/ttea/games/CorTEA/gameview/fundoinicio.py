import math
import random
from typing import Dict, List, Optional, Tuple

import pygame
from ttea.games.CorTEA.gameui import UI
from ttea.games.CorTEA.gameutil import GameSettings

Cor = Tuple[int, int, int]


class FundoInicio:
    """Fundo animado da tela inicial: uma fase do CorTEA vista em 3D.

    A grade 4x3 vira um tabuleiro de blocos coloridos sobre uma plataforma,
    em perspectiva (como o chão projetado visto de cima e de frente). Um
    caminho se acende quadrado por quadrado, igual à exibição da partida: o
    bloco da vez sobe como um pilar brilhante e os já percorridos ficam um
    pouco elevados, com borda dourada. Depois de cada caminho vem outro, com
    outra cor.
    """

    # Câmera: distância focal, altura e linha do horizonte (em pixels)
    FOCO = 440
    ALTURA_CAMERA = 4.0
    HORIZONTE = 50
    Z_PERTO = 3.6  # profundidade da borda da frente do tabuleiro

    TAM = 1.0  # lado de um quadrado (unidades do "chão")
    ESPACO = 0.1
    ESPESSURA = 0.22  # altura de um bloco parado
    ELEVACAO_PERCORRIDO = 0.12
    ELEVACAO_ACESO = 0.55

    PASSO_MS = 650
    PAUSA_MS = 1500

    # Caminhos de exemplo (índices da grade, da linha de baixo até a de cima)
    CAMINHOS = [
        [9, 5, 6, 2],
        [10, 11, 7, 3],
        [8, 4, 5, 1],
        [11, 10, 6, 5, 1],
    ]

    COR_CEU_TOPO = (18, 22, 58)
    COR_CEU_BASE = (86, 52, 140)
    COR_PLATAFORMA = (38, 42, 78)
    DOURADO = (255, 215, 0)

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.largura, self.altura = surface.get_size()
        self.cx = self.largura / 2
        self._ceu: Optional[pygame.Surface] = None
        self._cores_ciclo: Dict[int, List[Cor]] = {}
        self._brilho: Dict[Cor, pygame.Surface] = {}
        rng = random.Random(7)
        self._particulas = [
            (
                rng.uniform(0, self.largura),  # x
                rng.uniform(0, self.altura + 40),  # y inicial
                rng.uniform(6, 22),  # raio
                rng.uniform(8, 25),  # velocidade (px/s)
                rng.uniform(0, 2 * math.pi),  # fase do balanço
                rng.choice(GameSettings.PALETA),
            )
            for _ in range(26)
        ]
        self._bolhas: Dict[Tuple[int, Cor], pygame.Surface] = {}

    # ====================== Projeção ======================
    def projetar(self, x: float, z: float, h: float = 0.0) -> Tuple[float, float]:
        """Ponto do chão (x lateral, z profundidade, h altura) -> tela."""
        escala = self.FOCO / z
        return (
            self.cx + x * escala,
            self.HORIZONTE + (self.ALTURA_CAMERA - h) * escala,
        )

    def limites_quadrado(self, indice: int) -> Tuple[float, float, float, float]:
        """(x0, x1, z0, z1) do quadrado ``indice`` (linha 0 = fundo)."""
        linha, coluna = divmod(indice, GameSettings.COLUNAS)
        passo = self.TAM + self.ESPACO
        x0 = -GameSettings.COLUNAS * passo / 2 + self.ESPACO / 2 + coluna * passo
        z0 = self.Z_PERTO + (GameSettings.LINHAS - 1 - linha) * passo
        return x0, x0 + self.TAM, z0, z0 + self.TAM

    # ====================== Animação ======================
    def _ciclo(self, agora: int) -> Tuple[int, int]:
        """(índice do caminho, ms desde o início dele)."""
        duracoes = [
            len(c) * self.PASSO_MS + self.PAUSA_MS for c in self.CAMINHOS
        ]
        resto = agora % sum(duracoes)
        for k, duracao in enumerate(duracoes):
            if resto < duracao:
                return k, resto
            resto -= duracao
        return 0, 0  # pragma: no cover

    def _cores(self, k: int) -> List[Cor]:
        """Cores da grade no caminho ``k`` (fixas durante o caminho)."""
        if k not in self._cores_ciclo:
            rng = random.Random(100 + k)
            paleta = GameSettings.PALETA
            cor_caminho = paleta[k % len(paleta)]
            outras = [c for c in paleta if c != cor_caminho]
            rng.shuffle(outras)
            outras = outras[:3]
            caminho = self.CAMINHOS[k]
            total = GameSettings.COLUNAS * GameSettings.LINHAS
            self._cores_ciclo[k] = [
                cor_caminho if i in caminho else rng.choice(outras)
                for i in range(total)
            ]
        return self._cores_ciclo[k]

    def estado_quadrado(self, indice: int, agora: int) -> Tuple[float, float, bool]:
        """(altura do bloco, brilho 0-1, já percorrido) no instante ``agora``."""
        k, decorrido = self._ciclo(agora)
        caminho = self.CAMINHOS[k]
        if indice not in caminho:
            return self.ESPESSURA, 0.0, False
        posicao = caminho.index(indice)
        passo, resto = divmod(decorrido, self.PASSO_MS)
        fracao = resto / self.PASSO_MS
        base = self.ESPESSURA + self.ELEVACAO_PERCORRIDO
        if passo >= len(caminho):  # caminho completo: tudo pulsa junto
            pulso = 0.5 + 0.5 * math.sin(decorrido / 160)
            return base, 0.25 * pulso, True
        if posicao < passo:
            return base, 0.0, True
        if posicao == passo:
            onda = math.sin(math.pi * fracao)
            altura = (
                self.ESPESSURA
                + self.ELEVACAO_PERCORRIDO * fracao
                + self.ELEVACAO_ACESO * onda
            )
            return altura, 0.5 * onda, fracao > 0.5
        return self.ESPESSURA, 0.0, False

    # ====================== Desenho ======================
    def draw(self, agora: int) -> None:
        self.surface.blit(self._ceu_cache(), (0, 0))
        self._draw_particulas(agora)
        self._draw_plataforma()

        k, _ = self._ciclo(agora)
        cores = self._cores(k)
        colunas = GameSettings.COLUNAS
        # Do fundo para a frente; em cada linha, de fora para dentro.
        ordem_colunas = sorted(range(colunas), key=lambda c: -abs(c - (colunas - 1) / 2))
        for linha in range(GameSettings.LINHAS):
            for coluna in ordem_colunas:
                indice = linha * colunas + coluna
                altura, brilho, percorrido = self.estado_quadrado(indice, agora)
                self._draw_bloco(indice, cores[indice], altura, brilho, percorrido)

    def _ceu_cache(self) -> pygame.Surface:
        if self._ceu is None:
            ceu = pygame.Surface((self.largura, self.altura))
            for y in range(self.altura):
                cor = UI.misturar(
                    self.COR_CEU_TOPO, self.COR_CEU_BASE, y / max(1, self.altura - 1)
                )
                pygame.draw.line(ceu, cor, (0, y), (self.largura, y))
            self._ceu = ceu
        return self._ceu

    def _bolha(self, raio: int, cor: Cor) -> pygame.Surface:
        chave = (raio, cor)
        if chave not in self._bolhas:
            bolha = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
            for r in range(raio, 0, -2):
                alfa = int(38 * (1 - r / raio) + 6)
                pygame.draw.circle(bolha, (*cor, alfa), (raio, raio), r)
            self._bolhas[chave] = bolha
        return self._bolhas[chave]

    def _draw_particulas(self, agora: int) -> None:
        """Luzes coloridas desfocadas subindo devagar ao fundo."""
        s = agora / 1000
        faixa = self.altura + 60
        for x, y0, raio, velocidade, fase, cor in self._particulas:
            y = (y0 - velocidade * s) % faixa - 30
            x_balanco = x + 12 * math.sin(s * 0.7 + fase)
            bolha = self._bolha(int(raio), cor)
            self.surface.blit(bolha, (x_balanco - raio, y - raio))

    def _quad(self, pontos, cor, borda: Optional[Cor] = None, largura: int = 2):
        pygame.draw.polygon(self.surface, cor, pontos)
        if borda is not None:
            pygame.draw.polygon(self.surface, borda, pontos, largura)

    def _draw_plataforma(self) -> None:
        """Laje escura sob o tabuleiro, com borda clara (a área projetada)."""
        x0, _, _, _ = self.limites_quadrado(0)
        _, x1, _, _ = self.limites_quadrado(GameSettings.COLUNAS - 1)
        _, _, z0, _ = self.limites_quadrado(
            (GameSettings.LINHAS - 1) * GameSettings.COLUNAS
        )
        _, _, _, z1 = self.limites_quadrado(0)
        m = 0.22
        x0, x1, z0, z1 = x0 - m, x1 + m, z0 - m, z1 + m
        p = self.projetar
        topo = [p(x0, z0), p(x1, z0), p(x1, z1), p(x0, z1)]
        frente = [p(x0, z0), p(x1, z0), p(x1, z0, -0.15), p(x0, z0, -0.15)]
        self._quad(frente, UI.misturar(self.COR_PLATAFORMA, (0, 0, 0), 0.45))
        self._quad(topo, self.COR_PLATAFORMA, (120, 130, 200))

    def _draw_bloco(
        self, indice: int, cor: Cor, altura: float, brilho: float, percorrido: bool
    ) -> None:
        x0, x1, z0, z1 = self.limites_quadrado(indice)
        p = self.projetar
        cor_topo = UI.clarear_cor(cor, brilho) if brilho > 0 else cor

        # Lateral voltada para o centro (só aparece nos blocos de fora)
        if x1 < 0 or x0 > 0:
            xs = x1 if x1 < 0 else x0
            lateral = [p(xs, z0, altura), p(xs, z1, altura), p(xs, z1), p(xs, z0)]
            self._quad(lateral, UI.misturar(cor_topo, (0, 0, 0), 0.45))

        frente = [p(x0, z0, altura), p(x1, z0, altura), p(x1, z0), p(x0, z0)]
        self._quad(frente, UI.misturar(cor_topo, (0, 0, 0), 0.3))

        topo = [p(x0, z0, altura), p(x1, z0, altura), p(x1, z1, altura), p(x0, z1, altura)]
        borda = self.DOURADO if percorrido else UI.clarear_cor(cor_topo, 0.35)
        self._quad(topo, cor_topo, borda, 3 if percorrido else 2)

        # Reflexo suave no topo (efeito de material brilhante)
        m = 0.18
        reflexo = [
            p(x0 + m, z1 - m, altura),
            p(x0 + m + 0.35, z1 - m, altura),
            p(x0 + m, z1 - m - 0.25, altura),
        ]
        pygame.draw.polygon(self.surface, UI.clarear_cor(cor_topo, 0.45), reflexo)

        if brilho > 0:
            self._draw_brilho(p((x0 + x1) / 2, (z0 + z1) / 2, altura), cor, brilho)

    def _draw_brilho(self, centro, cor: Cor, intensidade: float) -> None:
        """Halo de luz sobre o bloco aceso."""
        if cor not in self._brilho:
            raio = 90
            halo = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
            clara = UI.clarear_cor(cor, 0.5)
            for r in range(raio, 0, -3):
                alfa = int(70 * (1 - r / raio) ** 2)
                pygame.draw.circle(halo, (*clara, alfa), (raio, raio), r)
            self._brilho[cor] = halo
        halo = self._brilho[cor].copy()
        halo.set_alpha(int(255 * min(1.0, intensidade * 2)))
        self.surface.blit(halo, halo.get_rect(center=(int(centro[0]), int(centro[1]))))
