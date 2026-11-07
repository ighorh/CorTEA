from ttea.games.CorTEA.gameutil import GameSettings


class SistemaAjuda:
    """Gerencia as ajudas visuais (classe ``SistemaAjuda`` do diagrama).

    Quando o jogador fica um tempo sem responder, o próximo quadrado do
    caminho pisca. Cada ajuda usada consome uma unidade do estoque e custa
    uma pequena penalidade de pontos; novas ajudas são concedidas como
    recompensa quando o jogador conclui uma fase com sucesso.
    """

    def __init__(
        self,
        quantidade: int = None,
        maximo: int = None,
        tempo_limite_inatividade: int = None,
        penalidade: int = None,
    ):
        self.maximo_ajudas = (
            GameSettings.AJUDAS_MAXIMO if maximo is None else maximo
        )
        self.quantidade_disponivel = min(
            self.maximo_ajudas,
            GameSettings.AJUDAS_INICIAIS if quantidade is None else quantidade,
        )
        self.tempo_limite_inatividade = (
            GameSettings.TEMPO_INATIVIDADE_AJUDA
            if tempo_limite_inatividade is None
            else tempo_limite_inatividade
        )
        self.penalidade_pontuacao = (
            GameSettings.PENALIDADE_AJUDA if penalidade is None else penalidade
        )
        self.ajuda_ativa = False
        self._ultima_acao = 0

    def reiniciar_tempo(self, agora: int) -> None:
        """Zera a contagem de inatividade e apaga a ajuda em exibição."""
        self._ultima_acao = agora
        self.ajuda_ativa = False

    def possui_ajuda_disponivel(self) -> bool:
        return self.quantidade_disponivel > 0

    def verificar_inatividade(self, agora: int) -> bool:
        """True se o jogador ficou parado tempo demais e há ajuda a dar."""
        return (
            not self.ajuda_ativa
            and self.possui_ajuda_disponivel()
            and agora - self._ultima_acao >= self.tempo_limite_inatividade
        )

    def exibir_ajuda(self) -> None:
        self.ajuda_ativa = True

    def consumir_ajuda(self) -> None:
        self.quantidade_disponivel = max(0, self.quantidade_disponivel - 1)

    def aplicar_penalidade(self, pontos: int) -> int:
        """Retorna a pontuação depois de descontar o custo da ajuda (nunca
        abaixo de zero)."""
        return max(0, pontos - self.penalidade_pontuacao)

    def conceder_ajuda(self) -> bool:
        """Recompensa: +1 ajuda, até o máximo. True se concedeu."""
        if self.quantidade_disponivel >= self.maximo_ajudas:
            return False
        self.quantidade_disponivel += 1
        return True
