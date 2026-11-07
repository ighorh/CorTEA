import argparse
import os
import sys

import pygame
from ttea.games.CorTEA.gamecontroller import GameController
from ttea.games.CorTEA.gamecore import (
    JanelaCamera,
    Rastreamento,
    SeletorPermanencia,
)
from ttea.games.CorTEA.gameutil import GameSettings, GameState
from ttea.games.CorTEA.gameview import Menu

PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))
INI_PADRAO = os.path.join(PASTA_JOGO, "cortea.ini")
ICONE = os.path.join(PASTA_JOGO, "resources", "icons", "CorTea.png")


class CorTEA:
    """Classe principal: janela, entrada (teclado, mouse e webcam) e o loop
    do jogo. A regra do jogo fica no ``GameController``."""

    def __init__(self, argumentos=None):
        """Inicializa o jogo, a janela, os objetos e as variáveis de estado."""
        # 1. Argumentos vindos da plataforma T-TEA
        parser = argparse.ArgumentParser(description="CorTEA Exergame")
        parser.add_argument(
            "--lang", type=str, default="pt_BR", help="Idioma do app"
        )
        parser.add_argument(
            "--player_id", type=int, default=0, help="ID do Jogador"
        )
        parser.add_argument(
            "--professional_id", type=int, default=0, help="ID do Profissional"
        )
        parser.add_argument(
            "--phase", type=int, default=0, help="Fase inicial (0 = padrão)"
        )
        parser.add_argument(
            "--camera", type=int, default=0, help="Índice da webcam"
        )
        args = parser.parse_args(argumentos)

        # 2. Configurações: padrões -> cortea.ini -> argumentos da plataforma
        GameSettings.load_ini(INI_PADRAO)
        GameSettings.setup(args)

        # 3. Inicialização do Pygame
        pygame.init()
        try:  # ícone da janela e da barra de tarefas
            pygame.display.set_icon(pygame.image.load(ICONE))
        except (pygame.error, FileNotFoundError):
            pass
        tamanho = (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
        try:
            # SCALED: a janela pode ser redimensionada / tela cheia, e o jogo
            # continua desenhando em 800x600.
            self.screen = pygame.display.set_mode(
                tamanho, pygame.SCALED | pygame.RESIZABLE
            )
        except pygame.error:
            self.screen = pygame.display.set_mode(tamanho)
        pygame.display.set_caption(GameSettings.WINDOW_NAME)
        self.clock = pygame.time.Clock()
        GameSettings.load_fonts()

        # 4. Criação dos objetos principais
        self.rastreamento = Rastreamento(tamanho, GameSettings.CAMERA_INDEX)
        if self.rastreamento.motivo_inativo:
            print(
                f"[CorTEA] {self.rastreamento.motivo_inativo}: "
                "jogando apenas com o mouse."
            )
        self.janela_camera = JanelaCamera()
        self.game = GameController(self.screen)
        self.menu = Menu(self.screen)
        self.seletor = SeletorPermanencia(
            GameSettings.TEMPO_PERMANENCIA, GameSettings.TOLERANCIA_PERDA_MAO
        )
        self._estado_anterior = None
        self.running = True

    # ====================== Eventos ======================
    def handle_events(self):
        """Gerencia os eventos de entrada (teclado, mouse)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._encerrar()
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_key(self, key) -> None:
        estado = self.game.estado
        if key == pygame.K_ESCAPE:
            if estado in GameState.PAUSAVEIS:
                self.game.pausar()
            elif estado == GameState.PAUSADO:
                self.game.continuar()
            elif estado in (GameState.CONFIGURACOES, GameState.CONTROLES):
                self.game.ir_para(GameState.INICIO)
            elif estado == GameState.CONFIRMAR_SAIDA:
                self.game.cancelar_saida()
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            if estado == GameState.INICIO:
                self.game.iniciar_jogo()
            elif estado == GameState.PAUSADO:
                self.game.continuar()
            elif estado == GameState.CONCLUSAO:
                self.game.reiniciar()
        elif key == pygame.K_c:
            self.game.alternar_previa()
            self.rastreamento.gerar_previa = self.game.mostrar_previa
        elif key == pygame.K_e:
            GameSettings.ESPELHAR_CAMERA = not GameSettings.ESPELHAR_CAMERA
        elif key == pygame.K_h:
            self.game.alternar_painel()
        elif key == pygame.K_m:
            self.game.alternar_som()
        elif key == pygame.K_F11:
            pygame.display.toggle_fullscreen()

    def _handle_click(self, pos) -> None:
        """Clique do mouse: escolhe botão (menus) ou quadrado (partida)."""
        estado = self.game.estado
        if estado in GameState.MENUS:
            acao = self.menu.acao_em(estado, pos)
            if acao and self.menu.habilitado(estado, acao, self.game):
                self._executar_acao(acao, pos)
        elif estado in GameState.SELECAO_NA_GRADE:
            indice = self.game.grid.indice_em(pos)
            if indice is not None:
                self.game.selecionar_quadrado(indice)

    def _executar_acao(self, acao: str, pos=(0, 0)) -> None:
        """Executa a ação de um botão (vinda do mouse ou da mão)."""
        g = self.game
        if acao in ("volume_menos", "volume_mais", "barra_volume"):
            self.menu.ajustar_volume(acao, pos)
            g.sons.ajustar_volume()
        elif acao == "jogar":
            g.iniciar_jogo()
        elif acao == "configuracoes":
            g.ir_para(GameState.CONFIGURACOES)
        elif acao == "controles":
            g.ir_para(GameState.CONTROLES)
        elif acao == "voltar":
            g.ir_para(GameState.INICIO)
        elif acao == "som":
            g.alternar_som()
        elif acao == "continuar":
            g.continuar()
        elif acao == "retroceder":
            g.mudar_fase(-1)
        elif acao == "avancar":
            g.mudar_fase(+1)
        elif acao == "sair":
            if g.estado == GameState.PAUSADO:
                g.pedir_saida()  # pede confirmação (Quadro 6 do artigo)
            else:
                g.voltar_ao_inicio()
        elif acao == "sim":
            g.voltar_ao_inicio()
        elif acao == "nao":
            g.cancelar_saida()
        elif acao == "reiniciar":
            g.reiniciar()

    # ====================== Atualização ======================
    def update(self):
        """Atualiza a lógica do jogo a cada frame."""
        pontos = self.rastreamento.capturar_movimento()
        self.game.pontos_maos = pontos
        self.game.camera_ativa = self.rastreamento.ativo
        self._atualizar_janela_camera()
        self.game.atualizar()
        self._atualizar_selecao(pontos)
        if self.game.estado == GameState.ENCERRADO:
            self.running = False

    def _atualizar_janela_camera(self) -> None:
        """Mostra a webcam numa janela à parte (tecla C liga/desliga)."""
        if not self.game.mostrar_previa:
            self.janela_camera.fechar()
            return
        if not self.janela_camera.mostrar(self.rastreamento.obter_previa()):
            # Fechada pelo X da janela: equivale a desligar com a tecla C.
            self.game.mostrar_previa = False
            self.rastreamento.gerar_previa = False

    def _alvos_selecionaveis(self) -> dict:
        """Alvos que a mão do jogador pode selecionar na tela atual."""
        estado = self.game.estado
        if estado in GameState.SELECAO_NA_GRADE:
            return {
                ("quad", indice): retangulo
                for indice, retangulo in self.game.grid.quadrados
            }
        if estado in GameState.MENUS:
            return {
                ("acao", acao): retangulo
                for acao, retangulo in self.menu.botoes(estado).items()
                if self.menu.habilitado(estado, acao, self.game)
            }
        return {}

    def _atualizar_selecao(self, pontos) -> None:
        """Seleção por permanência da mão sobre quadrados e botões."""
        estado = self.game.estado
        if estado != self._estado_anterior:
            self.seletor.reiniciar()
            self._estado_anterior = estado

        alvos = self._alvos_selecionaveis()
        agora = self.game.tempo_real()
        escolhido = self.seletor.atualizar(agora, pontos, alvos)

        progresso = {}
        for chave in alvos:
            fracao = self.seletor.progresso(chave, agora)
            if fracao > 0:
                progresso[chave] = fracao
        self.game.progresso_selecao = progresso

        if escolhido is not None:
            tipo, valor = escolhido
            if tipo == "quad":
                self.game.selecionar_quadrado(valor)
            else:
                self._executar_acao(valor)

    # ====================== Desenho ======================
    def draw(self):
        """Desenha todos os elementos na tela."""
        if self.game.estado == GameState.ENCERRADO:
            return
        self.screen.fill(GameSettings.COR_FUNDO)

        if self.game.estado in GameState.MENUS:
            self.menu.draw(
                self.game.estado, self.game.progresso_selecao, self.game
            )
            self.game.draw_maos()
        else:
            self.game.draw()

        pygame.display.flip()

    # ====================== Loop principal ======================
    def run(self):
        """Loop principal do jogo."""
        try:
            while self.running:
                self.handle_events()
                if not self.running:
                    break
                self.update()
                if not self.running:
                    break
                self.draw()
                self.clock.tick(GameSettings.FPS)
        finally:
            self.cleanup()
        sys.exit()

    def _encerrar(self) -> None:
        self.game.encerrar()
        self.running = False

    def cleanup(self):
        """Libera a webcam, fecha o Pygame e informa onde o CSV foi salvo."""
        self.game.encerrar()  # salva a tentativa em andamento, se houver
        self.janela_camera.fechar()
        self.rastreamento.close()
        pygame.quit()

        print("\n--- RESUMO DA SESSÃO ---")
        caminho = self.game.csv.caminho_arquivo
        if caminho:
            print(f"Relatório salvo com sucesso em: {caminho}")
            print(f"Tentativas de fase registradas: {len(self.game.csv.linhas)}")
        else:
            print("Nenhuma jogada foi registrada.")


# ====================== EXECUÇÃO DO JOGO ======================
if __name__ == "__main__":
    cortea = CorTEA()
    cortea.run()
