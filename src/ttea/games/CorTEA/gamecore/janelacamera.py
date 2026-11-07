from typing import Optional

import cv2
import numpy as np


class JanelaCamera:
    """Janela separada (OpenCV) com a imagem da webcam, como a "Tela de
    Captura" do KarTEA. Serve para o terapeuta conferir a detecção das mãos
    sem cobrir a grade do jogo.

    Deve ser usada pela thread principal (o ``imshow`` do OpenCV não é
    seguro fora dela); a thread do ``Rastreamento`` só prepara a imagem.
    """

    NOME = "CorTEA - Camera"

    def __init__(self):
        self.aberta = False

    def mostrar(self, quadro: Optional[np.ndarray]) -> bool:
        """Exibe o quadro (BGR). Retorna False se o usuário fechou a janela
        pelo X (quem chama deve parar de mostrá-la)."""
        if self.aberta and self._fechada_pelo_usuario():
            self.aberta = False
            return False
        if quadro is None:
            return True
        try:
            cv2.imshow(self.NOME, quadro)
            cv2.waitKey(1)  # processa os eventos da janela do OpenCV
            self.aberta = True
        except cv2.error:  # sem suporte a janelas (ex.: OpenCV headless)
            self.aberta = False
        return True

    def fechar(self) -> None:
        if not self.aberta:
            return
        try:
            cv2.destroyWindow(self.NOME)
            cv2.waitKey(1)
        except cv2.error:
            pass
        self.aberta = False

    def _fechada_pelo_usuario(self) -> bool:
        try:
            return cv2.getWindowProperty(self.NOME, cv2.WND_PROP_VISIBLE) < 1
        except cv2.error:
            return True
