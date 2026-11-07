import sys

import cv2

# import settings
from ttea.games.kartea.gameutil import GameSettings


def camera_backend() -> int:
    """Return the native OpenCV camera backend for the current platform."""
    if sys.platform == "win32":
        return cv2.CAP_DSHOW
    if sys.platform == "darwin":
        return cv2.CAP_AVFOUNDATION
    if sys.platform.startswith("linux"):
        return cv2.CAP_V4L2
    return cv2.CAP_ANY


class Camera:
    """Classe responsável pelo gerenciamento da câmera (captura de vídeo via OpenCV)."""

    def __init__(self):
        """Inicializa a captura de vídeo usando a configuração definida em settings."""
        self.cap = cv2.VideoCapture(GameSettings.CAMERA, camera_backend())
        self.ret = False
        self.frame = None

        # Lê o primeiro frame para inicialização
        self.ret, self.frame = self.cap.read()

    def load_camera(self) -> bool:
        """
        Lê um novo frame da câmera, aplica flip horizontal e desenha
        a área de calibração na imagem.
        """
        self.ret, self.frame = self.cap.read()

        if not self.ret or self.frame is None:
            self.frame = None
            return False

        if self.frame is not None:
            # Espelha a imagem horizontalmente (efeito mirror)
            self.frame = cv2.flip(self.frame, 1)

            # Desenha as linhas da área de calibração
            cv2.line(
                self.frame,
                GameSettings.pontos_calibracao[0],
                GameSettings.pontos_calibracao[1],
                GameSettings.verde,
                2,
            )

            cv2.line(
                self.frame,
                GameSettings.pontos_calibracao[1],
                GameSettings.pontos_calibracao[3],
                GameSettings.verde,
                2,
            )

            cv2.line(
                self.frame,
                GameSettings.pontos_calibracao[2],
                GameSettings.pontos_calibracao[0],
                GameSettings.verde,
                2,
            )

            cv2.line(
                self.frame,
                GameSettings.pontos_calibracao[2],
                GameSettings.pontos_calibracao[3],
                GameSettings.verde,
                2,
            )

            # Desenha os pontos de calibração como círculos
            cv2.circle(
                self.frame,
                GameSettings.pontos_calibracao[0],
                5,
                GameSettings.azul,
                3,
            )
            cv2.circle(
                self.frame,
                GameSettings.pontos_calibracao[1],
                5,
                GameSettings.azul,
                3,
            )
            cv2.circle(
                self.frame,
                GameSettings.pontos_calibracao[2],
                5,
                GameSettings.azul,
                3,
            )
            cv2.circle(
                self.frame,
                GameSettings.pontos_calibracao[3],
                5,
                GameSettings.azul,
                3,
            )

            # Exibe a janela de captura
            cv2.imshow("Tela de Captura", self.frame)

        return True

    def close_camera(self):
        """Libera a câmera e fecha a janela de captura."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyWindow("Tela de Captura")
