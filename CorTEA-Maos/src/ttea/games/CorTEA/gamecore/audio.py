from typing import Dict, Optional

import numpy as np
import pygame
from ttea.games.CorTEA.gameutil import GameSettings

# Escala pentatônica (dó, ré, mi, sol, lá, dó, ré, mi): soa bem em qualquer
# ordem, então nenhum passo do caminho "soa errado".
_NOTAS = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.7, 1318.5]


class Sons:
    """Sons do jogo gerados por código (sem arquivos de áudio).

    Todos são curtos e suaves, com início e fim graduais, para não causar
    sobrecarga sensorial (RN05). Se não houver placa de som, o jogo
    continua em silêncio.
    """

    def __init__(self):
        self.disponivel = False
        self._sons: Dict[str, "pygame.mixer.Sound"] = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 2, 512)
            self._freq, _, self._canais = pygame.mixer.get_init()
            self._criar_sons()
            self.disponivel = True
        except Exception:
            self.disponivel = False

    # ====================== Geração ======================
    def _tom(self, freq: float, dur: float, vol: float = 0.35, harmonico=0.25):
        n = int(self._freq * dur)
        t = np.arange(n) / self._freq
        onda = np.sin(2 * np.pi * freq * t) + harmonico * np.sin(
            4 * np.pi * freq * t
        )
        # Envelope: ataque de 10 ms e queda suave até o fim
        ataque = max(1, int(0.01 * self._freq))
        env = np.ones(n)
        env[:ataque] = np.linspace(0, 1, ataque)
        env *= np.exp(-3.0 * t / dur)
        return onda * env * vol

    def _para_som(self, onda: np.ndarray) -> "pygame.mixer.Sound":
        pico = np.max(np.abs(onda)) or 1.0
        onda = onda / max(1.0, pico)
        dados = (onda * 32767 * 0.8).astype(np.int16)
        if self._canais == 2:
            dados = np.column_stack((dados, dados))
        return pygame.sndarray.make_sound(np.ascontiguousarray(dados))

    def _criar_sons(self) -> None:
        for i, freq in enumerate(_NOTAS):
            self._sons[f"nota{i}"] = self._para_som(self._tom(freq, 0.45))
        # Neutro (tentativa errada): tom grave, curto e baixinho
        self._sons["neutro"] = self._para_som(
            self._tom(261.63, 0.25, vol=0.18, harmonico=0.0)
        )
        # Rodada concluída: arpejo ascendente curto
        self._sons["rodada"] = self._para_som(self._arpejo([0, 2, 3], 0.14))
        # Fase concluída: arpejo mais longo
        self._sons["fase"] = self._para_som(self._arpejo([0, 2, 3, 5], 0.2))
        # Fase não concluída: duas notas descendo suave (acolhedor)
        self._sons["tentar"] = self._para_som(
            np.concatenate(
                [
                    self._tom(_NOTAS[3], 0.25, vol=0.25),
                    self._tom(_NOTAS[1], 0.4, vol=0.25),
                ]
            )
        )

    def _arpejo(self, indices, dur_nota):
        partes = [self._tom(_NOTAS[i], dur_nota + 0.15) for i in indices]
        passo = int(self._freq * dur_nota)
        total = passo * (len(partes) - 1) + len(partes[-1])
        mix = np.zeros(total)
        for k, parte in enumerate(partes):
            ini = k * passo
            mix[ini : ini + len(parte)] += parte
        return mix

    # ====================== Reprodução ======================
    def _tocar(self, nome: str) -> None:
        if not self.disponivel or not GameSettings.SOM_LIGADO:
            return
        som = self._sons.get(nome)
        if som is not None:
            som.set_volume(GameSettings.VOLUME)
            som.play()

    def nota(self, passo: int) -> None:
        """Nota do passo ``passo`` do caminho (sobe a cada quadrado)."""
        self._tocar(f"nota{passo % len(_NOTAS)}")

    def neutro(self) -> None:
        self._tocar("neutro")

    def rodada_concluida(self) -> None:
        self._tocar("rodada")

    def fase_concluida(self) -> None:
        self._tocar("fase")

    def tentar_de_novo(self) -> None:
        self._tocar("tentar")

    def ajustar_volume(self) -> None:
        for som in self._sons.values():
            som.set_volume(GameSettings.VOLUME)
