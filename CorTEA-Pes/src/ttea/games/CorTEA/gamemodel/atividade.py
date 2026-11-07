import random
from typing import List, Optional, Sequence, Tuple

from ttea.games.CorTEA.gameutil import GameSettings
from ttea.games.CorTEA.gameutil.gamesettings import ConfigFase

Cor = Tuple[int, int, int]


class Atividade:
    """Lógica principal do jogo: gera o caminho de cores e valida as
    respostas do jogador (classe ``Atividade`` do diagrama de classes).

    Um *caminho* é uma sequência de quadrados vizinhos (para cima, baixo,
    esquerda ou direita) que começa na linha de baixo da grade, perto do
    jogador, e termina na linha de cima. Todos os quadrados do caminho têm a
    mesma cor. Nas fases mais avançadas existem quadrados "isca" com essa
    mesma cor fora do caminho, então não basta seguir a cor: é preciso
    lembrar a ordem exibida pelo sistema.
    """

    def __init__(
        self,
        colunas: int = None,
        linhas: int = None,
        rng: Optional[random.Random] = None,
    ):
        self.colunas = colunas or GameSettings.COLUNAS
        self.linhas = linhas or GameSettings.LINHAS
        self.rng = rng or random.Random()

        self.config: Optional[ConfigFase] = None
        self.caminho: List[int] = []
        self.cores: List[Cor] = []
        self.cor_caminho: Cor = GameSettings.PALETA[0]
        self.iscas: List[int] = []
        self.passo_atual = 0

    # ====================== Geração ======================
    def gerar_sequencia(self, config: ConfigFase) -> List[int]:
        """Sorteia um novo caminho e as cores da grade para a fase."""
        self.config = config
        self.caminho = self._sortear_caminho(config.comprimento)
        self.passo_atual = 0

        paleta = list(GameSettings.PALETA)
        anterior = self.cor_caminho if self.cores else None
        candidatas = [c for c in paleta if c != anterior] or paleta
        self.cor_caminho = self.rng.choice(candidatas)

        outras = [c for c in paleta if c != self.cor_caminho]
        self.rng.shuffle(outras)
        outras = outras[: max(1, config.n_cores - 1)]

        total = self.colunas * self.linhas
        fora = [i for i in range(total) if i not in self.caminho]
        n_iscas = min(config.n_iscas, len(fora))
        self.iscas = self.rng.sample(fora, n_iscas)

        self.cores = []
        for indice in range(total):
            if indice in self.caminho or indice in self.iscas:
                self.cores.append(self.cor_caminho)
            else:
                self.cores.append(self.rng.choice(outras))
        return list(self.caminho)

    def _vizinhos(self, indice: int) -> List[int]:
        linha, coluna = divmod(indice, self.colunas)
        vizinhos = []
        if linha > 0:
            vizinhos.append(indice - self.colunas)
        if linha < self.linhas - 1:
            vizinhos.append(indice + self.colunas)
        if coluna > 0:
            vizinhos.append(indice - 1)
        if coluna < self.colunas - 1:
            vizinhos.append(indice + 1)
        return vizinhos

    def _sortear_caminho(self, comprimento: int) -> List[int]:
        """Caminho aleatório, sem repetir quadrados, da linha de baixo até a
        linha de cima, com exatamente ``comprimento`` quadrados."""
        comprimento = max(self.linhas, comprimento)
        ultima_linha = (self.linhas - 1) * self.colunas
        inicios = list(range(ultima_linha, ultima_linha + self.colunas))
        self.rng.shuffle(inicios)

        for inicio in inicios:
            caminho = self._buscar([inicio], comprimento)
            if caminho:
                return caminho
        # Não deve acontecer numa grade 4x3 com comprimento <= 12, mas, por
        # segurança, devolve uma coluna reta (sempre válida).
        coluna = self.rng.randrange(self.colunas)
        return [
            (linha * self.colunas) + coluna
            for linha in range(self.linhas - 1, -1, -1)
        ]

    def _buscar(self, caminho: List[int], comprimento: int):
        atual = caminho[-1]
        if len(caminho) == comprimento:
            return caminho if atual < self.colunas else None
        if atual < self.colunas:
            # Já chegou à linha de cima: o caminho termina ali.
            return None
        vizinhos = self._vizinhos(atual)
        self.rng.shuffle(vizinhos)
        for vizinho in vizinhos:
            if vizinho in caminho:
                continue
            achado = self._buscar(caminho + [vizinho], comprimento)
            if achado:
                return achado
        return None

    # ====================== Progresso ======================
    @property
    def esperado(self) -> int:
        """Índice do próximo quadrado a ser tocado."""
        return self.caminho[self.passo_atual]

    @property
    def percorridos(self) -> List[int]:
        """Índices dos quadrados já concluídos."""
        return self.caminho[: self.passo_atual]

    @property
    def concluido(self) -> bool:
        """True quando todos os passos do caminho foram cumpridos."""
        return bool(self.caminho) and self.passo_atual >= len(self.caminho)

    def validar_resposta(self, indice: int) -> bool:
        """Confere se ``indice`` é o próximo quadrado do caminho.

        Se for, avança o passo. Se não for, nada muda: o jogador continua
        no mesmo passo e pode tentar de novo (sem punição).
        """
        if self.concluido or indice != self.esperado:
            return False
        self.passo_atual += 1
        return True

    def cores_do_quadrado(self, indice: int) -> Cor:
        return self.cores[indice]
