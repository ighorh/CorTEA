from typing import List

from ttea.games.CorTEA.gameutil import GameSettings


class Desempenho:
    """Resultados do jogador em uma tentativa de fase (classe ``Desempenho``
    do diagrama de classes).

    Guarda acertos (A), erros (E), acertos consecutivos (C) e os tempos de
    resposta, e calcula o índice de desempenho (ID) da Equação 1 do artigo::

        ID = (A x 2) - (E x 1) + (C x 1,5)

    Aqui, C é a *maior* sequência de acertos seguidos da tentativa.
    """

    def __init__(self):
        self.acertos = 0
        self.erros = 0
        self.acertos_consecutivos = 0  # sequência em andamento
        self.melhor_sequencia = 0  # C da equação
        self.tempos: List[float] = []  # segundos

    def atualizar_dados(self, acertou: bool, tempo_resposta: float) -> None:
        """Registra uma resposta do jogador."""
        if acertou:
            self.acertos += 1
            self.acertos_consecutivos += 1
            self.melhor_sequencia = max(
                self.melhor_sequencia, self.acertos_consecutivos
            )
            self.tempos.append(max(0.0, tempo_resposta))
        else:
            self.erros += 1
            self.acertos_consecutivos = 0

    @property
    def total_respostas(self) -> int:
        return self.acertos + self.erros

    @property
    def tempo_medio_resposta(self) -> float:
        """Tempo médio (s) entre a apresentação do estímulo e o acerto."""
        if not self.tempos:
            return 0.0
        return sum(self.tempos) / len(self.tempos)

    def calcular_indice(self) -> float:
        """Índice de desempenho (ID) da tentativa."""
        return (
            self.acertos * GameSettings.PESO_ACERTOS
            - self.erros * GameSettings.PESO_ERROS
            + self.melhor_sequencia * GameSettings.PESO_CONSECUTIVOS
        )

    @staticmethod
    def indice_maximo(total_passos: int) -> float:
        """ID de uma tentativa perfeita (todos acertos, nenhum erro)."""
        return total_passos * (
            GameSettings.PESO_ACERTOS + GameSettings.PESO_CONSECUTIVOS
        )

    def verificar_progresso(self, total_passos: int) -> bool:
        """True se o ID atingiu a pontuação mínima para avançar de fase
        (RF12: abaixo disso o jogador repete a mesma fase)."""
        if total_passos <= 0:
            return False
        minimo = GameSettings.ID_MINIMO_FRACAO * self.indice_maximo(
            total_passos
        )
        return self.calcular_indice() >= minimo
