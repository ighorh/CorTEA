from typing import TYPE_CHECKING, Dict

import cv2
import numpy as np
import pygame

from ttea.games.kartea.model import PlayerKarteaSession
from ttea.games.kartea.util import KarteaPathConfig

if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaConfig
    from ttea.games.kartea.service import PlayerKarteaConfigService


class GameSettings:
    """Classe central que contém todas as configurações do jogo KarTEA."""

    # ====================== Configurações Gerais ======================
    WINDOW_NAME = "KarTEA"
    GAME_TITLE = WINDOW_NAME
    CAMERA = 0
    CAMERA_FLIP = 0
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    FPS = 60
    DRAW_FPS = False

    CURRENT_LANG = "pt_BR"
    PLAYER_ID = 0
    PROFESSIONAL_ID = 0

    PHASE = 1
    LEVEL = 1
    LEVEL_TIME = 120

    PALETTE = 0
    SOUND = True
    HUD = True

    PLAYER_KARTEA_SERVICE = None

    # ====================== Variáveis de Jogo ======================
    CONTADOR = 0
    pontos_calibracao = np.zeros((4, 2), dtype=int)

    div0_pista = 0
    div1_pista = SCREEN_WIDTH // 3
    div2_pista = 2 * (SCREEN_WIDTH // 3)
    div3_pista = SCREEN_WIDTH

    pista = 1
    score = 0
    movimento = 0
    Alvo = 0
    Alvo_c = 0
    Alvo_d = 0
    Obst = 0
    Obst_c = 0
    Obst_d = 0

    # ====================== Tamanhos ======================
    BUTTONS_SIZES = (150, 45)
    CAR_SIZE = int(SCREEN_WIDTH / 5)
    CAR_HITBOX_SIZE = (CAR_SIZE + 50, CAR_SIZE + 50)
    TARGETS_SIZES = (100, 100)
    OBSTACLE_SIZES = (100, 100)

    OBJ_POS = [(368, 80), (393, 80), (419, 80)]

    ROAD_WIDTH = 400
    SEGMENT_LENGTH = 200
    CAMERA_DEPTH = 3

    # ====================== Desenho e Depuração ======================
    DRAW_HITBOX = False

    # ====================== Animação ======================
    ANIMATION_SPEED = 0.01

    # ====================== Dificuldade ======================
    # GAME_DURATION = 30
    TIME_PAST = 0

    TARGETS_SPAWN_TIME = 8
    TARGETS_MOVE_SPEED = 1
    OBSTACLE_PENALITY = 0

    # ====================== Cores ======================
    COLORS = {
        "title": (38, 61, 39),
        "score": (38, 61, 39),
        "timer": (38, 61, 39),
        "buttons": {
            "default": (56, 67, 209),
            "second": (87, 99, 255),
            "text": (255, 255, 255),
            "shadow": (46, 54, 163),
        },
    }

    # ====================== Som e Música ======================
    MUSIC_VOLUME = 0
    SOUNDS_VOLUME = 1

    MISS_SOUND = ""
    CRASH_SOUND = ""
    POINT_SOUND = ""
    WIN_SOUND = ""
    CLOCK_TICK_SOUND = ""

    # ====================== Fontes ======================
    pygame.font.init()
    FONTS = {
        "small": pygame.font.Font(None, 10),
        "medium": pygame.font.Font(None, 25),
        "big": pygame.font.Font(None, 50),
    }

    # ====================== Config e Estado do Menu ======================
    MENU = "Inicial"
    MENU_BACKGROUND = ""
    MENU_CLICK_SOUND = ""
    MENU_FEEDBACK_25 = ""
    MENU_FEEDBACK_50 = ""
    MENU_FEEDBACK_75 = ""

    # ====================== Cores para OpenCV ======================
    azul = (0, 0, 255)
    verde = (0, 255, 0)
    vermelho = (255, 0, 0)
    amarelo = (255, 255, 0)
    branco = (255, 255, 255)
    preto = (0, 0, 0)

    fonte = cv2.FONT_HERSHEY_SIMPLEX
    font = pygame.font.SysFont(None, 25)

    # ====================== Resources ======================
    ENVIRONMENT_IMAGE = ""
    ENVIRONMENT_IMAGE_OTHER_SIDE = ""
    FINISH_IMAGE = ""
    HORIZON_BG_IMAGE = ""
    NEGATIVE_FEEDBACK_SOUND = ""
    NEGATIVE_FEEDBACK_IMAGE = ""
    NEUTRAL_FEEDBACK_IMAGE = ""
    NEUTRAL_FEEDBACK_SOUND = ""
    OBSTACLE_IMAGE = ""
    POSITIVE_FEEDBACK_IMAGE = ""
    POSITIVE_FEEDBACK_SOUND = ""
    TARGET_IMAGE = ""
    VEHICLE_IMAGE = ""

    # ====================== Configurações de Hardware ======================
    # Tamanhos das telas
    largura_projetor = SCREEN_WIDTH
    altura_projetor = SCREEN_HEIGHT

    largura_tela_controle = 640
    altura_tela_controle = 480

    relacao_largura = largura_projetor / largura_tela_controle
    relacao_altura = altura_projetor / altura_tela_controle

    # Telas para calibração e controle
    tela_de_calibracao = np.zeros(
        (altura_projetor, largura_projetor, 3), np.uint8
    )
    tela_de_controle = np.zeros(
        (altura_tela_controle, largura_tela_controle, 3), np.uint8
    )

    @classmethod
    def setup(
        cls,
        args,
        player_kartea_service: "PlayerKarteaConfigService",
        player_config: "PlayerKarteaConfig",
        default_config: Dict[str, str],
    ) -> None:
        cls.CURRENT_LANG = args.lang
        cls.PLAYER_ID = args.player_id
        cls.PROFESSIONAL_ID = args.professional_id
        cls.PLAYER_KARTEA_SERVICE = player_kartea_service

        # ====================== Game Settings ======================
        if not player_config or player_config.phase.id is None:
            cls.PHASE = int(default_config["game_settings"]["phase_default"])
        else:
            cls.PHASE = player_config.phase.id

        if not player_config or player_config.phase.id is None:
            cls.LEVEL = int(default_config["game_settings"]["level_default"])
        else:
            cls.LEVEL = player_config.level.id

        if not player_config or player_config.level_time is None:
            cls.LEVEL_TIME = int(
                default_config["game_settings"]["level_time_default"]
            )
        else:
            cls.LEVEL_TIME = player_config.level_time

        # ====================== Visual Resources ======================
        if not player_config or player_config.car_image is None:
            cls.VEHICLE_IMAGE = default_config["visual_resources"][
                "vehicle_image_default"
            ]
        else:
            cls.VEHICLE_IMAGE = player_config.car_image

        if not player_config or player_config.environment_image is None:
            cls.ENVIRONMENT_IMAGE = default_config["visual_resources"][
                "environment_image_default"
            ]
        else:
            cls.ENVIRONMENT_IMAGE = player_config.environment_image

        cls.ENVIRONMENT_IMAGE_OTHER_SIDE = KarteaPathConfig.game_builtin_image(
            "variant1environment"
        )

        if not player_config or player_config.obstacle_image is None:
            cls.OBSTACLE_IMAGE = default_config["visual_resources"][
                "obstacle_image_default"
            ]
        else:
            cls.OBSTACLE_IMAGE = player_config.obstacle_image

        if not player_config or player_config.target_image is None:
            cls.TARGET_IMAGE = default_config["visual_resources"][
                "target_image_default"
            ]
        else:
            cls.TARGET_IMAGE = player_config.target_image

        # ====================== Visual Feedback ======================
        if not player_config or player_config.positive_feedback_image is None:
            cls.POSITIVE_FEEDBACK_IMAGE = default_config["visual_feedback"][
                "positive_feedback_image_default"
            ]
        else:
            cls.POSITIVE_FEEDBACK_IMAGE = player_config.positive_feedback_image

        if (
            not player_config
            or player_config.neutral_feedback_image_default is None
        ):
            cls.NEUTRAL_FEEDBACK_IMAGE = default_config["visual_feedback"][
                "neutral_feedback_image_default"
            ]
        else:
            cls.NEUTRAL_FEEDBACK_IMAGE = (
                player_config.neutral_feedback_image_default
            )

        if (
            not player_config
            or player_config.negative_feedback_image_default is None
        ):
            cls.NEGATIVE_FEEDBACK_IMAGE = default_config["visual_feedback"][
                "negative_feedback_image_default"
            ]
        else:
            cls.NEGATIVE_FEEDBACK_IMAGE = (
                player_config.negative_feedback_image_default
            )

        # ====================== Sound Feedback =========================
        if not player_config or player_config.positive_feedback_sound is None:
            cls.POSITIVE_FEEDBACK_SOUND = default_config["sound_feedback"][
                "positive_feedback_sound_default"
            ]
        else:
            cls.POSITIVE_FEEDBACK_SOUND = player_config.positive_feedback_sound

        if not player_config or player_config.neutral_feedback_sound is None:
            cls.NEUTRAL_FEEDBACK_SOUND = default_config["sound_feedback"][
                "neutral_feedback_sound_default"
            ]
        else:
            cls.NEUTRAL_FEEDBACK_SOUND = player_config.neutral_feedback_sound

        if not player_config or player_config.negative_feedback_sound is None:
            cls.NEGATIVE_FEEDBACK_SOUND = default_config["sound_feedback"][
                "negative_feedback_sound_default"
            ]
        else:
            cls.NEGATIVE_FEEDBACK_SOUND = player_config.negative_feedback_sound

        # ====================== Interface Settings ======================
        if not player_config or player_config.hud is None:
            cls.HUD = default_config["interface_settings"]["hud_default"]
        else:
            cls.HUD = player_config.hud

        if not player_config or player_config.palette is None:
            cls.PALETTE = default_config["interface_settings"][
                "palette_default"
            ]
        else:
            cls.PALETTE = player_config.palette

        if not player_config or player_config.sound is None:
            cls.SOUND = default_config["interface_settings"]["sound_default"]
        else:
            cls.SOUND = player_config.sound

        # ====================== Config e Estado do Menu ======================
        cls.MENU_BACKGROUND = KarteaPathConfig.game_builtin_image("menu")
        cls.MENU_CLICK_SOUND = KarteaPathConfig.game_sound("point.wav")
        cls.MENU_FEEDBACK_25 = KarteaPathConfig.game_builtin_image("trophy25")
        cls.MENU_FEEDBACK_50 = KarteaPathConfig.game_builtin_image("trophy50")
        cls.MENU_FEEDBACK_75 = KarteaPathConfig.game_builtin_image("trophy75")

        # ====================== Som e Música ======================
        cls.MISS_SOUND = KarteaPathConfig.game_sound("miss.wav")
        cls.CRASH_SOUND = KarteaPathConfig.game_sound("crash.wav")
        cls.POINT_SOUND = KarteaPathConfig.game_sound("point.wav")
        cls.WIN_SOUND = KarteaPathConfig.game_sound("win.wav")
        cls.CLOCK_TICK_SOUND = KarteaPathConfig.game_sound("clocktick.wav")

        # ====================== Resources ===================================
        cls.FINISH_IMAGE = KarteaPathConfig.game_builtin_image("finish")
        cls.HORIZON_BG_IMAGE = KarteaPathConfig.game_builtin_image("horizon")

    @classmethod
    def session_data(
        cls,
        player_id: int,
        professional_id: int,
        phase_reached: int,
        level_reached: int,
        general_score: int,
        q_movement: int,
        q_collided_target: int,
        q_avoided_target: int,
        q_collided_obstacle: int,
        q_avoided_obstacle: int,
    ) -> None:
        player = cls.PLAYER_KARTEA_SERVICE.dao.player_dao.select(player_id)

        professional = cls.PLAYER_KARTEA_SERVICE.dao.professional_dao.select(
            professional_id
        )
        phase = cls.PLAYER_KARTEA_SERVICE.dao.phase_dao.select(phase_reached)
        level = cls.PLAYER_KARTEA_SERVICE.dao.level_dao.select(
            phase_reached, level_reached
        )

        player_kartea_session = PlayerKarteaSession(
            player=player, professional=professional, phase=phase, level=level
        )

        player_kartea_session.phase_reached = phase_reached
        player_kartea_session.level_reached = level_reached
        player_kartea_session.general_score = general_score
        player_kartea_session.q_movement = q_movement
        player_kartea_session.q_collided_target = q_collided_target
        player_kartea_session.q_avoided_target = q_avoided_target
        player_kartea_session.q_collided_obstacle = q_collided_obstacle
        player_kartea_session.q_avoided_obstacle = q_avoided_obstacle

    @classmethod
    def session_detail_data():
        pass
