import math
from typing import Dict, Optional

import pygame
from ttea.games.CorTEA.gameui import UI
from ttea.games.CorTEA.gameview.fundoinicio import FundoInicio
from ttea.games.CorTEA.gameutil import (
    GameSettings,
    GameState,
    formatar_tempo,
    t,
)


class Menu:
    """Desenha e trata cliques de todas as telas fora da partida: início,
    configurações, controles, pausa, confirmação de saída e conclusão.

    Cada tela é um conjunto de botões identificados por uma *ação* (texto
    curto como ``"jogar"``). O mesmo conjunto serve ao mouse (clique) e à
    mão do jogador (permanência sobre o botão).
    """

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self._centro = GameSettings.SCREEN_WIDTH // 2
        self._botoes = self._criar_botoes()
        self._fundo: Optional[FundoInicio] = None  # criado na 1ª exibição
        self.barra_volume = pygame.Rect(285, 270, 230, 50)

    def _criar_botoes(self) -> Dict[str, Dict[str, pygame.Rect]]:
        cx = self._centro
        altura = GameSettings.SCREEN_HEIGHT
        R = pygame.Rect
        return {
            # Botões no alto: o tabuleiro 3D do fundo ocupa a parte de baixo
            GameState.INICIO: {
                "jogar": R(cx - 125, 154, 250, 56),
                "configuracoes": R(cx - 220, 226, 210, 46),
                "controles": R(cx + 10, 226, 210, 46),
            },
            GameState.CONFIGURACOES: {
                "volume_menos": R(230, 270, 55, 50),
                "volume_mais": R(515, 270, 55, 50),
                "som": R(cx - 105, 385, 210, 46),
                "voltar": R(cx - 105, altura - 85, 210, 46),
            },
            GameState.CONTROLES: {
                "voltar": R(cx - 105, altura - 85, 210, 46),
            },
            # Pausa (Fig. 16 do artigo): cruz com Continuar em cima
            GameState.PAUSADO: {
                "continuar": R(cx - 100, 250, 200, 50),
                "retroceder": R(cx - 305, 310, 200, 50),
                "avancar": R(cx + 105, 310, 200, 50),
                "sair": R(cx - 100, 370, 200, 50),
                "som": R(20, 20, 190, 44),
                "volume_menos": R(20, 76, 55, 40),
                "volume_mais": R(155, 76, 55, 40),
            },
            GameState.CONFIRMAR_SAIDA: {
                "sim": R(cx - 215, 330, 190, 56),
                "nao": R(cx + 25, 330, 190, 56),
            },
            # Conclusão (Fig. 17): Sair à esquerda, Reiniciar à direita
            GameState.CONCLUSAO: {
                "sair": R(70, altura - 100, 190, 52),
                "reiniciar": R(GameSettings.SCREEN_WIDTH - 260, altura - 100, 190, 52),
            },
        }

    # ====================== Botões / cliques ======================
    def botoes(self, estado: str) -> Dict[str, pygame.Rect]:
        """Ação -> retângulo de cada botão da tela."""
        return self._botoes.get(estado, {})

    def habilitado(self, estado: str, acao: str, controle) -> bool:
        """Retroceder/Avançar ficam apagados nas fases das pontas."""
        if estado == GameState.PAUSADO:
            if acao == "retroceder":
                return controle.pode_retroceder
            if acao == "avancar":
                return controle.pode_avancar
        return True

    def acao_em(self, estado: str, pos: tuple) -> Optional[str]:
        """Ação do botão sob ``pos`` (ou ``"barra_volume"``), ou ``None``."""
        for acao, retangulo in self.botoes(estado).items():
            if retangulo.collidepoint(pos):
                return acao
        if estado == GameState.CONFIGURACOES and self.barra_volume.collidepoint(pos):
            return "barra_volume"
        return None

    def ajustar_volume(self, acao: str, pos: tuple = (0, 0)) -> None:
        """Aplica uma ação de volume e avisa os sons."""
        if acao == "volume_menos":
            GameSettings.VOLUME = max(0.0, GameSettings.VOLUME - 0.1)
        elif acao == "volume_mais":
            GameSettings.VOLUME = min(1.0, GameSettings.VOLUME + 0.1)
        elif acao == "barra_volume":
            GameSettings.VOLUME = max(
                0.0,
                min(
                    1.0,
                    (pos[0] - self.barra_volume.left) / self.barra_volume.width,
                ),
            )
        GameSettings.VOLUME = round(GameSettings.VOLUME, 2)

    # ====================== Desenho ======================
    def draw(
        self,
        estado: str,
        progresso: Optional[Dict[object, float]] = None,
        controle=None,
    ) -> None:
        """Desenha a tela do ``estado``. ``progresso`` traz a permanência da
        mão sobre cada botão e ``controle`` é o ``GameController``."""
        self._progresso = progresso or {}
        self._controle = controle
        if estado == GameState.INICIO:
            self._draw_inicio()
        elif estado == GameState.CONFIGURACOES:
            self._draw_configuracoes()
        elif estado == GameState.CONTROLES:
            self._draw_controles()
        elif estado == GameState.PAUSADO:
            self._draw_pausado()
        elif estado == GameState.CONFIRMAR_SAIDA:
            self._draw_confirmar()
        elif estado == GameState.CONCLUSAO:
            self._draw_conclusao()

    def _botao(self, estado: str, acao: str, texto: str) -> None:
        habilitado = True
        if self._controle is not None:
            habilitado = self.habilitado(estado, acao, self._controle)
        UI.button(
            self.surface,
            self.botoes(estado)[acao],
            texto,
            progresso=self._progresso.get(("acao", acao), 0.0),
            habilitado=habilitado,
        )

    def _draw_inicio(self) -> None:
        """Tela inicial: uma fase do jogo em 3D ao fundo (``FundoInicio``),
        título com letras coloridas em relevo e os botões."""
        agora = pygame.time.get_ticks()
        if self._fundo is None:
            self._fundo = FundoInicio(self.surface)
        self._fundo.draw(agora)

        self._draw_titulo_3d(agora)
        UI.draw_text(
            self.surface,
            t("subtitulo"),
            (self._centro, 128),
            (235, 235, 250),
        )
        self._botao(GameState.INICIO, "jogar", t("jogar"))
        self._botao(GameState.INICIO, "configuracoes", t("configuracoes"))
        self._botao(GameState.INICIO, "controles", t("controles"))

    def _draw_titulo_3d(self, agora: int) -> None:
        """Título com cada letra de uma cor da paleta, extrudada em 3D e
        balançando de leve, como blocos da grade."""
        fonte = GameSettings.FONTS["fase"]
        letras = list(GameSettings.GAME_TITLE)
        larguras = [fonte.size(letra)[0] for letra in letras]
        x = self._centro - sum(larguras) / 2
        profundidade = 9
        for i, (letra, largura) in enumerate(zip(letras, larguras)):
            cor = GameSettings.PALETA[i % len(GameSettings.PALETA)]
            y = 62 + 5 * math.sin(agora / 380 + i * 0.7)
            sombra = fonte.render(letra, True, UI.misturar(cor, (0, 0, 0), 0.6))
            for d in range(profundidade, 0, -1):
                self.surface.blit(sombra, sombra.get_rect(midleft=(x + d * 0.6, y + d)))
            contorno = fonte.render(letra, True, (255, 255, 255))
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                self.surface.blit(contorno, contorno.get_rect(midleft=(x + dx, y + dy)))
            face = fonte.render(letra, True, cor)
            self.surface.blit(face, face.get_rect(midleft=(x, y)))
            x += largura

    def _draw_configuracoes(self) -> None:
        """Tela de configurações: volume e som ligado/desligado."""
        e = GameState.CONFIGURACOES
        cor_texto = GameSettings.COR_TEXTO

        UI.draw_text(
            self.surface,
            t("configuracoes"),
            (self._centro, 125),
            cor_texto,
            GameSettings.FONTS["title"],
        )
        UI.draw_text(
            self.surface,
            t("volume"),
            (self._centro, 225),
            cor_texto,
            GameSettings.FONTS["feedback"],
        )

        self._botao(e, "volume_menos", "-")
        self._botao(e, "volume_mais", "+")

        pygame.draw.rect(
            self.surface, (205, 205, 205), self.barra_volume, border_radius=10
        )
        preenchimento = pygame.Rect(
            self.barra_volume.left,
            self.barra_volume.top,
            int(self.barra_volume.width * GameSettings.VOLUME),
            self.barra_volume.height,
        )
        pygame.draw.rect(
            self.surface, (75, 75, 75), preenchimento, border_radius=10
        )
        UI.draw_text(
            self.surface,
            f"{round(GameSettings.VOLUME * 100)}%",
            (self._centro, 350),
            cor_texto,
        )
        self._botao(
            e,
            "som",
            t("som_ligado") if GameSettings.SOM_LIGADO else t("som_desligado"),
        )
        self._botao(e, "voltar", t("voltar"))

    def _draw_controles(self) -> None:
        """Desenha as teclas e suas funções."""
        cor_texto = GameSettings.COR_TEXTO
        UI.draw_text(
            self.surface,
            t("controles"),
            (self._centro, 100),
            cor_texto,
            GameSettings.FONTS["title"],
        )
        teclas = [
            ("ESC", t("ctrl_pausar")),
            ("ENTER", t("ctrl_iniciar")),
            ("C", t("ctrl_camera")),
            ("E", t("ctrl_espelhar")),
            ("H", t("ctrl_painel")),
            ("M", t("ctrl_som")),
            ("F11", t("ctrl_tela")),
        ]
        y = 152
        for rotulo, descricao in teclas:
            UI.key(self.surface, (200, y, 130, 40), rotulo)
            UI.draw_text(
                self.surface,
                descricao,
                (360, y + 20),
                cor_texto,
                anchor="midleft",
            )
            y += 48
        self._botao(GameState.CONTROLES, "voltar", t("voltar"))

    def _draw_pausado(self) -> None:
        """Tela de pausa (Fig. 16): Continuar, Retroceder, Avançar, Sair."""
        e = GameState.PAUSADO
        self.surface.fill((235, 235, 235))
        UI.draw_text(
            self.surface,
            GameSettings.GAME_TITLE,
            (self._centro, 135),
            (0, 0, 0),
            GameSettings.FONTS["title"],
        )
        if self._controle is not None:
            UI.draw_text(
                self.surface,
                f"{t('pausado')} - {t('fase')} {self._controle.fase}",
                (self._centro, 205),
                GameSettings.COR_TEXTO,
                GameSettings.FONTS["feedback"],
            )
        self._botao(e, "continuar", t("continuar"))
        self._botao(e, "retroceder", t("retroceder"))
        self._botao(e, "avancar", t("avancar"))
        self._botao(e, "sair", t("sair"))
        self._botao(
            e,
            "som",
            t("som_ligado") if GameSettings.SOM_LIGADO else t("som_desligado"),
        )
        self._botao(e, "volume_menos", "-")
        self._botao(e, "volume_mais", "+")
        UI.draw_text(
            self.surface,
            f"{round(GameSettings.VOLUME * 100)}%",
            (115, 96),
            GameSettings.COR_TEXTO,
        )

    def _draw_confirmar(self) -> None:
        e = GameState.CONFIRMAR_SAIDA
        self.surface.fill((235, 235, 235))
        UI.draw_text(
            self.surface,
            t("confirmar_sair"),
            (self._centro, 250),
            GameSettings.COR_TEXTO,
            GameSettings.FONTS["feedback"],
        )
        self._botao(e, "sim", t("sim"))
        self._botao(e, "nao", t("nao"))

    def _draw_conclusao(self) -> None:
        """Tela de conclusão (Fig. 17): troféu e resumo da sessão."""
        e = GameState.CONCLUSAO
        self.surface.fill((245, 245, 245))
        UI.draw_text(
            self.surface,
            t("parabens"),
            (self._centro, 70),
            (0, 0, 0),
            GameSettings.FONTS["feedback"],
        )
        UI.trofeu(self.surface, (200, 270), 1.5)

        resumo = self._controle.resumo() if self._controle is not None else {}
        linhas = [
            (f"{t('total_pontos')}: {int(resumo.get('pontos', 0))}", "feedback"),
            (
                f"{t('tempo_total')}: "
                f"{formatar_tempo(resumo.get('tempo_total', 0))}",
                "text",
            ),
            (
                f"{t('tempo_medio_fase')}: "
                f"{formatar_tempo(resumo.get('tempo_medio_fase', 0))}",
                "text",
            ),
            (
                f"{t('tempo_medio_resposta')}: "
                f"{resumo.get('tempo_medio_resposta', 0):.1f} s",
                "text",
            ),
        ]
        y = 200
        for texto, fonte in linhas:
            UI.draw_text(
                self.surface,
                texto,
                (360, y),
                GameSettings.COR_TEXTO,
                GameSettings.FONTS[fonte],
                anchor="midleft",
            )
            y += 52 if fonte == "feedback" else 42
        self._botao(e, "sair", t("sair"))
        self._botao(e, "reiniciar", t("reiniciar"))
