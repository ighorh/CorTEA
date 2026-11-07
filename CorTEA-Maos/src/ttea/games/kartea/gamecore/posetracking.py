import cv2
import mediapipe as mp
import numpy as np

# from settings import *
# import settings as st
from ttea.games.kartea.gameutil import GameSettings

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_poses = mp.solutions.pose


class PoseTracking:
    """Classe responsável pela detecção de pose corporal usando MediaPipe, com foco nos pés."""

    def __init__(self):
        self.pose_tracking = mp_poses.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

        # Variáveis de posição dos pés
        self.feet_x = 0
        self.feet_y = 0
        self.feet1_x = 0
        self.feet1_y = 0
        self.feet2_x = 0
        self.feet2_y = 0

        self.results = None
        self.feet_closed = (
            False  # Mantido como no original (apesar do método vazio)
        )

    def scan_feets(self, image):
        """
        Processa o frame da câmera, detecta os pés e retorna a imagem anotada.

        Args:
            image: Frame capturado pela câmera (BGR)

        Returns:
            Imagem processada com landmarks desenhados
        """
        rows, cols, _ = image.shape

        # Converte BGR → RGB e marca como não writeable para melhor performance
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        self.results = self.pose_tracking.process(image)

        # Prepara a imagem para desenho
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.feet_closed = False

        if self.results.pose_landmarks:
            # Landmark 30 = left heel, Landmark 29 = right heel
            self.feet1_x = self.results.pose_landmarks.landmark[30].x
            self.feet1_y = self.results.pose_landmarks.landmark[30].y
            self.feet2_x = self.results.pose_landmarks.landmark[29].x
            self.feet2_y = self.results.pose_landmarks.landmark[29].y

            # Calcula ponto central entre os dois pés
            x = (self.feet1_x + self.feet2_x) / 2
            y = (self.feet1_y + self.feet2_y) / 2

            # Converte coordenadas usando transformação de perspectiva
            self.feet_x, self.feet_y = self.posicao(x, y)

            # Força a posição Y fixa (movimento apenas lateral)
            self.feet_y = GameSettings.SCREEN_HEIGHT - 50

            # Desenha os landmarks na imagem
            mp_drawing.draw_landmarks(
                image,
                self.results.pose_landmarks,
                mp_poses.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )

        return image

    def get_feet_center(self):
        """Retorna a posição central dos pés (usada para controlar o carro)."""
        return (self.feet_x, self.feet_y)

    def get_feet1(self):
        """Retorna a posição do pé esquerdo (heel)."""
        return self.posicao(self.feet1_x, self.feet1_y)

    def get_feet2(self):
        """Retorna a posição do pé direito (heel)."""
        return self.posicao(self.feet2_x, self.feet2_y)

    def display_feet(self):
        """Exibe a imagem processada (método mantido do original)."""
        if hasattr(self, "image") and self.image is not None:
            cv2.imshow("image", self.image)
            cv2.waitKey(1)

    def is_feet_closed(self):
        """Método reservado para detecção de pés fechados (ainda não implementado no original)."""
        pass

    def posicao(self, x: float, y: float):
        """
        Aplica transformação de perspectiva para mapear a posição do jogador
        da câmera para as coordenadas do jogo.
        """
        # Pontos de calibração da câmera para a tela de controle
        # TODO pontos de calibração devem ser configuráveis (atualmente fixos no settings)
        pts1 = np.float32(
            [
                GameSettings.pontos_calibracao[0],
                GameSettings.pontos_calibracao[1],
                GameSettings.pontos_calibracao[2],
                GameSettings.pontos_calibracao[3],
                # pontos_calibracao[0],
                # pontos_calibracao[1],
                # pontos_calibracao[2],
                # pontos_calibracao[3],
            ]
        )
        pts2 = np.float32(
            [
                [0, 0],
                [GameSettings.largura_tela_controle, 0],
                [0, GameSettings.altura_tela_controle],
                [
                    GameSettings.largura_tela_controle,
                    GameSettings.altura_tela_controle,
                ],
            ]
        )

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        # Posição normalizada do jogador
        p = (
            int(x * GameSettings.largura_tela_controle),
            int(y * GameSettings.altura_tela_controle),
        )

        # Aplica a transformação de perspectiva
        position_x = (
            matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]
        ) / (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2])
        position_y = (
            matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]
        ) / (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2])

        # Converte para as dimensões reais da tela do jogo
        p_after = (
            int(position_x * GameSettings.relacao_largura),
            int(position_y * GameSettings.relacao_altura),
        )

        return p_after
