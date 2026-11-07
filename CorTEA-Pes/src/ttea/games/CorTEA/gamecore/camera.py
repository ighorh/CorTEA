import sys
from typing import Optional, Tuple

import cv2
import numpy as np

from ttea.games.CorTEA.gameutil import GameSettings


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
    """Captura de vídeo via OpenCV.

    A leitura é feita pela thread do ``Rastreamento``; esta classe só abre,
    lê e libera a câmera. Se a câmera não abrir, ``aberta`` fica False e o
    jogo continua funcionando com o mouse.
    """

    LARGURA = 640
    ALTURA = 480

    def __init__(self, camera_index: int = 0):
        self.cap = cv2.VideoCapture(camera_index, camera_backend())
        if self.cap is not None and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.LARGURA)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.ALTURA)
        self.aberta = bool(self.cap is not None and self.cap.isOpened())

    def ler(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Lê um frame (BGR), espelhado na horizontal se
        ``GameSettings.ESPELHAR_CAMERA`` estiver ligado (efeito espelho)."""
        if not self.aberta:
            return False, None
        ok, frame = self.cap.read()
        if not ok or frame is None:
            return False, None
        if GameSettings.ESPELHAR_CAMERA:
            frame = cv2.flip(frame, 1)
        return True, frame

    def close_camera(self) -> None:
        """Libera a câmera."""
        if self.cap is not None:
            self.cap.release()
        self.aberta = False
