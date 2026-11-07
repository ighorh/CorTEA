import threading
import time
from typing import List, Optional, Tuple

import cv2
import numpy as np

from ttea.games.CorTEA.gamecore.camera import Camera
from ttea.games.CorTEA.gameutil import GameSettings

try:  # O jogo continua funcionando (com mouse) se o MediaPipe falhar.
    import mediapipe as mp

    _mp_pose = mp.solutions.pose
    _mp_drawing = mp.solutions.drawing_utils
except Exception:  # pragma: no cover - depende do ambiente
    mp = None
    _mp_pose = None
    _mp_drawing = None

# MediaPipe Pose: calcanhar esquerdo = 29; calcanhar direito = 30.
_CALCANHARES = (29, 30)


class Rastreamento:
    """Captura o movimento do jogador pela webcam usando o rastreio de pés.

    Uma thread própria lê a câmera e roda o MediaPipe Pose, para que a tela
    do jogo não trave esperando a webcam. O jogo consulta o resultado mais
    recente com ``capturar_movimento``.
    """

    def __init__(
        self, tamanho_tela: Tuple[int, int], indice_camera: int = 0
    ):
        self.largura, self.altura = tamanho_tela
        self._lock = threading.Lock()
        self._parar = threading.Event()
        self._pontos: List[Tuple[int, int]] = []
        self._previa = None  # imagem BGR (numpy) para a janela da câmera
        self._ultimo_frame = 0.0
        self._pontos_suavizados: List[Tuple[float, float]] = []
        self.gerar_previa = GameSettings.MOSTRAR_PREVIA_CAMERA
        self.posicao_usuario: Optional[Tuple[int, int]] = None

        self.camera: Optional[Camera] = None
        self._thread: Optional[threading.Thread] = None
        self.motivo_inativo = ""

        if _mp_pose is None:
            self.motivo_inativo = "MediaPipe Pose indisponível"
            return
        self.camera = Camera(indice_camera)
        if not self.camera.aberta:
            self.motivo_inativo = "Webcam não encontrada"
            return
        self._thread = threading.Thread(
            target=self._laco, name="cortea-rastreamento", daemon=True
        )
        self._thread.start()

    # ====================== API usada pelo jogo ======================
    @property
    def ativo(self) -> bool:
        """True se a webcam está entregando imagens agora."""
        return (
            self._thread is not None
            and self._thread.is_alive()
            and time.monotonic() - self._ultimo_frame < 1.0
        )

    def capturar_movimento(self) -> List[Tuple[int, int]]:
        """Posições (na tela do jogo) dos pés detectados no último frame."""
        with self._lock:
            pontos = list(self._pontos)
        self.posicao_usuario = pontos[0] if pontos else None
        return pontos

    def detectar_posicao(self, grid) -> Optional[int]:
        """Índice do quadrado da grade sob o primeiro pé detectado, ou ``None``."""
        pontos = self.capturar_movimento()
        return grid.indice_em(pontos[0]) if pontos else None

    def obter_previa(self):
        """Última imagem da webcam (BGR, numpy) ou ``None``."""
        with self._lock:
            return self._previa

    def close(self) -> None:
        self._parar.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self.camera is not None:
            self.camera.close_camera()

    # ====================== Conversões ======================
    def mapear(self, x: float, y: float) -> Tuple[int, int]:
        """Mapeia o ponto da câmera pela calibração de perspectiva do KarTEA."""
        largura = GameSettings.LARGURA_TELA_CONTROLE
        altura = GameSettings.ALTURA_TELA_CONTROLE
        pontos_origem = np.float32(GameSettings.PONTOS_CALIBRACAO)
        pontos_destino = np.float32(
            [
                [0, 0],
                [largura, 0],
                [0, altura],
                [largura, altura],
            ]
        )
        matriz = cv2.getPerspectiveTransform(pontos_origem, pontos_destino)

        ponto_x = int(x * largura)
        ponto_y = int(y * altura)
        divisor = (
            matriz[2][0] * ponto_x
            + matriz[2][1] * ponto_y
            + matriz[2][2]
        )
        if abs(divisor) < 1e-9:
            raise ValueError("Pontos de calibração produzem uma posição inválida.")

        posicao_x = (
            matriz[0][0] * ponto_x
            + matriz[0][1] * ponto_y
            + matriz[0][2]
        ) / divisor
        posicao_y = (
            matriz[1][0] * ponto_x
            + matriz[1][1] * ponto_y
            + matriz[1][2]
        ) / divisor
        tela_x = int(posicao_x * self.largura / largura)
        tela_y = int(posicao_y * self.altura / altura)
        return (
            min(self.largura - 1, max(0, tela_x)),
            min(self.altura - 1, max(0, self.altura - tela_y)),
        )

    def _extrair_pontos(self, resultados) -> List[Tuple[float, float]]:
        """Retorna um único ponto central calculado entre os dois calcanhares."""
        pose = resultados.pose_landmarks
        if pose is None:
            return []

        landmarks = pose.landmark
        x = sum(landmarks[i].x for i in _CALCANHARES) / len(_CALCANHARES)
        y = sum(landmarks[i].y for i in _CALCANHARES) / len(_CALCANHARES)
        return [(x, y)]

    def _suavizar(
        self, novos: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Média móvel exponencial por pé, para reduzir o tremor."""
        alfa = GameSettings.SUAVIZACAO
        anteriores = list(self._pontos_suavizados)
        resultado = []
        for x, y in novos:
            melhor = None
            for ant in anteriores:
                d = (ant[0] - x) ** 2 + (ant[1] - y) ** 2
                if d < 150**2 and (melhor is None or d < melhor[0]):
                    melhor = (d, ant)
            if melhor is not None:
                anteriores.remove(melhor[1])
                x = alfa * melhor[1][0] + (1 - alfa) * x
                y = alfa * melhor[1][1] + (1 - alfa) * y
            resultado.append((x, y))
        self._pontos_suavizados = resultado
        return [(int(x), int(y)) for x, y in resultado]

    def _desenhar_previa(self, frame, resultados):
        """Imagem (BGR) para a janela da câmera: os pés detectados e a área
        útil (o que fica dentro dela corresponde à tela do jogo)."""
        if resultados.pose_landmarks:
            _mp_drawing.draw_landmarks(
                frame,
                resultados.pose_landmarks,
                _mp_pose.POSE_CONNECTIONS,
            )
        altura, largura = frame.shape[:2]
        escala_x = largura / GameSettings.LARGURA_TELA_CONTROLE
        escala_y = altura / GameSettings.ALTURA_TELA_CONTROLE
        cantos = [
            (round(x * escala_x), round(y * escala_y))
            for x, y in GameSettings.PONTOS_CALIBRACAO
        ]
        for inicio, fim in ((0, 1), (1, 3), (3, 2), (2, 0)):
            cv2.line(frame, cantos[inicio], cantos[fim], (0, 200, 0), 2)
        for ponto in cantos:
            cv2.circle(frame, ponto, 5, (255, 0, 0), 2)
        return frame

    # ====================== Thread ======================
    def _laco(self) -> None:
        pose = _mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        try:
            while not self._parar.is_set():
                ok, frame = self.camera.ler()
                if not ok:
                    time.sleep(0.02)
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb.flags.writeable = False
                resultados = pose.process(rgb)
                rgb.flags.writeable = True

                normalizados = self._extrair_pontos(resultados)
                telas = [self.mapear(x, y) for x, y in normalizados]
                telas = self._suavizar(telas)

                previa = None
                if self.gerar_previa:
                    previa = self._desenhar_previa(frame, resultados)

                with self._lock:
                    self._pontos = telas
                    self._previa = previa
                    self._ultimo_frame = time.monotonic()
        finally:
            pose.close()
