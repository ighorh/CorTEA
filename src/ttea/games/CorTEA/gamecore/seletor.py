from typing import Dict, Hashable, Iterable, Optional


class SeletorPermanencia:
    """Seleciona um alvo quando a mão fica sobre ele por tempo suficiente.

    Em vez de "tocar" o quadrado assim que a mão entra nele (o que gera
    erros quando a mão só atravessa a grade), o jogador precisa manter a mão
    sobre o quadrado por ``tempo_ms``. Depois de selecionado, o alvo só pode
    ser selecionado de novo depois que a mão sair dele.

    Os alvos são qualquer objeto com o método ``collidepoint`` (por exemplo,
    ``pygame.Rect``), identificados por uma chave.
    """

    def __init__(self, tempo_ms: int, tolerancia_ms: int = 0):
        self.tempo_ms = tempo_ms
        self.tolerancia_ms = tolerancia_ms
        self._inicio: Dict[Hashable, int] = {}
        self._ultimo_visto: Dict[Hashable, int] = {}
        self._travados = set()

    def reiniciar(self) -> None:
        self._inicio.clear()
        self._ultimo_visto.clear()
        self._travados.clear()

    def progresso(self, chave: Hashable, agora: int) -> float:
        """Fração (0 a 1) da permanência já cumprida sobre o alvo."""
        inicio = self._inicio.get(chave)
        if inicio is None or chave in self._travados:
            return 0.0
        return max(0.0, min(1.0, (agora - inicio) / self.tempo_ms))

    def atualizar(
        self, agora: int, pontos: Iterable, alvos: Dict[Hashable, object]
    ) -> Optional[Hashable]:
        """Atualiza as permanências e devolve a chave do alvo selecionado
        neste instante (ou ``None``)."""
        pontos = list(pontos)

        # Esquece alvos que deixaram de existir
        for chave in list(self._inicio):
            if chave not in alvos:
                self._inicio.pop(chave, None)
                self._ultimo_visto.pop(chave, None)
                self._travados.discard(chave)
        self._travados &= set(alvos)

        escolhido = None
        for chave, retangulo in alvos.items():
            sobre = any(retangulo.collidepoint(p) for p in pontos)
            if sobre:
                self._ultimo_visto[chave] = agora
                if chave not in self._inicio:
                    self._inicio[chave] = agora
                if (
                    escolhido is None
                    and chave not in self._travados
                    and agora - self._inicio[chave] >= self.tempo_ms
                ):
                    escolhido = chave
            else:
                visto = self._ultimo_visto.get(chave)
                if visto is not None and agora - visto <= self.tolerancia_ms:
                    continue  # a detecção piscou: mantém a contagem
                self._inicio.pop(chave, None)
                self._ultimo_visto.pop(chave, None)
                self._travados.discard(chave)

        if escolhido is not None:
            self._travados.add(escolhido)
        return escolhido
