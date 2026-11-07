import random
import time

import cv2
import pygame

from ttea.games.kartea.gamecore import Camera, PoseTracking
from ttea.games.kartea.gamemodel import (Background, Car, Image, Obstacle,
                                         Target)
from ttea.games.kartea.gameui import UI
from ttea.games.kartea.gameutil import GameSettings


class GameController:
    """Classe principal responsável pela lógica do jogo KarTEA."""

    def __init__(self, surface):
        self.surface = surface

        # Componentes principais
        self.background = Background()
        self.pose_tracking = PoseTracking()
        self.car = Car()
        self.cap = Camera()

        # Configurações baseadas no nível
        self._setup_level_settings()

        # Variáveis de jogo
        self.targets = []
        self.Last_Obj = -1
        self.targets_spawn_timer = 0

        self.score = 0
        self.movimento = 0
        self.alvo = 0
        self.alvo_c = 0
        self.alvo_d = 0
        self.obst = 0
        self.obst_c = 0
        self.obst_d = 0
        self.finish = 0

        self.SOM = GameSettings.SOUND  # arquivo.get_K_SOM(self.config_player)
        self.HUD = GameSettings.HUD  # arquivo.get_K_HUD(self.config_player)
        self.PAUSE = False

        self.game_start_time = time.time()
        self.time_left = GameSettings.LEVEL_TIME  # GameSettings.GAME_DURATION

        # Sons
        self.sounds = {}
        self._load_sounds()

        # Sincroniza variáveis globais de settings
        self._sync_settings()

    def _load_sounds(self):
        """Carrega os sons do jogo."""
        # self.sounds["slap"] = pygame.mixer.Sound(
        #    "Assets/Kartea/Sounds/point.wav"
        # )

        self.sounds["slap"] = pygame.mixer.Sound(GameSettings.POINT_SOUND)

        self.sounds["screaming"] = pygame.mixer.Sound(GameSettings.MISS_SOUND)

        # volume = 1 if arquivo.get_K_SOM(self.config_player) else 0
        volume = 1 if self.SOM else 0
        self.sounds["slap"].set_volume(volume)
        self.sounds["screaming"].set_volume(volume)

    def _setup_level_settings(self):
        """Configura velocidade e tempo de spawn conforme o nível."""
        GameSettings.TARGETS_MOVE_SPEED = GameSettings.LEVEL

        if GameSettings.LEVEL < 3:
            GameSettings.TARGETS_SPAWN_TIME = 8
        elif GameSettings.LEVEL < 5:
            GameSettings.TARGETS_SPAWN_TIME = 4
        else:
            GameSettings.TARGETS_SPAWN_TIME = 2

    def _sync_settings(self):
        """Sincroniza as variáveis locais com as globais de settings."""
        GameSettings.score = self.score
        GameSettings.movimento = self.movimento
        GameSettings.alvo = self.alvo
        GameSettings.alvo_c = self.alvo_c
        GameSettings.alvo_d = self.alvo_d
        GameSettings.obst = self.obst
        GameSettings.obst_c = self.obst_c
        GameSettings.obst_d = self.obst_d
        GameSettings.TIME_PAST = 0

    def reset(self):
        """Reseta todas as variáveis necessárias para iniciar um novo nível."""
        self.background = Background()
        self.pose_tracking = PoseTracking()
        self.car = Car()

        self._setup_level_settings()

        self.targets = []
        self.Last_Obj = -1
        self.targets_spawn_timer = 0
        self.game_start_time = time.time()
        self.time_left = GameSettings.LEVEL_TIME
        GameSettings.TIME_PAST = 0

        self.score = 0
        self.movimento = 0
        self.alvo = 0
        self.alvo_c = 0
        self.alvo_d = 0
        self.obst = 0
        self.obst_c = 0
        self.obst_d = 0
        self.finish = 0

        self._sync_settings()

    def spawn_targets(self):
        """Spawna um novo alvo ou obstáculo conforme a fase e nível."""
        t = time.time()
        if t <= self.targets_spawn_timer:
            return

        self.targets_spawn_timer = t + GameSettings.TARGETS_SPAWN_TIME

        fase = GameSettings.PHASE  # arquivo.get_K_FASE(self.config_player)
        pos = self.background.get_startPos()

        # Lógica de escolha do tipo de objeto
        if self.Last_Obj == -1:
            r = random.randint(0, 2)
        else:
            r = self.Last_Obj
            if GameSettings.LEVEL % 2 == 1:
                if r == 0:
                    r = 1
                elif r == 1:
                    while r == self.Last_Obj:
                        r = random.randint(0, 2)
                else:
                    r = 1
            else:
                while r == self.Last_Obj:
                    r = random.randint(0, 2)

        self.Last_Obj = r

        target = Target(r)
        obstacle = Obstacle(r)

        # Adiciona conforme a fase
        if fase == 1:
            self.targets.append(target)
            self.background.lines[pos].target = target
            self.alvo += 1
            GameSettings.Alvo += 1
            # TODO gravar sessão detalhado
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    settings.pista,
            #    r,
            #    "Criou Alvo",
            # )

        elif fase == 2:
            self.targets.append(obstacle)
            self.background.lines[pos].target = obstacle
            self.obst += 1
            GameSettings.Obst += 1
            # TODO gravar sessão detalhado
            # arquivo.grava_Detalhado(
            #    arquivo.get_Player(),
            #    arquivo.get_Sessao(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    settings.pista,
            #    r,
            #    "Criou Obstaculo",
            # )

        else:  # fase 3
            if random.randint(0, 100) < 50:
                self.targets.append(obstacle)
                self.background.lines[pos].target = obstacle
                self.obst += 1
                GameSettings.Obst += 1
                # TODO gravar sessão detalhado
                # arquivo.grava_Detalhado(
                #    arquivo.get_Player(),
                #    arquivo.get_Sessao(),
                #    arquivo.get_Fase(),
                #    arquivo.get_Nivel(),
                #    settings.pista,
                #    r,
                #    "Criou Obstaculo",
                # )
            else:
                self.targets.append(target)
                self.background.lines[pos].target = target
                self.alvo += 1
                GameSettings.Alvo += 1
                # TODO gravar sessão detalhado
                # arquivo.grava_Detalhado(
                #    arquivo.get_Player(),
                #    arquivo.get_Sessao(),
                #    arquivo.get_Fase(),
                #    arquivo.get_Nivel(),
                #    settings.pista,
                #    r,
                #    "Criou Alvo",
                # )

    def spawn_finish(self):
        """Coloca a linha de chegada no fundo."""

        pos = self.background.get_startPos()
        # "Assets/Kartea/Finish.png"
        self.background.lines[pos].sprite = Image.load(
            GameSettings.FINISH_IMAGE
        )

        self.background.lines[pos].spriteX = -0.5

    def load_camera(self) -> bool:
        """Carrega/atualiza o frame da câmera."""
        return self.cap.load_camera()

    def set_feet_position(self):
        """Atualiza a posição do carro com base na posição dos pés detectados."""
        self.cap.frame = self.pose_tracking.scan_feets(self.cap.frame)
        x, y = self.pose_tracking.get_feet_center()
        Y = GameSettings.SCREEN_HEIGHT - GameSettings.CAR_SIZE / 2
        self.car.rect.center = (x, Y)

    def draw(self):
        """Desenha todos os elementos na tela."""
        # Background
        if not self.PAUSE:
            if GameSettings.LEVEL < 3:
                self.background.speed1()
            elif GameSettings.LEVEL < 5:
                self.background.speed2()
            else:
                self.background.speed3()
        else:
            self.background.stop()

        self.background.draw(self.surface)

        # Carro
        self.car.draw(self.surface)

        # HUD
        if self.HUD:
            UI.draw_text(
                self.surface,
                f"Pontuação : {self.score}",
                (650, 5),
                GameSettings.COLORS["score"],
                font=GameSettings.FONTS["medium"],
                shadow=True,
                shadow_color=(255, 255, 255),
            )

            timer_text_color = (
                (160, 40, 0)
                if self.time_left < 5
                else GameSettings.COLORS["timer"]
            )
            UI.draw_text(
                self.surface,
                f"Tempo : {self.time_left}",
                (350, 5),
                timer_text_color,
                font=GameSettings.FONTS["medium"],
                shadow=True,
                shadow_color=(255, 255, 255),
            )

            UI.draw_text(
                self.surface,
                f"Fase : {GameSettings.PHASE}",
                (5, 5),
                timer_text_color,
                font=GameSettings.FONTS["medium"],
                shadow=True,
                shadow_color=(255, 255, 255),
            )

            UI.draw_text(
                self.surface,
                f"Nivel : {GameSettings.LEVEL}",
                (5, 25),
                timer_text_color,
                font=GameSettings.FONTS["medium"],
                shadow=True,
                shadow_color=(255, 255, 255),
            )

    def game_time_update(self):
        """Atualiza o tempo restante do nível."""
        self.time_left = GameSettings.LEVEL_TIME - int(
            GameSettings.TIME_PAST / 1000
        )

    def update(self):
        """Loop principal de atualização do jogo."""
        if not self.load_camera():
            return None

        self.set_feet_position()

        # Verifica pausa
        if self.PAUSE:
            GameSettings.MENU = "Pause"
            self.PAUSE = False
            return "menu"

        self.game_time_update()
        self.draw()

        if self.time_left > 0:
            # Spawn de alvos/obstáculos
            if self.time_left > (2 * GameSettings.TARGETS_SPAWN_TIME):
                self.spawn_targets()
            else:
                if self.finish == 0:
                    self.spawn_finish()
                    self.finish += 1

            # Detecção de pista e movimento
            x, y = self.pose_tracking.get_feet_center()
            feet1_x, feet1_y = self.pose_tracking.get_feet1()
            feet2_x, feet2_y = self.pose_tracking.get_feet2()

            troca_pista = GameSettings.pista

            # Atualiza pista com base nos pés
            if (
                GameSettings.div0_pista <= feet1_x < GameSettings.div1_pista
            ) and (
                GameSettings.div0_pista <= feet2_x < GameSettings.div1_pista
            ):
                GameSettings.pista = 0
            elif (
                GameSettings.div1_pista <= feet1_x < GameSettings.div2_pista
            ) and (
                GameSettings.div1_pista <= feet2_x < GameSettings.div2_pista
            ):
                GameSettings.pista = 1
            elif (
                GameSettings.div2_pista <= feet1_x < GameSettings.div3_pista
            ) and (
                GameSettings.div2_pista <= feet2_x < GameSettings.div3_pista
            ):
                GameSettings.pista = 2
            elif (
                (feet1_x < GameSettings.div0_pista)
                and (feet2_x < GameSettings.div0_pista)
            ) or (
                (feet1_x > GameSettings.div3_pista)
                and (feet2_x > GameSettings.div3_pista)
            ):
                GameSettings.pista = -1

            # Atualiza pista com base na posição central
            if GameSettings.div0_pista <= x < GameSettings.div1_pista:
                GameSettings.pista = 0
            elif GameSettings.div1_pista <= x < GameSettings.div2_pista:
                GameSettings.pista = 1
            elif GameSettings.div2_pista <= x < GameSettings.div3_pista:
                GameSettings.pista = 2
            else:
                GameSettings.pista = -1

            # Verifica troca de pista
            if GameSettings.pista != troca_pista:
                print(
                    f"Trocou da pista {troca_pista} para {GameSettings.pista}"
                )
                if GameSettings.pista != -1 and troca_pista != -1:
                    self.score += 2
                    self.movimento += 1
                    # TODO gravar sessão detalhado
                    # arquivo.grava_Detalhado(
                    #    arquivo.get_Player(),
                    #    arquivo.get_Sessao(),
                    #    arquivo.get_Fase(),
                    #    arquivo.get_Nivel(),
                    #    GameSettings.pista,
                    #    troca_pista,
                    #    "Trocou de Pista",
                    # )
                elif GameSettings.pista == -1:
                    print("Perdeu o Sinal")
                    # TODO gravar sessão detalhado
                    # arquivo.grava_Detalhado(
                    #    arquivo.get_Player(),
                    #    arquivo.get_Sessao(),
                    #    arquivo.get_Fase(),
                    #    arquivo.get_Nivel(),
                    #    GameSettings.pista,
                    #    troca_pista,
                    #    "Saiu da area do jogo",
                    # )
                    self.PAUSE = True
                    GameSettings.pista = 0

            # Atualiza posição do carro e interação com alvos
            self.car.rect.center = (x, y)
            self.car.left_click = self.pose_tracking.feet_closed
            self.score = self.car.kill_targets(
                self.surface, self.targets, self.score, self.sounds
            )

            # Remove alvos que saíram da tela
            for alvo in self.targets[:]:
                if alvo.current_pos[1] > (GameSettings.SCREEN_HEIGHT + 100):
                    self.score += alvo.kill(
                        self.surface, self.targets, self.sounds
                    )

        else:
            # Fim do nível - Feedback
            print("Terminou o Nível!")

            ponto_T = self.alvo * 12 + self.obst * 12

            if self.score >= (3 * ponto_T) / 4:
                # TODO gravar sessão detalhado
                # arquivo.grava_Detalhado(
                #    arquivo.get_Player(),
                #    arquivo.get_Sessao(),
                #    arquivo.get_Fase(),
                #    arquivo.get_Nivel(),
                #    settings.pista,
                #    settings.pista,
                #    "Controle Jogo: Avanca Nivel",
                # )
                GameSettings.MENU = "Feedback_3"
            elif self.score >= ponto_T / 4:
                # TODO gravar sessão detalhado
                # arquivo.grava_Detalhado(
                #    arquivo.get_Player(),
                #    arquivo.get_Sessao(),
                #    arquivo.get_Fase(),
                #    arquivo.get_Nivel(),
                #    GameSettings.pista,
                #    GameSettings.pista,
                #    "Controle Jogo: Permanece Nivel",
                # )
                GameSettings.MENU = "Feedback_2"
            else:
                # TODO gravar sessão detalhado
                # arquivo.grava_Detalhado(
                #    arquivo.get_Player(),
                #    arquivo.get_Sessao(),
                #    arquivo.get_Fase(),
                #    arquivo.get_Nivel(),
                #    GameSettings.pista,
                #    GameSettings.pista,
                #    "Controle Jogo: Retrocede Nivel",
                # )
                GameSettings.MENU = "Feedback_1"

            # Gravação final da sessão
            GameSettings.score = self.score
            GameSettings.movimento = self.movimento
            # TODO gravar sessão detalhado
            # arquivo.grava_Sessao(
            #    arquivo.get_Player(),
            #    arquivo.get_Fase(),
            #    arquivo.get_Nivel(),
            #    self.score,
            #    self.movimento,
            #    GameSettings.Alvo_c,
            #    GameSettings.Alvo_d,
            #    GameSettings.Obst_c,
            #    GameSettings.Obst_d,
            # )

            return "menu"

        # Eventos do Pygame (mantidos originais)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("Space game.py")
                    if self.background.speed == 0:
                        self.PAUSE = False
                        # print("Unpause")
                        # TODO gravar sessão detalhado
                        # arquivo.grava_Detalhado(
                        #    arquivo.get_Player(),
                        #    arquivo.get_Sessao(),
                        #    arquivo.get_Fase(),
                        #    arquivo.get_Nivel(),
                        #    GameSettings.pista,
                        #    GameSettings.pista,
                        #    "Controle UFE: Unpause",
                        # )
                    else:
                        self.PAUSE = True
                        # print("Pause")
                        # TODO gravar sessão detalhado
                        # arquivo.grava_Detalhado(
                        #    arquivo.get_Player(),
                        #    arquivo.get_Sessao(),
                        #    arquivo.get_Fase(),
                        #    arquivo.get_Nivel(),
                        #    GameSettings.pista,
                        #    GameSettings.pista,
                        #    "Controle UFE: Pause",
                        # )
                        self.background.stop()
                        GameSettings.MENU = "Pause"
                        return "menu"

                # Atalhos de som e HUD (mantidos exatamente como no original)
                if event.key in (pygame.K_s, pygame.K_1):
                    self.SOM = not self.SOM
                    volume = 1 if self.SOM else 0
                    self.sounds["slap"].set_volume(volume)
                    self.sounds["screaming"].set_volume(volume)
                    arquivo.set_K_SOM(self.config_player, self.SOM)
                    status = "Habilita Som" if self.SOM else "Desabilita Som"
                    # TODO gravar sessão detalhado
                    # arquivo.grava_Detalhado(
                    #    arquivo.get_Player(),
                    #    arquivo.get_Sessao(),
                    #    arquivo.get_Fase(),
                    #    arquivo.get_Nivel(),
                    #    GameSettings.pista,
                    #    GameSettings.pista,
                    #    f"Controle UFE: {status}",
                    # )

                if event.key in (pygame.K_h, pygame.K_2):
                    self.HUD = not self.HUD
                    arquivo.set_K_HUD(self.config_player, self.HUD)
                    status = "Habilita HUD" if self.HUD else "Desabilita HUD"
                    # TODO gravar sessão detalhado
                    # arquivo.grava_Detalhado(
                    #    arquivo.get_Player(),
                    #    arquivo.get_Sessao(),
                    #    arquivo.get_Fase(),
                    #    arquivo.get_Nivel(),
                    #    GameSettings.pista,
                    #    GameSettings.pista,
                    #    f"Controle UFE: {status}",
                    # )

        cv2.waitKey(1)
