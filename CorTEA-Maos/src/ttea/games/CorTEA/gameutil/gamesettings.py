import configparser
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import pygame


@dataclass(frozen=True)
class ConfigFase:
    """Parâmetros de dificuldade de uma fase (GDD: "Fases e Níveis":
    variação no tamanho da sequência e na velocidade de exibição)."""

    numero: int
    comprimento: int  # quantidade de quadrados do caminho
    passo_ms: int  # tempo que cada quadrado fica aceso na exibição
    n_cores: int  # cores diferentes na grade (inclui a cor do caminho)
    n_iscas: int  # quadrados da cor do caminho que NÃO fazem parte dele


class GameSettings:
    """Classe central que contém todas as configurações do jogo CorTEA."""

    # ====================== Configurações Gerais ======================
    WINDOW_NAME = "CorTEA - Caminho das Cores"
    GAME_TITLE = "CorTEA"
    # Resolução padrão da plataforma T-TEA
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    FPS = 60

    CURRENT_LANG = "pt_BR"
    PLAYER_ID = 0
    PROFESSIONAL_ID = 0
    CAMERA_INDEX = 0

    VOLUME = 0.5
    SOM_LIGADO = True

    # ====================== Grade ======================
    COLUNAS = 4
    LINHAS = 3
    TAM_QUAD = 130
    ESPACO = 10
    MARGEM = 20

    LARGURA_GRADE = COLUNAS * TAM_QUAD + (COLUNAS - 1) * ESPACO
    ALTURA_GRADE = LINHAS * TAM_QUAD + (LINHAS - 1) * ESPACO
    OFFSET_X = (SCREEN_WIDTH - LARGURA_GRADE) // 2
    OFFSET_Y = 55

    # ====================== Cores ======================
    COR_FUNDO = (245, 245, 245)
    COR_ACERTO = (0, 160, 60)
    # Feedback de "erro" propositalmente neutro: nada de vermelho vivo
    # (RN04 / RN05: sem punição nem estímulo que cause frustração).
    COR_ERRO = (100, 110, 150)
    COR_TEXTO = (35, 35, 35)

    # Paleta dos quadrados (protótipos do artigo: azul, vermelho, verde,
    # amarelo, roxo). A primeira cor é sorteada para o caminho a cada rodada.
    PALETA: List[Tuple[int, int, int]] = [
        (40, 40, 220),  # azul
        (245, 0, 0),  # vermelho
        (35, 215, 55),  # verde
        (240, 245, 0),  # amarelo
        (85, 35, 215),  # roxo
        (255, 140, 0),  # laranja
    ]

    # ====================== Regras do Jogo ======================
    # Tabela de fases. Fase 1 = sequência curta e lenta, sem iscas; as
    # seguintes aumentam o caminho, aceleram a exibição e adicionam
    # quadrados "isca" da mesma cor do caminho (exigem memória da ordem).
    FASES: List[ConfigFase] = [
        ConfigFase(1, 4, 1200, 3, 0),
        ConfigFase(2, 5, 1100, 3, 0),
        ConfigFase(3, 5, 1000, 4, 1),
        ConfigFase(4, 6, 900, 4, 1),
        ConfigFase(5, 6, 800, 5, 2),
        ConfigFase(6, 7, 700, 5, 2),
        ConfigFase(7, 7, 600, 5, 3),
        ConfigFase(8, 8, 600, 5, 3),
    ]
    FASE_INICIAL = 1
    RODADAS_POR_FASE = 2  # caminhos diferentes por fase

    # Pontuação (GDD: baseada em acertos consecutivos e desempenho geral)
    PONTOS_ACERTO = 10
    BONUS_SEQUENCIA = 2  # por acerto consecutivo acima do primeiro
    BONUS_SEQUENCIA_MAX = 5
    # A pontuação nunca diminui por erro (RN04). Só o uso da ajuda custa.
    PENALIDADE_AJUDA = 2

    # Índice de desempenho (Equação 1 do artigo):
    #   ID = (A x 2) - (E x 1) + (C x 1,5)
    PESO_ACERTOS = 2.0
    PESO_ERROS = 1.0
    PESO_CONSECUTIVOS = 1.5
    # Fração do ID máximo possível da fase exigida para avançar (RF12).
    # ID máximo = (PESO_ACERTOS + PESO_CONSECUTIVOS) x passos da fase.
    ID_MINIMO_FRACAO = 0.6

    # Sistema de ajuda (classe SistemaAjuda do diagrama de classes)
    AJUDAS_INICIAIS = 3
    AJUDAS_MAXIMO = 3
    TEMPO_INATIVIDADE_AJUDA = 6000  # ms sem responder até piscar a ajuda
    AJUDA_PISCA_MS = 350

    # Tempos (ms)
    DURACAO_FEEDBACK = 1200
    DURACAO_INTRO_FASE = 2200
    ATRASO_INICIAL_EXIBICAO = 700
    PAUSA_APOS_EXIBICAO = 600
    DURACAO_INTERVALO_RODADA = 1300
    DURACAO_RESULTADO_FASE = 3000
    TEMPO_LIMITE_RODADA = 120000  # 0 = sem limite

    # Seleção por permanência da mão sobre o quadrado (evita erros quando a
    # mão apenas atravessa a grade).
    TEMPO_PERMANENCIA = 700  # ms
    TOLERANCIA_PERDA_MAO = 250  # ms de "perdão" se a detecção piscar

    # Rastreamento (webcam)
    # "palma" (centro da mão, mais estável p/ crianças) ou "indicador"
    PONTO_DA_MAO = "palma"
    MARGEM_CAMERA = 0.10  # parte da imagem das bordas que fica "sobrando"
    SUAVIZACAO = 0.5  # 0 = sem suavização; perto de 1 = muito suave
    MOSTRAR_PREVIA_CAMERA = False
    # Espelha a imagem da webcam (o jogador se vê como num espelho). Algumas
    # webcams já entregam a imagem espelhada: nesse caso, desligue.
    ESPELHAR_CAMERA = True
    MOSTRAR_PAINEL = False

    # ====================== Fontes ======================
    # Preenchido por load_fonts(), pois exige pygame já inicializado
    FONTS: Dict[str, "pygame.font.Font"] = {}

    @classmethod
    def setup(cls, args) -> None:
        """Guarda os argumentos recebidos da plataforma T-TEA.

        Parameters
        ----------
        args : argparse.Namespace
            Argumentos ``--lang``, ``--player_id`` e ``--professional_id``
            (e, opcionalmente, ``--phase`` e ``--camera``).
        """
        cls.CURRENT_LANG = args.lang
        cls.PLAYER_ID = args.player_id
        cls.PROFESSIONAL_ID = args.professional_id
        cls.CAMERA_INDEX = getattr(args, "camera", 0)
        fase = getattr(args, "phase", 0)
        if fase:
            cls.FASE_INICIAL = fase

    @classmethod
    def config_da_fase(cls, numero: int) -> ConfigFase:
        """Retorna a configuração da fase (limitada ao intervalo válido)."""
        numero = max(1, min(cls.total_fases(), numero))
        return cls.FASES[numero - 1]

    @classmethod
    def total_fases(cls) -> int:
        return len(cls.FASES)

    @classmethod
    def load_ini(cls, caminho: str) -> None:
        """Sobrescreve os padrões com os valores de ``cortea.ini``.

        Valores ausentes ou inválidos mantêm o padrão; o arquivo é opcional.
        """
        if not caminho or not os.path.isfile(caminho):
            return
        ini = configparser.ConfigParser()
        try:
            ini.read(caminho, encoding="utf-8")
        except configparser.Error:
            return

        def ler(secao, chave, atual, tipo):
            try:
                if tipo is bool:
                    return ini.getboolean(secao, chave)
                return tipo(ini.get(secao, chave))
            except (configparser.Error, ValueError):
                return atual

        cls.FASE_INICIAL = ler("jogo", "fase_inicial", cls.FASE_INICIAL, int)
        cls.RODADAS_POR_FASE = max(
            1, ler("jogo", "rodadas_por_fase", cls.RODADAS_POR_FASE, int)
        )
        cls.ID_MINIMO_FRACAO = ler(
            "jogo", "id_minimo_fracao", cls.ID_MINIMO_FRACAO, float
        )
        cls.TEMPO_LIMITE_RODADA = (
            ler(
                "jogo",
                "tempo_limite_rodada_s",
                cls.TEMPO_LIMITE_RODADA // 1000,
                int,
            )
            * 1000
        )
        cls.AJUDAS_INICIAIS = ler(
            "ajuda", "ajudas_iniciais", cls.AJUDAS_INICIAIS, int
        )
        cls.AJUDAS_MAXIMO = ler("ajuda", "ajudas_maximo", cls.AJUDAS_MAXIMO, int)
        cls.TEMPO_INATIVIDADE_AJUDA = (
            ler(
                "ajuda",
                "tempo_inatividade_s",
                cls.TEMPO_INATIVIDADE_AJUDA // 1000,
                int,
            )
            * 1000
        )
        cls.TEMPO_PERMANENCIA = ler(
            "rastreamento", "tempo_permanencia_ms", cls.TEMPO_PERMANENCIA, int
        )
        cls.PONTO_DA_MAO = ler(
            "rastreamento", "ponto_da_mao", cls.PONTO_DA_MAO, str
        )
        cls.MOSTRAR_PREVIA_CAMERA = ler(
            "rastreamento", "mostrar_previa", cls.MOSTRAR_PREVIA_CAMERA, bool
        )
        cls.ESPELHAR_CAMERA = ler(
            "rastreamento", "espelhar_camera", cls.ESPELHAR_CAMERA, bool
        )
        cls.VOLUME = min(1.0, max(0.0, ler("som", "volume", cls.VOLUME, float)))
        cls.SOM_LIGADO = ler("som", "ligado", cls.SOM_LIGADO, bool)

    @classmethod
    def load_fonts(cls) -> None:
        """Carrega as fontes do jogo (chamar depois de ``pygame.init()``)."""
        cls.FONTS = {
            "small": pygame.font.SysFont("Arial", 17, bold=True),
            "text": pygame.font.SysFont("Arial", 24, bold=True),
            "feedback": pygame.font.SysFont("Arial", 32, bold=True),
            "title": pygame.font.SysFont("Arial", 76, bold=True),
            "fase": pygame.font.SysFont("Arial", 96, bold=True),
        }
