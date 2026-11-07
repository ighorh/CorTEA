from ttea.games.CorTEA.gameutil import GameSettings


class Feedback:
    """Mensagem temporária mostrada ao jogador (acerto, erro, etc.).

    Recebe o tempo (ms) como argumento, para que o relógio do jogo (que
    para durante a pausa) seja o único usado.
    """

    def __init__(self):
        self.mensagem = ""
        self.cor = (0, 0, 0)
        self._fim = 0

    def mostrar(
        self, mensagem: str, cor: tuple, agora: int, duracao: int = None
    ) -> None:
        """Passa a exibir a mensagem, contando o tempo a partir de ``agora``."""
        self.mensagem = mensagem
        self.cor = cor
        self._fim = agora + (
            GameSettings.DURACAO_FEEDBACK if duracao is None else duracao
        )

    def ativo(self, agora: int) -> bool:
        """True enquanto a mensagem ainda deve aparecer na tela."""
        return bool(self.mensagem) and agora < self._fim

    def limpar(self) -> None:
        self.mensagem = ""
        self._fim = 0
