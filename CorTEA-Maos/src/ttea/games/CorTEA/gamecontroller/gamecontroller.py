import random
from typing import Callable, Dict, List, Optional

import pygame
from ttea.games.CorTEA.gamecore import Sons
from ttea.games.CorTEA.gamemodel import (
    Atividade,
    Desempenho,
    Feedback,
    Grid,
    Sessao,
    SistemaAjuda,
    Usuario,
)
from ttea.games.CorTEA.gameui import UI
from ttea.games.CorTEA.gameutil import (
    GameSettings,
    GameState,
    GerenciadorCSV,
    formatar_tempo,
    t,
)


class GameController:
    """Controla a partida do CorTEA: fluxo das fases, rodadas, validação das
    respostas, ajuda, pontuação, registro de desempenho e desenho da cena.

    Corresponde à classe ``SistemaCorTea`` do diagrama de classes (iniciar
    sessão, encerrar sessão e ajustar a fase automaticamente).

    O tempo do jogo (``agora``) não avança enquanto o jogo está pausado, então
    nenhum cronômetro (ajuda, limite da rodada) corre durante a pausa.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        relogio: Optional[Callable[[], int]] = None,
        rng: Optional[random.Random] = None,
        sons: Optional[Sons] = None,
        diretorio_csv: Optional[str] = None,
        usuario: Optional[Usuario] = None,
    ):
        self.surface = surface
        self._relogio = relogio or pygame.time.get_ticks
        self.rng = rng or random.Random()
        self.sons = sons if sons is not None else Sons()
        self._diretorio_csv = diretorio_csv

        # Componentes principais
        self.grid = Grid()
        self.atividade = Atividade(rng=self.rng)
        self.feedback = Feedback()
        self.ajuda = SistemaAjuda()
        self.desempenho = Desempenho()
        self.usuario = usuario or Usuario.carregar(GameSettings.PLAYER_ID)
        self.sessao = Sessao(self.usuario)
        self.csv = GerenciadorCSV(self.sessao, diretorio_csv)

        # Estado do jogo
        self.estado = GameState.INICIO
        self.fase = GameSettings.FASE_INICIAL
        self.rodada = 1
        self.pontos = 0
        self.ultima_fase_concluida = False
        self.mostrar_painel = GameSettings.MOSTRAR_PAINEL
        self.mostrar_previa = GameSettings.MOSTRAR_PREVIA_CAMERA

        # Relógio do jogo (congela na pausa)
        self._pausa_acumulada = 0
        self._inicio_pausa: Optional[int] = None
        self._estado_antes_pausa: Optional[str] = None
        self._t_inicio_sessao = 0
        self._tempo_total_final = 0.0

        # Controle de tempo das telas
        self._fim_estado = 0
        self._inicio_exibicao = 0
        self._ultimo_passo_tocado = -1
        self._inicio_tentativa = 0
        self._t_ref = 0  # início do estímulo atual (p/ tempo de resposta)
        self._prazo_rodada = 0
        self._erro_indice: Optional[int] = None
        self._erro_t = 0

        # Entrada (preenchidos por quem controla a webcam / o seletor)
        self.pontos_maos: List[tuple] = []
        self.progresso_selecao: Dict[object, float] = {}
        self.camera_ativa = False

    # ====================== Relógio ======================
    def tempo_real(self) -> int:
        """Relógio que não para na pausa (usado pela seleção por mão)."""
        return self._relogio()

    @property
    def agora(self) -> int:
        """Tempo do jogo em ms (congelado durante a pausa)."""
        base = (
            self._inicio_pausa
            if self._inicio_pausa is not None
            else self._relogio()
        )
        return base - self._pausa_acumulada

    # ====================== Fluxo da sessão ======================
    @property
    def config_fase(self):
        return GameSettings.config_da_fase(self.fase)

    @property
    def passos_da_fase(self) -> int:
        """Total de quadrados a tocar numa fase completa (todas as rodadas)."""
        return self.config_fase.comprimento * GameSettings.RODADAS_POR_FASE

    def ir_para(self, estado: str) -> None:
        """Troca para uma tela de menu (início, configurações, controles)."""
        self.estado = estado

    def iniciar_jogo(self) -> None:
        """Começa a sessão a partir da tela inicial (RF01)."""
        self.sessao.iniciar()
        self._t_inicio_sessao = self.agora
        self.fase = max(1, min(GameSettings.total_fases(), self.fase))
        self._entrar_intro()

    def reiniciar(self) -> None:
        """Nova sessão do zero (botão "Reiniciar" da tela de conclusão)."""
        self._nova_sessao()
        self.iniciar_jogo()

    def voltar_ao_inicio(self) -> None:
        """Encerra a sessão atual, salvando o que ainda não foi gravado (RF13),
        e volta para a tela inicial sem fechar o jogo (botão "Sair")."""
        self._registrar_tentativa()
        self.sessao.finalizar()
        self._nova_sessao()
        self.estado = GameState.INICIO

    def _nova_sessao(self) -> None:
        """Zera sessão, relatório, pontos, fase, ajudas e pausa."""
        self.sessao = Sessao(self.usuario)
        self.csv = GerenciadorCSV(self.sessao, self._diretorio_csv)
        self.pontos = 0
        self.fase = GameSettings.FASE_INICIAL
        self.ajuda = SistemaAjuda()
        self.desempenho = Desempenho()
        self._pausa_acumulada = 0
        self._inicio_pausa = None
        self._estado_antes_pausa = None
        self._tempo_total_final = 0.0

    def encerrar(self) -> None:
        """Encerra a sessão, salvando o que ainda não foi gravado (RF13)."""
        if self.estado == GameState.ENCERRADO:
            return
        self._registrar_tentativa()
        self.sessao.finalizar()
        self.estado = GameState.ENCERRADO

    # ---- Pausa -----------------------------------------------------------
    def pausar(self) -> None:
        if self.estado not in GameState.PAUSAVEIS:
            return
        self._estado_antes_pausa = self.estado
        self._inicio_pausa = self._relogio()
        self.estado = GameState.PAUSADO

    def continuar(self) -> None:
        if self.estado != GameState.PAUSADO:
            return
        if self._inicio_pausa is not None:
            self._pausa_acumulada += self._relogio() - self._inicio_pausa
            self._inicio_pausa = None
        self.estado = self._estado_antes_pausa or GameState.JOGO
        self._estado_antes_pausa = None
        self.ajuda.reiniciar_tempo(self.agora)

    @property
    def pode_retroceder(self) -> bool:
        return self.fase > 1

    @property
    def pode_avancar(self) -> bool:
        return self.fase < GameSettings.total_fases()

    def mudar_fase(self, delta: int) -> None:
        """Terapeuta avança ou retrocede uma fase pelo menu de pausa. A fase
        é recomeçada com um caminho novo (não há "reinício" da fase atual)."""
        if self.estado != GameState.PAUSADO:
            return
        nova = self.fase + delta
        if nova < 1 or nova > GameSettings.total_fases() or delta == 0:
            return
        self._registrar_tentativa()
        self.fase = nova
        self.continuar()
        self._entrar_intro()

    def pedir_saida(self) -> None:
        """Mostra a confirmação de encerramento (a partir da pausa)."""
        if self.estado == GameState.PAUSADO:
            self.estado = GameState.CONFIRMAR_SAIDA

    def cancelar_saida(self) -> None:
        if self.estado == GameState.CONFIRMAR_SAIDA:
            self.estado = GameState.PAUSADO

    def alternar_som(self) -> None:
        GameSettings.SOM_LIGADO = not GameSettings.SOM_LIGADO

    def alternar_painel(self) -> None:
        self.mostrar_painel = not self.mostrar_painel

    def alternar_previa(self) -> None:
        self.mostrar_previa = not self.mostrar_previa

    # ---- Fases e rodadas -------------------------------------------------
    def _entrar_intro(self) -> None:
        """Mostra "FASE n" com a grade da fase (primeira rodada)."""
        self.rodada = 1
        self.desempenho = Desempenho()
        self.atividade.gerar_sequencia(self.config_fase)
        self._inicio_tentativa = self.agora
        self._fim_estado = self.agora + GameSettings.DURACAO_INTRO_FASE
        self.feedback.limpar()
        self.ajuda.reiniciar_tempo(self.agora)
        self.estado = GameState.INTRO_FASE

    def _iniciar_exibicao(self) -> None:
        """O sistema mostra o caminho aceso, quadrado por quadrado."""
        self._inicio_exibicao = self.agora
        self._ultimo_passo_tocado = -1
        self.feedback.mostrar(t("observe"), GameSettings.COR_TEXTO, self.agora, 60000)
        self.estado = GameState.MOSTRANDO

    def _iniciar_turno(self) -> None:
        """Vez do jogador reproduzir o caminho."""
        agora = self.agora
        self._t_ref = agora
        self._prazo_rodada = (
            agora + GameSettings.TEMPO_LIMITE_RODADA
            if GameSettings.TEMPO_LIMITE_RODADA > 0
            else 0
        )
        self.ajuda.reiniciar_tempo(agora)
        self.feedback.mostrar(t("sua_vez"), GameSettings.COR_TEXTO, agora)
        self.estado = GameState.JOGO

    def passo_exibido(self) -> Optional[int]:
        """Posição (no caminho) do quadrado aceso agora, ou ``None``."""
        passo_ms = self.config_fase.passo_ms
        decorrido = (
            self.agora - self._inicio_exibicao - GameSettings.ATRASO_INICIAL_EXIBICAO
        )
        if decorrido < 0:
            return None
        passo = decorrido // passo_ms
        if passo >= len(self.atividade.caminho):
            return None
        return int(passo)

    def _aceso_agora(self) -> Optional[int]:
        """Índice do quadrado aceso (some um instante entre dois passos)."""
        passo = self.passo_exibido()
        if passo is None:
            return None
        passo_ms = self.config_fase.passo_ms
        decorrido = (
            self.agora - self._inicio_exibicao - GameSettings.ATRASO_INICIAL_EXIBICAO
        )
        if (decorrido % passo_ms) > 0.8 * passo_ms:
            return None
        return self.atividade.caminho[passo]

    # ====================== Atualização por frame ======================
    def atualizar(self) -> None:
        """Avança os cronômetros e as animações da partida."""
        agora = self.agora
        estado = self.estado

        if estado == GameState.INTRO_FASE:
            if agora >= self._fim_estado:
                self._iniciar_exibicao()

        elif estado == GameState.MOSTRANDO:
            passo = self.passo_exibido()
            if passo is not None and passo != self._ultimo_passo_tocado:
                self._ultimo_passo_tocado = passo
                self.sons.nota(passo)
            fim = (
                self._inicio_exibicao
                + GameSettings.ATRASO_INICIAL_EXIBICAO
                + len(self.atividade.caminho) * self.config_fase.passo_ms
                + GameSettings.PAUSA_APOS_EXIBICAO
            )
            if agora >= fim:
                self._iniciar_turno()

        elif estado == GameState.JOGO:
            if self._prazo_rodada and agora >= self._prazo_rodada:
                self._finalizar_fase(tempo_esgotado=True)
            elif self.ajuda.verificar_inatividade(agora):
                self.ajuda.exibir_ajuda()
                self.ajuda.consumir_ajuda()
                self.pontos = self.ajuda.aplicar_penalidade(self.pontos)

        elif estado == GameState.INTERVALO:
            if agora >= self._fim_estado:
                self.rodada += 1
                self.atividade.gerar_sequencia(self.config_fase)
                self._iniciar_exibicao()

        elif estado in (
            GameState.FASE_CONCLUIDA,
            GameState.FASE_NAO_CONCLUIDA,
        ):
            if agora >= self._fim_estado:
                self._apos_resultado()

    # ====================== Resposta do jogador ======================
    def selecionar_quadrado(self, indice: int) -> None:
        """O jogador escolheu um quadrado (mão parada sobre ele ou clique)."""
        if self.estado != GameState.JOGO:
            return
        agora = self.agora
        tempo_resposta = (agora - self._t_ref) / 1000.0
        acertou = self.atividade.validar_resposta(indice)
        self.desempenho.atualizar_dados(acertou, tempo_resposta)

        if acertou:
            sequencia = self.desempenho.acertos_consecutivos
            bonus = GameSettings.BONUS_SEQUENCIA * min(
                sequencia - 1, GameSettings.BONUS_SEQUENCIA_MAX
            )
            self.pontos += GameSettings.PONTOS_ACERTO + bonus
            self.sons.nota(self.atividade.passo_atual - 1)
            self.feedback.mostrar(
                t("muito_bem"), GameSettings.COR_ACERTO, agora
            )
        else:
            self._erro_indice = indice
            self._erro_t = agora
            self.sons.neutro()
            self.feedback.mostrar(
                t("tente_outra_vez"), GameSettings.COR_ERRO, agora
            )

        self._t_ref = agora
        self.ajuda.reiniciar_tempo(agora)

        if acertou and self.atividade.concluido:
            self._rodada_concluida()

    def _rodada_concluida(self) -> None:
        if self.rodada < GameSettings.RODADAS_POR_FASE:
            self.sons.rodada_concluida()
            self.feedback.mostrar(
                t("rodada_ok"), GameSettings.COR_ACERTO, self.agora
            )
            self._fim_estado = self.agora + GameSettings.DURACAO_INTERVALO_RODADA
            self.estado = GameState.INTERVALO
        else:
            self._finalizar_fase()

    def _finalizar_fase(self, tempo_esgotado: bool = False) -> None:
        """Avalia a tentativa pelo índice de desempenho (RF09, RF12, RF14)."""
        agora = self.agora
        concluiu = not tempo_esgotado and self.desempenho.verificar_progresso(
            self.passos_da_fase
        )
        indice = self.desempenho.calcular_indice()
        self._registrar_tentativa()

        self.ultima_fase_concluida = concluiu
        if concluiu:
            self.pontos += max(0, int(indice))
            self.ajuda.conceder_ajuda()  # recompensa: +1 ajuda
            self.sons.fase_concluida()
            self.feedback.mostrar(
                t("fase_concluida"),
                GameSettings.COR_ACERTO,
                agora,
                GameSettings.DURACAO_RESULTADO_FASE,
            )
            self.estado = GameState.FASE_CONCLUIDA
        else:
            self.sons.tentar_de_novo()
            self.feedback.mostrar(
                t("vamos_de_novo"),
                GameSettings.COR_ERRO,
                agora,
                GameSettings.DURACAO_RESULTADO_FASE,
            )
            self.estado = GameState.FASE_NAO_CONCLUIDA
        self._fim_estado = agora + GameSettings.DURACAO_RESULTADO_FASE

    def _apos_resultado(self) -> None:
        if not self.ultima_fase_concluida:
            self._entrar_intro()  # repete a mesma fase
        elif self.fase >= GameSettings.total_fases():
            self._tempo_total_final = (self.agora - self._t_inicio_sessao) / 1000
            self.sessao.finalizar()
            self.estado = GameState.CONCLUSAO
        else:
            self.fase += 1
            self._entrar_intro()

    def _registrar_tentativa(self) -> None:
        """Grava no CSV a tentativa de fase em andamento, se houve respostas."""
        d = self.desempenho
        if d.total_respostas == 0:
            return
        duracao = (self.agora - self._inicio_tentativa) / 1000
        self.sessao.registrar_tentativa(duracao, d.tempos)
        try:
            self.csv.salvar_dados(
                acertos=d.acertos,
                erros=d.erros,
                acertos_consecutivos=d.melhor_sequencia,
                fase=self.fase,
                tempo_medio_resposta=d.tempo_medio_resposta,
            )
        except Exception as erro:  # nunca derrubar o jogo por causa do CSV
            print(f"Não foi possível salvar o relatório: {erro}")
        self.desempenho = Desempenho()

    def resumo(self) -> Dict[str, float]:
        """Números mostrados na tela de conclusão."""
        total = self._tempo_total_final or (
            (self.agora - self._t_inicio_sessao) / 1000
        )
        return {
            "pontos": self.pontos,
            "tempo_total": total,
            "tempo_medio_fase": self.sessao.tempo_medio_fase,
            "tempo_medio_resposta": self.sessao.tempo_medio_resposta,
        }

    # ====================== Desenho ======================
    def draw(self) -> None:
        """Desenha a cena da partida (as telas de menu ficam em ``Menu``)."""
        estado = self.estado
        self._draw_grade()
        self._draw_feedback()

        if estado == GameState.INTRO_FASE:
            self._draw_fase_grande()
        else:
            self._draw_circulo_cor()
            self._draw_placar()

        if estado == GameState.FASE_CONCLUIDA:
            for x in (50, GameSettings.SCREEN_WIDTH - 50):
                UI.icone_certo(self.surface, (x, 30))
        elif estado == GameState.FASE_NAO_CONCLUIDA:
            for x in (50, GameSettings.SCREEN_WIDTH - 50):
                UI.icone_x(self.surface, (x, 30))

        self.draw_maos()
        if self.mostrar_painel:
            self._draw_painel()

    def _draw_grade(self) -> None:
        agora = self.agora
        estado = self.estado
        aceso = self._aceso_agora() if estado == GameState.MOSTRANDO else None
        mostrando = estado == GameState.MOSTRANDO
        pisca = (agora // GameSettings.AJUDA_PISCA_MS) % 2 == 0
        esperado = (
            self.atividade.esperado
            if estado == GameState.JOGO and not self.atividade.concluido
            else None
        )

        for indice, retangulo in self.grid.quadrados:
            cor = self.atividade.cores[indice]
            cor_borda = (200, 200, 200)
            espessura_borda = 5

            if mostrando:
                if indice == aceso:
                    cor = UI.clarear_cor(cor, 0.45)
                    cor_borda = (255, 255, 255)
                    espessura_borda = 12
                else:
                    cor = UI.misturar(cor, (215, 215, 215), 0.7)
            else:
                if self.ajuda.ajuda_ativa and indice == esperado and pisca:
                    cor = UI.clarear_cor(cor, 0.4)  # Fig. 10: ajuda
                if indice in self.atividade.percorridos and estado == GameState.JOGO:
                    cor_borda = (255, 215, 0)  # borda dourada: já concluído
                    espessura_borda = 8
                if (
                    indice == self._erro_indice
                    and agora - self._erro_t < 600
                    and estado == GameState.JOGO
                ):
                    cor_borda = GameSettings.COR_ERRO
                    espessura_borda = 8

            pygame.draw.rect(self.surface, cor, retangulo, border_radius=15)
            pygame.draw.rect(
                self.surface,
                cor_borda,
                retangulo,
                espessura_borda,
                border_radius=15,
            )

            progresso = self.progresso_selecao.get(("quad", indice), 0.0)
            if progresso > 0:
                UI.anel_progresso(self.surface, retangulo.center, 34, progresso)

    def draw_maos(self) -> None:
        sobre_alvo = bool(self.progresso_selecao)
        cor = (0, 170, 70) if sobre_alvo else (30, 120, 230)
        for posicao in self.pontos_maos:
            pygame.draw.circle(self.surface, (255, 255, 255), posicao, 16)
            pygame.draw.circle(self.surface, cor, posicao, 11)

    def _draw_feedback(self) -> None:
        if self.feedback.ativo(self.agora):
            UI.draw_text(
                self.surface,
                self.feedback.mensagem,
                (GameSettings.SCREEN_WIDTH // 2, self.grid.offset_y // 2),
                self.feedback.cor,
                GameSettings.FONTS["feedback"],
            )

    def _area_inferior(self):
        """Centro e raio do círculo que fica abaixo da grade."""
        espaco_vertical = GameSettings.SCREEN_HEIGHT - (
            self.grid.offset_y + self.grid.altura
        )
        raio = max(1, (espaco_vertical - 10) // 2)
        cx = GameSettings.SCREEN_WIDTH // 2
        cy = self.grid.offset_y + self.grid.altura + 5 + raio
        return (cx, cy), raio

    def _draw_circulo_cor(self) -> None:
        """Círculo inferior: mostra a cor do caminho a seguir."""
        centro, raio = self._area_inferior()
        pygame.draw.circle(
            self.surface, self.atividade.cor_caminho, centro, raio
        )
        pygame.draw.circle(self.surface, (50, 50, 50), centro, raio, 6)

    def _draw_fase_grande(self) -> None:
        centro, _ = self._area_inferior()
        UI.draw_text(
            self.surface,
            f"{t('fase').upper()} {self.fase}",
            centro,
            (0, 0, 0),
            GameSettings.FONTS["fase"],
        )

    def _draw_placar(self) -> None:
        margem = GameSettings.MARGEM
        UI.draw_text(
            self.surface,
            f"{t('fase')}: {self.fase}",
            (margem, GameSettings.SCREEN_HEIGHT - margem),
            (0, 0, 0),
            anchor="bottomleft",
        )
        UI.draw_text(
            self.surface,
            f"{t('pontos')}: {self.pontos}",
            (
                GameSettings.SCREEN_WIDTH - margem,
                GameSettings.SCREEN_HEIGHT - margem,
            ),
            (0, 0, 0),
            anchor="bottomright",
        )

    def _draw_painel(self) -> None:
        """Painel do terapeuta (tecla H): desempenho em tempo real."""
        d = self.desempenho
        restante = 0
        if self.estado == GameState.JOGO and self._prazo_rodada:
            restante = max(0, (self._prazo_rodada - self.agora) / 1000)
        linhas = [
            (t("hud_rodada"), f"{self.rodada}/{GameSettings.RODADAS_POR_FASE}"),
            (t("hud_acertos"), str(d.acertos)),
            (t("hud_erros"), str(d.erros)),
            (
                t("hud_sequencia"),
                f"{d.acertos_consecutivos} ({d.melhor_sequencia})",
            ),
            (t("hud_indice"), f"{d.calcular_indice():.1f}"),
            (
                t("hud_ajudas"),
                f"{self.ajuda.quantidade_disponivel}/{self.ajuda.maximo_ajudas}",
            ),
            (t("hud_tempo"), formatar_tempo(restante) if restante else "-"),
        ]
        x = self.grid.offset_x + self.grid.largura + 8
        largura = GameSettings.SCREEN_WIDTH - x - 4
        altura = len(linhas) * 40 + 10
        fundo = pygame.Surface((largura, altura), pygame.SRCALPHA)
        fundo.fill((255, 255, 255, 215))
        self.surface.blit(fundo, (x, 60))
        y = 70
        for rotulo, valor in linhas:
            UI.draw_text(
                self.surface,
                rotulo,
                (x + 8, y),
                (90, 90, 90),
                GameSettings.FONTS["small"],
                anchor="topleft",
            )
            UI.draw_text(
                self.surface,
                valor,
                (x + 8, y + 17),
                GameSettings.COR_TEXTO,
                GameSettings.FONTS["small"],
                anchor="topleft",
            )
            y += 40

    # ====================== Encerramento ======================
    def close(self) -> None:
        """Libera recursos (o ``CorTEA`` fecha a webcam)."""
        self.encerrar()
