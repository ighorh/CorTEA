"""Testes do jogo CorTEA.

Cobrem a lógica descrita no artigo (caminho de cores, índice de desempenho,
ajudas, progressão de fases, CSV) e percorrem o desenho de todas as telas.

Usam o pygame de verdade quando ele está instalado (com driver de vídeo e de
áudio "dummy", sem abrir janela) e, se não estiver, um pygame falso mínimo.
"""

import csv
import os
import random
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def _instalar_pygame_falso():
    """pygame mínimo para rodar os testes onde o pygame não está instalado."""

    class Rect:
        def __init__(self, *args):
            if len(args) == 1:
                args = tuple(args[0])
            if len(args) == 2:
                (x, y), (w, h) = args
            else:
                x, y, w, h = args
            self.left, self.top, self.width, self.height = x, y, w, h

        @property
        def right(self):
            return self.left + self.width

        @property
        def bottom(self):
            return self.top + self.height

        @property
        def center(self):
            return (self.left + self.width // 2, self.top + self.height // 2)

        def collidepoint(self, *ponto):
            x, y = ponto[0] if len(ponto) == 1 else ponto
            return (
                self.left <= x < self.right and self.top <= y < self.bottom
            )

        def move(self, dx, dy):
            return Rect(self.left + dx, self.top + dy, self.width, self.height)

        def inflate(self, dx, dy):
            return Rect(
                self.left - dx // 2,
                self.top - dy // 2,
                self.width + dx,
                self.height + dy,
            )

    pg = MagicMock(name="pygame")
    pg.Rect = Rect
    pg.error = Exception
    pg.mouse.get_pos = lambda: (0, 0)
    pg.time.get_ticks = lambda: 0
    pg.SRCALPHA = 65536
    sys.modules["pygame"] = pg
    return pg


try:
    import pygame  # noqa: F401

    PYGAME_REAL = True
except ImportError:
    pygame = _instalar_pygame_falso()
    PYGAME_REAL = False

from ttea.games.CorTEA.gamecore import Rastreamento, SeletorPermanencia
from ttea.games.CorTEA.gamecontroller import GameController
from ttea.games.CorTEA.gameui import UI
from ttea.games.CorTEA.gamemodel import (
    Atividade,
    Desempenho,
    Grid,
    Sessao,
    SistemaAjuda,
    Usuario,
)
from ttea.games.CorTEA.gameutil import (
    GameSettings,
    GameState,
    GerenciadorCSV,
    formatar_tempo,
    t,
)
from ttea.games.CorTEA.gameview import Menu


class Relogio:
    """Relógio falso (ms) para simular o tempo sem esperar."""

    def __init__(self):
        self.ms = 1000

    def __call__(self):
        return self.ms


def _preparar_pygame_real():
    if PYGAME_REAL:
        pygame.init()
        GameSettings.load_fonts()
        return pygame.display.set_mode(
            (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)
        )
    GameSettings.FONTS = {
        n: MagicMock()
        for n in ("small", "text", "feedback", "title", "fase")
    }
    return MagicMock(name="screen")


class SemSom:
    """Substitui ``Sons``, registrando o que seria tocado."""

    def __init__(self):
        self.tocados = []

    def nota(self, passo):
        self.tocados.append(("nota", passo))

    def neutro(self):
        self.tocados.append(("neutro",))

    def rodada_concluida(self):
        self.tocados.append(("rodada",))

    def fase_concluida(self):
        self.tocados.append(("fase",))

    def tentar_de_novo(self):
        self.tocados.append(("tentar",))

    def ajustar_volume(self):
        pass


class TesteBase(unittest.TestCase):
    def setUp(self):
        self._salvo = {
            k: getattr(GameSettings, k)
            for k in (
                "SOM_LIGADO",
                "VOLUME",
                "FASE_INICIAL",
                "RODADAS_POR_FASE",
                "CURRENT_LANG",
                "TEMPO_LIMITE_RODADA",
                "AJUDAS_INICIAIS",
            )
        }
        GameSettings.CURRENT_LANG = "pt_BR"

    def tearDown(self):
        for k, v in self._salvo.items():
            setattr(GameSettings, k, v)


# ======================================================================
# Atividade: geração do caminho de cores
# ======================================================================
class TesteAtividade(TesteBase):
    def test_caminho_valido_em_todas_as_fases(self):
        colunas = GameSettings.COLUNAS
        for config in GameSettings.FASES:
            for semente in range(150):
                a = Atividade(rng=random.Random(semente))
                caminho = a.gerar_sequencia(config)
                self.assertEqual(len(caminho), config.comprimento)
                self.assertEqual(len(set(caminho)), len(caminho))
                # começa na linha de baixo e termina na de cima
                self.assertGreaterEqual(caminho[0], (GameSettings.LINHAS - 1) * colunas)
                self.assertLess(caminho[-1], colunas)
                # cada passo vai para um vizinho (cima/baixo/esquerda/direita)
                for ant, prox in zip(caminho, caminho[1:]):
                    (l1, c1), (l2, c2) = divmod(ant, colunas), divmod(prox, colunas)
                    self.assertEqual(abs(l1 - l2) + abs(c1 - c2), 1)

    def test_cores_e_iscas(self):
        for config in GameSettings.FASES:
            for semente in range(60):
                a = Atividade(rng=random.Random(semente))
                a.gerar_sequencia(config)
                da_cor = [
                    i for i, c in enumerate(a.cores) if c == a.cor_caminho
                ]
                # quadrados da cor do caminho = caminho + iscas, nada mais
                self.assertEqual(
                    sorted(da_cor), sorted(a.caminho + a.iscas)
                )
                self.assertEqual(len(a.iscas), config.n_iscas)
                self.assertTrue(all(i not in a.caminho for i in a.iscas))
                # número de cores na grade respeita a fase
                self.assertLessEqual(len(set(a.cores)), config.n_cores)

    def test_cor_do_caminho_muda_entre_rodadas(self):
        a = Atividade(rng=random.Random(1))
        config = GameSettings.config_da_fase(1)
        anterior = None
        for _ in range(30):
            a.gerar_sequencia(config)
            self.assertNotEqual(a.cor_caminho, anterior)
            anterior = a.cor_caminho

    def test_validar_resposta(self):
        a = Atividade(rng=random.Random(3))
        a.gerar_sequencia(GameSettings.config_da_fase(1))
        primeiro, segundo = a.caminho[0], a.caminho[1]

        # errar não avança nem zera o progresso
        self.assertFalse(a.validar_resposta(segundo))
        self.assertEqual(a.passo_atual, 0)
        self.assertTrue(a.validar_resposta(primeiro))
        self.assertEqual(a.passo_atual, 1)
        self.assertEqual(a.percorridos, [primeiro])
        self.assertFalse(a.validar_resposta(primeiro))  # voltar atrás = erro
        self.assertEqual(a.passo_atual, 1)

        for indice in a.caminho[1:]:
            self.assertFalse(a.concluido)
            self.assertTrue(a.validar_resposta(indice))
        self.assertTrue(a.concluido)
        self.assertFalse(a.validar_resposta(0))


# ======================================================================
# Desempenho: Equação 1 do artigo
# ======================================================================
class TesteDesempenho(TesteBase):
    def test_equacao_1(self):
        d = Desempenho()
        for acertou in [True, True, True, False, True]:
            d.atualizar_dados(acertou, 1.0)
        # A=4, E=1, C(maior sequência)=3 -> 4*2 - 1*1 + 3*1,5 = 11,5
        self.assertEqual((d.acertos, d.erros, d.melhor_sequencia), (4, 1, 3))
        self.assertAlmostEqual(d.calcular_indice(), 11.5)

    def test_sequencia_zera_no_erro_mas_melhor_fica(self):
        d = Desempenho()
        for acertou in [True, True, False, True]:
            d.atualizar_dados(acertou, 0.5)
        self.assertEqual(d.acertos_consecutivos, 1)
        self.assertEqual(d.melhor_sequencia, 2)

    def test_tempo_medio_so_conta_acertos(self):
        d = Desempenho()
        d.atualizar_dados(True, 1.0)
        d.atualizar_dados(False, 9.0)
        d.atualizar_dados(True, 3.0)
        self.assertAlmostEqual(d.tempo_medio_resposta, 2.0)
        self.assertEqual(Desempenho().tempo_medio_resposta, 0.0)

    def test_progresso_exige_id_minimo(self):
        total = 10  # passos da fase
        perfeito = Desempenho()
        for _ in range(total):
            perfeito.atualizar_dados(True, 1)
        self.assertAlmostEqual(
            perfeito.calcular_indice(), Desempenho.indice_maximo(total)
        )
        self.assertTrue(perfeito.verificar_progresso(total))

        # 1 erro no meio: ainda passa
        bom = Desempenho()
        for acertou in [True] * 5 + [False] + [True] * 5:
            bom.atualizar_dados(acertou, 1)
        self.assertTrue(bom.verificar_progresso(total))

        # muitos erros seguidos: repete a fase
        ruim = Desempenho()
        for acertou in [True, False, False, True, False, False, True, True, False, True, True, False, False]:
            ruim.atualizar_dados(acertou, 1)
        self.assertFalse(ruim.verificar_progresso(total))

        # sem nenhum acerto nunca avança
        self.assertFalse(Desempenho().verificar_progresso(total))


# ======================================================================
# SistemaAjuda
# ======================================================================
class TesteSistemaAjuda(TesteBase):
    def test_ajuda_por_inatividade(self):
        s = SistemaAjuda(quantidade=2, maximo=3, tempo_limite_inatividade=5000, penalidade=2)
        s.reiniciar_tempo(0)
        self.assertFalse(s.verificar_inatividade(4999))
        self.assertTrue(s.verificar_inatividade(5000))
        s.exibir_ajuda()
        s.consumir_ajuda()
        self.assertTrue(s.ajuda_ativa)
        self.assertEqual(s.quantidade_disponivel, 1)
        # com a ajuda na tela não pede outra
        self.assertFalse(s.verificar_inatividade(20000))
        # qualquer ação apaga a ajuda e zera o tempo
        s.reiniciar_tempo(20000)
        self.assertFalse(s.ajuda_ativa)
        self.assertFalse(s.verificar_inatividade(24000))
        self.assertTrue(s.verificar_inatividade(25000))

    def test_sem_ajudas_nao_oferece(self):
        s = SistemaAjuda(quantidade=1, maximo=3, tempo_limite_inatividade=1000)
        s.reiniciar_tempo(0)
        s.exibir_ajuda()
        s.consumir_ajuda()
        s.reiniciar_tempo(0)
        self.assertFalse(s.possui_ajuda_disponivel())
        self.assertFalse(s.verificar_inatividade(999999))
        s.consumir_ajuda()  # nunca fica negativo
        self.assertEqual(s.quantidade_disponivel, 0)

    def test_penalidade_nao_deixa_pontos_negativos(self):
        s = SistemaAjuda(penalidade=2)
        self.assertEqual(s.aplicar_penalidade(10), 8)
        self.assertEqual(s.aplicar_penalidade(1), 0)

    def test_recompensa_respeita_o_maximo(self):
        s = SistemaAjuda(quantidade=2, maximo=3)
        self.assertTrue(s.conceder_ajuda())
        self.assertFalse(s.conceder_ajuda())
        self.assertEqual(s.quantidade_disponivel, 3)


# ======================================================================
# Seleção por permanência da mão
# ======================================================================
class TesteSeletor(TesteBase):
    def setUp(self):
        super().setUp()
        self.alvos = {
            "a": pygame.Rect(0, 0, 100, 100),
            "b": pygame.Rect(200, 0, 100, 100),
        }

    def test_seleciona_depois_do_tempo(self):
        s = SeletorPermanencia(700)
        self.assertIsNone(s.atualizar(0, [(50, 50)], self.alvos))
        self.assertIsNone(s.atualizar(699, [(50, 50)], self.alvos))
        self.assertAlmostEqual(s.progresso("a", 350), 0.5, places=1)
        self.assertEqual(s.atualizar(700, [(50, 50)], self.alvos), "a")

    def test_so_atravessar_nao_seleciona(self):
        s = SeletorPermanencia(700)
        self.assertIsNone(s.atualizar(0, [(50, 50)], self.alvos))
        self.assertIsNone(s.atualizar(300, [(150, 50)], self.alvos))  # saiu
        self.assertIsNone(s.atualizar(600, [(250, 50)], self.alvos))
        self.assertIsNone(s.atualizar(1000, [(150, 50)], self.alvos))
        self.assertEqual(s.progresso("a", 1000), 0.0)

    def test_nao_repete_ate_a_mao_sair(self):
        s = SeletorPermanencia(700)
        s.atualizar(0, [(50, 50)], self.alvos)
        self.assertEqual(s.atualizar(700, [(50, 50)], self.alvos), "a")
        self.assertIsNone(s.atualizar(2000, [(50, 50)], self.alvos))
        s.atualizar(2100, [], self.alvos)  # mão saiu
        s.atualizar(2200, [(50, 50)], self.alvos)
        self.assertEqual(s.atualizar(2900, [(50, 50)], self.alvos), "a")

    def test_tolerancia_a_falha_de_deteccao(self):
        s = SeletorPermanencia(700, tolerancia_ms=250)
        s.atualizar(0, [(50, 50)], self.alvos)
        s.atualizar(200, [], self.alvos)  # a webcam piscou (< tolerância)
        s.atualizar(300, [(50, 50)], self.alvos)  # voltou
        self.assertEqual(s.atualizar(700, [(50, 50)], self.alvos), "a")

        # sumiu por mais que a tolerância: a contagem recomeça
        s.reiniciar()
        s.atualizar(0, [(50, 50)], self.alvos)
        s.atualizar(400, [], self.alvos)
        s.atualizar(500, [(50, 50)], self.alvos)
        self.assertIsNone(s.atualizar(700, [(50, 50)], self.alvos))

    def test_sem_tolerancia_a_contagem_reinicia(self):
        s = SeletorPermanencia(700, tolerancia_ms=0)
        s.atualizar(0, [(50, 50)], self.alvos)
        s.atualizar(300, [], self.alvos)
        self.assertIsNone(s.atualizar(700, [(50, 50)], self.alvos))

    def test_duas_maos_alvos_independentes(self):
        s = SeletorPermanencia(700)
        maos = [(50, 50), (250, 50)]
        s.atualizar(0, maos, self.alvos)
        escolhido = s.atualizar(700, maos, self.alvos)
        self.assertEqual(escolhido, "a")
        self.assertEqual(s.atualizar(701, maos, self.alvos), "b")


# ======================================================================
# Rastreamento (sem webcam)
# ======================================================================
class TesteRastreamento(TesteBase):
    def setUp(self):
        super().setUp()
        self.r = Rastreamento((800, 600), indice_camera=99)

    def tearDown(self):
        self.r.close()
        super().tearDown()

    def test_sem_webcam_o_jogo_segue_com_o_mouse(self):
        self.assertFalse(self.r.ativo)
        self.assertEqual(self.r.capturar_movimento(), [])
        self.assertTrue(self.r.motivo_inativo)
        self.assertIsNone(self.r.obter_previa())

    def test_mapeamento_com_margem(self):
        m = GameSettings.MARGEM_CAMERA
        self.assertEqual(self.r.mapear(m, m), (0, 0))
        self.assertEqual(self.r.mapear(1 - m, 1 - m), (799, 599))
        self.assertEqual(self.r.mapear(0.5, 0.5), (400, 300))
        self.assertEqual(self.r.mapear(0.0, 1.0), (0, 599))  # limitado à tela

    def test_ponto_da_mao(self):
        def lm(x, y):
            return types.SimpleNamespace(x=x, y=y)

        marcos = [lm(0.0, 0.0)] * 21
        marcos[0] = lm(0.4, 0.6)
        marcos[5] = lm(0.5, 0.5)
        marcos[9] = lm(0.5, 0.4)
        marcos[13] = lm(0.5, 0.5)
        marcos[17] = lm(0.6, 0.6)
        marcos[8] = lm(0.45, 0.2)
        resultado = types.SimpleNamespace(
            multi_hand_landmarks=[types.SimpleNamespace(landmark=marcos)]
        )
        antigo = GameSettings.PONTO_DA_MAO
        try:
            GameSettings.PONTO_DA_MAO = "palma"
            (x, y), = self.r._extrair_pontos(resultado)
            self.assertAlmostEqual(x, 0.5)
            self.assertAlmostEqual(y, 0.52)
            GameSettings.PONTO_DA_MAO = "indicador"
            self.assertEqual(self.r._extrair_pontos(resultado), [(0.45, 0.2)])
        finally:
            GameSettings.PONTO_DA_MAO = antigo
        vazio = types.SimpleNamespace(multi_hand_landmarks=None)
        self.assertEqual(self.r._extrair_pontos(vazio), [])

    def test_suavizacao_reduz_o_tremor_e_aceita_salto(self):
        self.assertEqual(self.r._suavizar([(100, 100)]), [(100, 100)])
        suave = self.r._suavizar([(120, 100)])[0]
        self.assertTrue(100 < suave[0] < 120)
        # mão nova longe da anterior: não é "arrastada" para a antiga
        self.assertEqual(self.r._suavizar([(700, 500)]), [(700, 500)])


# ======================================================================
# Rastreamento com webcam e MediaPipe simulados (thread de captura)
# ======================================================================
class TesteRastreamentoSimulado(TesteBase):
    """Roda a thread de captura de verdade, mas com uma câmera e um
    detector de mãos falsos (não depende de webcam nem do MediaPipe)."""

    def test_thread_entrega_pontos_e_previa(self):
        import time

        import numpy as np
        from ttea.games.CorTEA.gamecore import rastreamento as modulo

        class CameraFalsa:
            aberta = True

            def __init__(self, indice):
                self.liberada = False

            def ler(self):
                time.sleep(0.005)
                return True, np.zeros((480, 640, 3), np.uint8)

            def close_camera(self):
                self.liberada = True
                self.aberta = False

        class MaosFalsas:
            fechada = False

            def __init__(self, **kwargs):
                pass

            def process(self, rgb):
                marcos = [types.SimpleNamespace(x=0.5, y=0.5)] * 21
                mao = types.SimpleNamespace(landmark=marcos)
                return types.SimpleNamespace(multi_hand_landmarks=[mao])

            def close(self):
                MaosFalsas.fechada = True

        originais = (modulo._mp_hands, modulo._mp_drawing, modulo.Camera)
        modulo._mp_hands = types.SimpleNamespace(
            Hands=MaosFalsas, HAND_CONNECTIONS=None
        )
        modulo._mp_drawing = types.SimpleNamespace(
            draw_landmarks=lambda *a, **k: None
        )
        modulo.Camera = CameraFalsa
        antigo = GameSettings.MOSTRAR_PREVIA_CAMERA
        GameSettings.MOSTRAR_PREVIA_CAMERA = True
        try:
            r = Rastreamento((800, 600))
            camera = r.camera
            for _ in range(200):
                if r.ativo and r.capturar_movimento():
                    break
                time.sleep(0.01)

            self.assertTrue(r.ativo)
            self.assertEqual(r.capturar_movimento(), [(400, 300)])
            self.assertEqual(r.posicao_usuario, (400, 300))
            self.assertEqual(r.obter_previa().shape, (480, 640, 3))
            grade = Grid()
            self.assertEqual(r.detectar_posicao(grade), grade.indice_em((400, 300)))

            r.close()
            self.assertTrue(MaosFalsas.fechada)
            self.assertTrue(camera.liberada)
            self.assertFalse(r._thread.is_alive())
        finally:
            modulo._mp_hands, modulo._mp_drawing, modulo.Camera = originais
            GameSettings.MOSTRAR_PREVIA_CAMERA = antigo


class TesteSons(TesteBase):
    def test_gera_todos_os_sons(self):
        from ttea.games.CorTEA.gamecore import Sons

        sons = Sons.__new__(Sons)
        sons.disponivel = True
        sons._freq, sons._canais, sons._sons = 44100, 2, {}
        if PYGAME_REAL:
            try:
                pygame.mixer.init(44100, -16, 2, 512)
            except Exception:
                self.skipTest("sem dispositivo de áudio")
        sons._criar_sons()
        self.assertEqual(len(sons._sons), 8 + 4)

        # a onda de uma nota fica dentro do intervalo e termina suave
        onda = sons._tom(523.25, 0.45)
        self.assertLessEqual(abs(onda).max(), 1.0)
        self.assertLess(abs(onda[-1]), 0.05)
        self.assertAlmostEqual(len(onda) / 44100, 0.45, places=2)

        # reprodução: respeita "som desligado" e não quebra
        GameSettings.SOM_LIGADO = False
        sons.nota(0)
        GameSettings.SOM_LIGADO = True
        sons.nota(0)
        sons.nota(99)  # além da escala: dá a volta
        sons.neutro()
        sons.rodada_concluida()
        sons.fase_concluida()
        sons.tentar_de_novo()
        sons.ajustar_volume()


# ======================================================================
# CSV (Tabela 2 do artigo)
# ======================================================================
class TesteCSV(TesteBase):
    def test_campos_e_linhas(self):
        with tempfile.TemporaryDirectory() as pasta:
            sessao = Sessao(Usuario(7, "Maria"))
            g = GerenciadorCSV(sessao, pasta)
            self.assertIsNone(g.exportar_csv())  # sem dados, sem arquivo

            g.salvar_dados(10, 2, 6, 1, 1.234)
            g.salvar_dados(8, 0, 8, 2, 0.9)
            self.assertTrue(os.path.isfile(g.caminho_arquivo))

            with open(g.caminho_arquivo, encoding="utf-8-sig", newline="") as f:
                linhas = list(csv.DictReader(f, delimiter=";"))
            self.assertEqual(
                list(linhas[0].keys()),
                [
                    "id_sessao",
                    "nome_usuario",
                    "data_hora",
                    "acertos",
                    "erros",
                    "acertos_consecutivos",
                    "fase",
                    "tempo_medio_resposta",
                ],
            )
            self.assertEqual(len(linhas), 2)
            self.assertEqual(linhas[0]["id_sessao"], sessao.id_sessao)
            self.assertEqual(linhas[0]["nome_usuario"], "Maria")
            self.assertEqual(linhas[0]["acertos"], "10")
            self.assertEqual(linhas[0]["erros"], "2")
            self.assertEqual(linhas[0]["acertos_consecutivos"], "6")
            self.assertEqual(linhas[0]["fase"], "1")
            self.assertEqual(linhas[0]["tempo_medio_resposta"], "1.23")
            self.assertEqual(linhas[1]["fase"], "2")


# ======================================================================
# Fluxo da partida (GameController)
# ======================================================================
class TesteFluxo(TesteBase):
    def setUp(self):
        super().setUp()
        self.pasta = tempfile.TemporaryDirectory()
        self.relogio = Relogio()
        self.sons = SemSom()
        self.tela = _preparar_pygame_real()
        self.g = GameController(
            self.tela,
            relogio=self.relogio,
            rng=random.Random(42),
            sons=self.sons,
            diretorio_csv=self.pasta.name,
            usuario=Usuario(1, "Teste"),
        )

    def tearDown(self):
        self.pasta.cleanup()
        super().tearDown()

    # ---- ajudantes ----
    def passar(self, ms, passo=50):
        """Avança o relógio em passos de ``passo`` ms, atualizando o jogo."""
        for _ in range(ms // passo):
            self.relogio.ms += passo
            self.g.atualizar()

    def ate(self, estado, limite_ms=600000, passo=50):
        gasto = 0
        while self.g.estado != estado and gasto < limite_ms:
            self.passar(passo, passo)
            gasto += passo
        self.assertEqual(self.g.estado, estado, f"nunca chegou a {estado}")

    def jogar_rodada(self, erros_antes=0):
        """Faz o jogador reproduzir o caminho atual (com erros opcionais)."""
        self.ate(GameState.JOGO)
        caminho = list(self.g.atividade.caminho)
        for k in range(erros_antes):
            errado = next(
                i for i in range(12) if i != self.g.atividade.esperado
            )
            self.passar(300)
            self.g.selecionar_quadrado(errado)
        for indice in caminho:
            self.passar(400)
            self.g.selecionar_quadrado(indice)

    def jogar_fase(self, erros_por_rodada=0):
        for _ in range(GameSettings.RODADAS_POR_FASE):
            self.jogar_rodada(erros_por_rodada)
            if self.g.rodada < GameSettings.RODADAS_POR_FASE:
                self.ate(GameState.MOSTRANDO)

    # ---- testes ----
    def test_comeca_no_inicio_e_jogar_abre_a_fase_1(self):
        self.assertEqual(self.g.estado, GameState.INICIO)
        self.g.iniciar_jogo()
        self.assertEqual(self.g.estado, GameState.INTRO_FASE)
        self.assertEqual(self.g.fase, 1)
        self.ate(GameState.MOSTRANDO)
        self.ate(GameState.JOGO)

    def test_exibicao_toca_uma_nota_por_quadrado(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        notas = [s for s in self.sons.tocados if s[0] == "nota"]
        self.assertEqual(
            notas, [("nota", i) for i in range(self.g.config_fase.comprimento)]
        )

    def test_acerto_pontua_e_erro_nao_tira_pontos(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        esperado = self.g.atividade.esperado
        errado = next(i for i in range(12) if i != esperado)

        self.g.selecionar_quadrado(errado)
        self.assertEqual(self.g.pontos, 0)  # errar não tira ponto (RN04)
        self.assertEqual(self.g.desempenho.erros, 1)
        self.assertEqual(self.g.feedback.mensagem, t("tente_outra_vez"))
        self.assertEqual(self.g.atividade.passo_atual, 0)  # tenta de novo
        self.assertIn(("neutro",), self.sons.tocados)

        self.g.selecionar_quadrado(esperado)
        self.assertEqual(self.g.pontos, GameSettings.PONTOS_ACERTO)
        self.g.selecionar_quadrado(self.g.atividade.esperado)
        # segundo acerto seguido ganha bônus de sequência
        self.assertEqual(
            self.g.pontos,
            2 * GameSettings.PONTOS_ACERTO + GameSettings.BONUS_SEQUENCIA,
        )

    def test_clique_fora_do_turno_e_ignorado(self):
        self.g.iniciar_jogo()  # INTRO_FASE
        self.g.selecionar_quadrado(0)
        self.assertEqual(self.g.desempenho.total_respostas, 0)

    def test_fase_perfeita_avanca_e_registra_csv(self):
        self.g.iniciar_jogo()
        self.jogar_fase()
        self.assertEqual(self.g.estado, GameState.FASE_CONCLUIDA)
        self.assertTrue(self.g.ultima_fase_concluida)
        self.assertIn(("fase",), self.sons.tocados)

        passos = self.g.config_fase.comprimento * GameSettings.RODADAS_POR_FASE
        self.assertEqual(len(self.g.csv.linhas), 1)
        linha = self.g.csv.linhas[0]
        self.assertEqual(linha["acertos"], passos)
        self.assertEqual(linha["erros"], 0)
        self.assertEqual(linha["acertos_consecutivos"], passos)
        self.assertEqual(linha["fase"], 1)

        self.ate(GameState.INTRO_FASE)
        self.assertEqual(self.g.fase, 2)

    def test_fase_concluida_da_ajuda_de_recompensa(self):
        self.g.ajuda.quantidade_disponivel = 1
        self.g.iniciar_jogo()
        self.jogar_fase()
        self.assertEqual(self.g.ajuda.quantidade_disponivel, 2)

    def test_poucos_erros_ainda_avanca(self):
        self.g.iniciar_jogo()
        self.jogar_fase(erros_por_rodada=1)
        self.assertEqual(self.g.estado, GameState.FASE_CONCLUIDA)

    def test_muitos_erros_repete_a_mesma_fase_sem_punicao(self):
        self.g.iniciar_jogo()
        self.jogar_fase(erros_por_rodada=12)
        self.assertEqual(self.g.estado, GameState.FASE_NAO_CONCLUIDA)
        self.assertFalse(self.g.ultima_fase_concluida)
        self.assertIn(("tentar",), self.sons.tocados)
        self.assertEqual(self.g.csv.linhas[0]["erros"], 24)
        # só os acertos pontuaram: nenhum desconto por erro
        self.assertGreaterEqual(self.g.pontos, 0)

        self.ate(GameState.INTRO_FASE)
        self.assertEqual(self.g.fase, 1)  # repete a fase 1
        # tentativa nova: contadores zerados
        self.assertEqual(self.g.desempenho.total_respostas, 0)

    def test_percorrer_todas_as_fases_chega_a_conclusao(self):
        self.g.iniciar_jogo()
        for numero in range(1, GameSettings.total_fases() + 1):
            self.assertEqual(self.g.fase, numero)
            self.jogar_fase()
            self.assertEqual(self.g.estado, GameState.FASE_CONCLUIDA)
            self.ate(
                GameState.CONCLUSAO
                if numero == GameSettings.total_fases()
                else GameState.INTRO_FASE
            )
        resumo = self.g.resumo()
        self.assertGreater(resumo["pontos"], 0)
        self.assertGreater(resumo["tempo_total"], 0)
        self.assertGreater(resumo["tempo_medio_fase"], 0)
        self.assertEqual(len(self.g.csv.linhas), GameSettings.total_fases())

    def test_ajuda_aparece_com_inatividade_e_custa_pontos(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        self.g.selecionar_quadrado(self.g.atividade.esperado)
        pontos = self.g.pontos
        ajudas = self.g.ajuda.quantidade_disponivel
        self.assertFalse(self.g.ajuda.ajuda_ativa)

        self.passar(GameSettings.TEMPO_INATIVIDADE_AJUDA + 100)
        self.assertTrue(self.g.ajuda.ajuda_ativa)
        self.assertEqual(self.g.ajuda.quantidade_disponivel, ajudas - 1)
        self.assertEqual(self.g.pontos, pontos - GameSettings.PENALIDADE_AJUDA)

        # a ajuda some quando o jogador responde
        self.g.selecionar_quadrado(self.g.atividade.esperado)
        self.assertFalse(self.g.ajuda.ajuda_ativa)

    def test_pausa_congela_cronometros(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        ajudas = self.g.ajuda.quantidade_disponivel
        self.passar(GameSettings.TEMPO_INATIVIDADE_AJUDA - 1000)

        self.g.pausar()
        self.assertEqual(self.g.estado, GameState.PAUSADO)
        self.relogio.ms += 10 * 60 * 1000  # 10 minutos pausado
        self.g.atualizar()
        self.g.continuar()
        self.assertEqual(self.g.estado, GameState.JOGO)
        self.passar(100)
        self.assertEqual(self.g.ajuda.quantidade_disponivel, ajudas)
        self.assertFalse(self.g.ajuda.ajuda_ativa)
        self.assertEqual(self.g.desempenho.erros, 0)

    def test_so_pausa_durante_a_partida(self):
        self.g.pausar()
        self.assertEqual(self.g.estado, GameState.INICIO)

    def test_tempo_esgotado_nao_conclui_a_fase(self):
        GameSettings.TEMPO_LIMITE_RODADA = 20000
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        self.g.selecionar_quadrado(self.g.atividade.esperado)
        self.passar(21000)
        self.assertEqual(self.g.estado, GameState.FASE_NAO_CONCLUIDA)
        self.assertEqual(self.g.csv.linhas[0]["acertos"], 1)
        self.ate(GameState.INTRO_FASE)
        self.assertEqual(self.g.fase, 1)  # repete a fase

    def test_retroceder_e_avancar_pela_pausa(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        self.g.pausar()
        self.assertFalse(self.g.pode_retroceder)  # fase 1: não há anterior
        self.g.mudar_fase(-1)
        self.assertEqual(self.g.estado, GameState.PAUSADO)
        self.assertEqual(self.g.fase, 1)

        self.g.mudar_fase(+1)
        self.assertEqual(self.g.fase, 2)
        self.assertEqual(self.g.estado, GameState.INTRO_FASE)
        self.ate(GameState.JOGO)
        self.g.pausar()
        self.g.mudar_fase(-1)
        self.assertEqual(self.g.fase, 1)

    def test_nao_avanca_alem_da_ultima_fase(self):
        self.g.fase = GameSettings.total_fases()
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        self.g.pausar()
        self.assertFalse(self.g.pode_avancar)
        self.g.mudar_fase(+1)
        self.assertEqual(self.g.fase, GameSettings.total_fases())
        self.assertEqual(self.g.estado, GameState.PAUSADO)

    def test_sair_pede_confirmacao_e_salva_tentativa_parcial(self):
        self.g.iniciar_jogo()
        self.ate(GameState.JOGO)
        self.g.selecionar_quadrado(self.g.atividade.esperado)
        self.g.pausar()
        self.g.pedir_saida()
        self.assertEqual(self.g.estado, GameState.CONFIRMAR_SAIDA)
        self.g.cancelar_saida()
        self.assertEqual(self.g.estado, GameState.PAUSADO)

        self.g.pedir_saida()
        self.g.encerrar()
        self.assertEqual(self.g.estado, GameState.ENCERRADO)
        self.assertEqual(len(self.g.csv.linhas), 1)  # o que já foi jogado
        self.assertTrue(os.path.isfile(self.g.csv.caminho_arquivo))
        self.assertEqual(self.g.csv.linhas[0]["acertos"], 1)

    def test_reiniciar_comeca_sessao_nova(self):
        self.g.iniciar_jogo()
        self.jogar_fase()
        antiga = self.g.sessao.id_sessao
        self.relogio.ms += 5000
        self.g.reiniciar()
        self.assertEqual(self.g.pontos, 0)
        self.assertEqual(self.g.fase, GameSettings.FASE_INICIAL)
        self.assertEqual(self.g.estado, GameState.INTRO_FASE)
        self.assertEqual(self.g.csv.linhas, [])
        self.assertIsNotNone(antiga)

    def test_fase_inicial_vem_da_configuracao(self):
        self.g.fase = 4
        self.g.iniciar_jogo()
        self.assertEqual(self.g.config_fase.numero, 4)
        self.assertEqual(
            len(self.g.atividade.caminho), GameSettings.FASES[3].comprimento
        )

    # ---- desenho: percorre todas as telas ----
    def test_desenha_todas_as_telas_sem_erro(self):
        menu = Menu(self.tela)
        for estado in GameState.MENUS:
            menu.draw(estado, {("acao", "jogar"): 0.5}, self.g)

        self.g.mostrar_painel = True
        self.g.mostrar_previa = True
        self.g.pontos_maos = [(100, 100), (300, 300)]
        self.g.progresso_selecao = {("quad", 3): 0.6}
        self.g.iniciar_jogo()
        self.g.draw()  # INTRO_FASE
        self.ate(GameState.MOSTRANDO)
        for _ in range(60):
            self.passar(100)
            self.g.draw()  # exibição animada
        self.ate(GameState.JOGO)
        self.g.ajuda.ajuda_ativa = True
        self.g.selecionar_quadrado(11 if self.g.atividade.esperado != 11 else 10)
        self.g.draw()  # JOGO com ajuda e erro
        self.g.pausar()
        menu.draw(GameState.PAUSADO, {}, self.g)
        self.g.continuar()
        self.jogar_fase_restante()
        self.g.draw()

    def jogar_fase_restante(self):
        self.ate(GameState.JOGO)
        for indice in list(self.g.atividade.caminho)[self.g.atividade.passo_atual :]:
            self.passar(300)
            self.g.selecionar_quadrado(indice)
        if self.g.estado == GameState.INTERVALO:
            self.g.draw()
            self.ate(GameState.MOSTRANDO)
            self.jogar_rodada()
        self.assertIn(
            self.g.estado,
            (GameState.FASE_CONCLUIDA, GameState.FASE_NAO_CONCLUIDA),
        )
        self.g.draw()  # ícones de resultado

    def test_desenha_a_conclusao(self):
        self.g.iniciar_jogo()
        for numero in range(1, GameSettings.total_fases() + 1):
            self.jogar_fase()
            self.ate(
                GameState.CONCLUSAO
                if numero == GameSettings.total_fases()
                else GameState.INTRO_FASE
            )
        Menu(self.tela).draw(GameState.CONCLUSAO, {}, self.g)


# ======================================================================
# Integração: a classe CorTEA (eventos, mouse, mão por permanência, loop)
# ======================================================================
class RastreamentoFalso:
    """No lugar da webcam real (os testes não devem abrir a câmera)."""

    gerar_previa = False
    ativo = False
    motivo_inativo = "teste"

    def __init__(self, *args, **kwargs):
        pass

    def capturar_movimento(self):
        return []

    def obter_previa(self):
        return None

    def close(self):
        pass


class TesteIntegracao(TesteBase):
    def setUp(self):
        super().setUp()
        from ttea.games.CorTEA import cortea as modulo

        self._modulo = modulo
        self._rastreamento_original = modulo.Rastreamento
        modulo.Rastreamento = RastreamentoFalso
        self.pasta = tempfile.TemporaryDirectory()
        self.relogio = Relogio()
        self.jogo = modulo.CorTEA([])
        self.jogo.game._relogio = self.relogio
        self.jogo.game.sons = SemSom()
        self.jogo.game.csv.diretorio = self.pasta.name
        self.jogo.game.usuario.nome = "Teste"
        self.mao = []
        self.jogo.rastreamento.capturar_movimento = lambda: list(self.mao)

    def tearDown(self):
        self._modulo.Rastreamento = self._rastreamento_original
        self.pasta.cleanup()
        super().tearDown()

    def quadro(self, ms=50):
        self.relogio.ms += ms
        self.jogo.update()
        self.jogo.draw()

    def ate(self, estado, limite_ms=300000):
        gasto = 0
        while self.jogo.game.estado != estado and gasto < limite_ms:
            self.quadro()
            gasto += 50
        self.assertEqual(self.jogo.game.estado, estado)

    def ficar_com_a_mao_em(self, ponto, ms):
        self.mao = [ponto]
        for _ in range(ms // 50):
            self.quadro()

    def test_jogar_com_mouse_do_inicio_a_saida(self):
        j, g = self.jogo, self.jogo.game
        botoes = j.menu.botoes(GameState.INICIO)
        j._handle_click(botoes["jogar"].center)
        self.assertEqual(g.estado, GameState.INTRO_FASE)
        self.ate(GameState.JOGO)

        for indice in list(g.atividade.caminho):
            j._handle_click(g.grid.retangulo(indice).center)
        self.assertEqual(g.desempenho.acertos, g.config_fase.comprimento)

        antes = g.estado  # fim da 1ª rodada: INTERVALO
        j._handle_key(pygame.K_ESCAPE)
        self.assertEqual(g.estado, GameState.PAUSADO)
        j._handle_click(j.menu.botoes(GameState.PAUSADO)["sair"].center)
        self.assertEqual(g.estado, GameState.CONFIRMAR_SAIDA)
        j._handle_click(j.menu.botoes(GameState.CONFIRMAR_SAIDA)["nao"].center)
        self.assertEqual(g.estado, GameState.PAUSADO)
        j._handle_key(pygame.K_ESCAPE)  # ESC volta de onde parou
        self.assertEqual(g.estado, antes)

    def test_sair_da_pausa_volta_ao_inicio_sem_fechar(self):
        j, g = self.jogo, self.jogo.game
        j._handle_click(j.menu.botoes(GameState.INICIO)["jogar"].center)
        self.ate(GameState.JOGO)
        j._handle_click(g.grid.retangulo(g.atividade.esperado).center)
        csv_antigo = g.csv
        j._handle_key(pygame.K_ESCAPE)
        j._handle_click(j.menu.botoes(GameState.PAUSADO)["sair"].center)
        j._handle_click(j.menu.botoes(GameState.CONFIRMAR_SAIDA)["sim"].center)

        self.assertEqual(g.estado, GameState.INICIO)
        self.assertTrue(j.running)
        self.assertEqual(len(csv_antigo.linhas), 1)  # tentativa salva
        self.assertIsNot(g.csv, csv_antigo)  # próxima partida = nova sessão
        self.assertEqual((g.pontos, g.fase), (0, GameSettings.FASE_INICIAL))
        self.quadro()
        j._handle_click(j.menu.botoes(GameState.INICIO)["jogar"].center)
        self.assertEqual(g.estado, GameState.INTRO_FASE)

    def test_sair_da_conclusao_volta_ao_inicio_sem_fechar(self):
        j, g = self.jogo, self.jogo.game
        g.estado = GameState.CONCLUSAO
        j._handle_click(j.menu.botoes(GameState.CONCLUSAO)["sair"].center)
        self.assertEqual(g.estado, GameState.INICIO)
        self.assertTrue(j.running)

    def test_jogar_so_com_a_mao_na_webcam(self):
        j, g = self.jogo, self.jogo.game
        # botão "Jogar" selecionado só com a mão parada sobre ele
        self.ficar_com_a_mao_em(j.menu.botoes(GameState.INICIO)["jogar"].center, 400)
        self.assertEqual(g.estado, GameState.INICIO)  # ainda não deu o tempo
        self.ficar_com_a_mao_em(j.menu.botoes(GameState.INICIO)["jogar"].center, 500)
        self.assertEqual(g.estado, GameState.INTRO_FASE)

        self.mao = []
        self.ate(GameState.JOGO)
        # primeiro passo: mão atravessa um quadrado errado sem parar
        errado = next(i for i in range(12) if i != g.atividade.esperado)
        self.ficar_com_a_mao_em(g.grid.retangulo(errado).center, 300)
        self.assertEqual(g.desempenho.erros, 0)
        # agora para sobre o quadrado certo
        certo = g.grid.retangulo(g.atividade.esperado).center
        self.ficar_com_a_mao_em(certo, 400)
        self.assertEqual(g.desempenho.acertos, 0)
        self.assertGreater(g.progresso_selecao.get(("quad", g.atividade.esperado), 0), 0)
        self.ficar_com_a_mao_em(certo, 500)
        self.assertEqual(g.desempenho.acertos, 1)
        self.assertEqual(g.desempenho.erros, 0)
        # ficar parado no mesmo quadrado não conta de novo
        self.ficar_com_a_mao_em(certo, 2000)
        self.assertEqual(g.desempenho.acertos, 1)
        self.assertEqual(g.desempenho.erros, 0)

        # parado sobre outro quadrado errado: erro (uma vez só)
        errado = next(
            i for i in range(12) if i not in (g.atividade.esperado, g.atividade.caminho[0])
        )
        self.ficar_com_a_mao_em(g.grid.retangulo(errado).center, 1500)
        self.assertEqual(g.desempenho.erros, 1)

    def test_teclas(self):
        j, g = self.jogo, self.jogo.game
        j._handle_key(pygame.K_RETURN)  # Enter inicia
        self.assertEqual(g.estado, GameState.INTRO_FASE)
        j._handle_key(pygame.K_h)
        self.assertTrue(g.mostrar_painel)
        j._handle_key(pygame.K_c)
        self.assertEqual(j.rastreamento.gerar_previa, g.mostrar_previa)
        j._handle_key(pygame.K_m)
        self.assertFalse(GameSettings.SOM_LIGADO)
        self.quadro()
        self.assertFalse(j.janela_camera.aberta)

    def test_janela_da_camera(self):
        j, g = self.jogo, self.jogo.game
        mostrados = []
        fechar_pelo_x = []

        class JanelaFalsa:
            aberta = False

            def mostrar(self, quadro):
                if fechar_pelo_x:
                    self.aberta = False
                    return False
                mostrados.append(quadro)
                self.aberta = True
                return True

            def fechar(self):
                self.aberta = False

        j.janela_camera = JanelaFalsa()
        quadro = object()
        j.rastreamento.obter_previa = lambda: quadro
        g.mostrar_previa = True
        self.quadro()
        self.assertIs(mostrados[-1], quadro)
        self.assertTrue(j.janela_camera.aberta)

        j._handle_key(pygame.K_c)  # C fecha a janela
        self.quadro()
        self.assertFalse(j.janela_camera.aberta)

        j._handle_key(pygame.K_c)  # C abre de novo
        self.quadro()
        self.assertTrue(j.janela_camera.aberta)

        fechar_pelo_x.append(True)  # fechada pelo X: desliga a prévia
        self.quadro()
        self.assertFalse(g.mostrar_previa)
        self.assertFalse(j.rastreamento.gerar_previa)

    def test_configuracoes_e_volta(self):
        j, g = self.jogo, self.jogo.game
        j._handle_click(j.menu.botoes(GameState.INICIO)["configuracoes"].center)
        self.assertEqual(g.estado, GameState.CONFIGURACOES)
        antes = GameSettings.VOLUME
        j._handle_click(j.menu.botoes(GameState.CONFIGURACOES)["volume_menos"].center)
        self.assertLess(GameSettings.VOLUME, antes)
        j._handle_key(pygame.K_ESCAPE)
        self.assertEqual(g.estado, GameState.INICIO)
        j._handle_click(j.menu.botoes(GameState.INICIO)["controles"].center)
        self.assertEqual(g.estado, GameState.CONTROLES)
        self.quadro()

    def test_fechar_a_janela_salva_o_que_foi_jogado(self):
        j, g = self.jogo, self.jogo.game
        j._handle_click(j.menu.botoes(GameState.INICIO)["jogar"].center)
        self.ate(GameState.JOGO)
        j._handle_click(g.grid.retangulo(g.atividade.esperado).center)
        j._encerrar()
        self.assertFalse(j.running)
        j.cleanup()  # fecha webcam e pygame, informa o CSV
        self.assertTrue(os.path.isfile(g.csv.caminho_arquivo))

    def test_fase_inicial_pelo_argumento_da_plataforma(self):
        from ttea.games.CorTEA import cortea as modulo

        jogo = modulo.CorTEA(["--phase", "3", "--lang", "en_US", "--player_id", "9"])
        self.assertEqual(GameSettings.FASE_INICIAL, 3)
        self.assertEqual(GameSettings.CURRENT_LANG, "en_US")
        self.assertEqual(GameSettings.PLAYER_ID, 9)
        jogo.game.iniciar_jogo()
        self.assertEqual(jogo.game.fase, 3)
        jogo.rastreamento.close()


class TesteMenuETextos(TesteBase):
    def setUp(self):
        super().setUp()
        self.tela = _preparar_pygame_real()
        self.menu = Menu(self.tela)

    def test_botoes_por_tela(self):
        self.assertEqual(
            set(self.menu.botoes(GameState.INICIO)),
            {"jogar", "configuracoes", "controles"},
        )
        self.assertEqual(
            set(self.menu.botoes(GameState.PAUSADO)),
            {
                "continuar",
                "retroceder",
                "avancar",
                "sair",
                "som",
                "volume_menos",
                "volume_mais",
            },
        )
        self.assertEqual(
            set(self.menu.botoes(GameState.CONCLUSAO)), {"sair", "reiniciar"}
        )
        self.assertEqual(self.menu.botoes(GameState.JOGO), {})

    def test_cliques(self):
        botao = self.menu.botoes(GameState.INICIO)["jogar"]
        self.assertEqual(
            self.menu.acao_em(GameState.INICIO, botao.center), "jogar"
        )
        self.assertIsNone(self.menu.acao_em(GameState.INICIO, (1, 1)))
        barra = self.menu.barra_volume
        self.assertEqual(
            self.menu.acao_em(GameState.CONFIGURACOES, barra.center),
            "barra_volume",
        )

    def test_botoes_nao_se_sobrepoem_na_pausa_e_na_inicial(self):
        for estado in (GameState.PAUSADO, GameState.INICIO, GameState.CONCLUSAO):
            retangulos = list(self.menu.botoes(estado).values())
            for i, a in enumerate(retangulos):
                for b in retangulos[i + 1 :]:
                    sobrepoe = not (
                        a.right <= b.left
                        or b.right <= a.left
                        or a.bottom <= b.top
                        or b.bottom <= a.top
                    )
                    self.assertFalse(sobrepoe, f"{estado}: {a} x {b}")

    def test_fundo_3d_da_tela_inicial(self):
        from ttea.games.CorTEA.gameview.fundoinicio import FundoInicio

        fundo = FundoInicio(self.tela)
        caminho = FundoInicio.CAMINHOS[0]
        passo = FundoInicio.PASSO_MS
        # meio do 1º passo: o 1º quadrado do caminho sobe e brilha
        altura, brilho, _ = fundo.estado_quadrado(caminho[0], passo // 2)
        self.assertGreater(altura, FundoInicio.ESPESSURA)
        self.assertGreater(brilho, 0)
        # quadrado fora do caminho fica parado
        fora = next(i for i in range(12) if i not in caminho)
        self.assertEqual(
            fundo.estado_quadrado(fora, passo // 2), (FundoInicio.ESPESSURA, 0.0, False)
        )
        # no passo seguinte o 1º já foi percorrido (borda dourada)
        self.assertTrue(fundo.estado_quadrado(caminho[0], passo + 10)[2])
        # perspectiva: a linha de cima (fundo) fica mais acima e mais estreita
        x0, x1, z0, _ = fundo.limites_quadrado(0)
        x0p, x1p, z0p, _ = fundo.limites_quadrado(8)
        self.assertLess(fundo.projetar(x0, z0)[1], fundo.projetar(x0p, z0p)[1])
        largura_fundo = fundo.projetar(x1, z0)[0] - fundo.projetar(x0, z0)[0]
        largura_frente = fundo.projetar(x1p, z0p)[0] - fundo.projetar(x0p, z0p)[0]
        self.assertLess(largura_fundo, largura_frente)
        # desenha vários instantes de todos os caminhos sem erro
        total = sum(
            len(c) * passo + FundoInicio.PAUSA_MS for c in FundoInicio.CAMINHOS
        )
        for agora in range(0, total, 170):
            fundo.draw(agora)

    def test_controles_mostram_a_tecla_de_espelhar(self):
        textos = []
        original = UI.draw_text

        def capturar(surface, text, *args, **kwargs):
            textos.append(text)
            return original(surface, text, *args, **kwargs)

        UI.draw_text = staticmethod(capturar)
        try:
            self.menu.draw(GameState.CONTROLES)
        finally:
            UI.draw_text = original
        self.assertIn("E", textos)
        self.assertIn(t("ctrl_espelhar"), textos)

    def test_volume(self):
        GameSettings.VOLUME = 0.5
        self.menu.ajustar_volume("volume_mais")
        self.assertAlmostEqual(GameSettings.VOLUME, 0.6)
        for _ in range(20):
            self.menu.ajustar_volume("volume_mais")
        self.assertEqual(GameSettings.VOLUME, 1.0)
        for _ in range(20):
            self.menu.ajustar_volume("volume_menos")
        self.assertEqual(GameSettings.VOLUME, 0.0)
        barra = self.menu.barra_volume
        self.menu.ajustar_volume("barra_volume", (barra.left + barra.width // 2, 0))
        self.assertAlmostEqual(GameSettings.VOLUME, 0.5, places=1)

    def test_textos_nos_tres_idiomas(self):
        from ttea.games.CorTEA.gameutil.textos import TEXTOS

        chaves = set(TEXTOS["pt_BR"])
        for idioma in ("en_US", "es_ES"):
            self.assertEqual(set(TEXTOS[idioma]), chaves, idioma)
        GameSettings.CURRENT_LANG = "en_US"
        self.assertEqual(t("jogar"), "Play")
        GameSettings.CURRENT_LANG = "xx_XX"  # idioma desconhecido -> pt_BR
        self.assertEqual(t("jogar"), "Jogar")
        self.assertEqual(t("chave_inexistente"), "chave_inexistente")

    def test_formatar_tempo(self):
        self.assertEqual(formatar_tempo(0), "0:00")
        self.assertEqual(formatar_tempo(75), "1:15")
        self.assertEqual(formatar_tempo(600), "10:00")

    def test_grade_e_area(self):
        grade = Grid()
        self.assertEqual(len(grade.quadrados), 12)
        self.assertEqual(grade.indice_em(grade.retangulo(5).center), 5)
        self.assertIsNone(grade.indice_em((0, 0)))
        # o círculo/placar de baixo cabe abaixo da grade
        self.assertLess(grade.offset_y + grade.altura, GameSettings.SCREEN_HEIGHT)


if __name__ == "__main__":
    unittest.main()
