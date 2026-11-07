import datetime
from typing import List, Optional


class Usuario:
    """Quem joga (classe ``Usuario`` do diagrama de classes)."""

    def __init__(self, id_usuario: int, nome: str):
        self.id_usuario = id_usuario
        self.nome = nome

    @classmethod
    def carregar(cls, id_usuario: int) -> "Usuario":
        """Busca o nome do jogador cadastrado na plataforma T-TEA.

        Se o cadastro não puder ser lido (ex.: jogo aberto fora da
        plataforma), usa um nome genérico.
        """
        nome = None
        try:
            from ttea.dao.playercsvdao import PlayerCSVDAO

            jogador = PlayerCSVDAO().select(id_usuario)
            if jogador is not None:
                nome = jogador.name
        except Exception:
            nome = None
        return cls(id_usuario, nome or f"Jogador {id_usuario}")


class Sessao:
    """Uma execução do jogo (classe ``Sessao`` do diagrama de classes).

    Acumula o que a tela de conclusão precisa mostrar: pontos, tempo total,
    tempo médio por fase e tempo médio de resposta.
    """

    def __init__(self, usuario: Usuario, inicio: Optional[datetime.datetime] = None):
        self.usuario = usuario
        self.data_hora = inicio or datetime.datetime.now()
        self.id_sessao = (
            f"{usuario.id_usuario}-{self.data_hora.strftime('%Y%m%d%H%M%S')}"
        )
        self.fim: Optional[datetime.datetime] = None
        self.duracao_fases: List[float] = []  # s por tentativa de fase
        self.tempos_resposta: List[float] = []  # s por acerto

    def iniciar(self) -> None:
        self.data_hora = datetime.datetime.now()

    def finalizar(self) -> None:
        self.fim = datetime.datetime.now()

    def registrar_tentativa(self, duracao: float, tempos: List[float]) -> None:
        self.duracao_fases.append(duracao)
        self.tempos_resposta.extend(tempos)

    @property
    def tempo_medio_fase(self) -> float:
        if not self.duracao_fases:
            return 0.0
        return sum(self.duracao_fases) / len(self.duracao_fases)

    @property
    def tempo_medio_resposta(self) -> float:
        if not self.tempos_resposta:
            return 0.0
        return sum(self.tempos_resposta) / len(self.tempos_resposta)
