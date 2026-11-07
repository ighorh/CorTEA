import threading
import time
from typing import List, Optional, Tuple

import cv2

from ttea.games.CorTEA.gamecore.camera import Camera
from ttea.games.CorTEA.gameutil import GameSettings

try:  # O jogo continua funcionando (com mouse) se o MediaPipe falhar.
    import mediapipe as mp

    _mp_hands = mp.solutions.hands
    _mp_drawing = mp.solutions.drawing_utils
except Exception:  # pragma: no cover - depende do ambiente
    mp = None
    _mp_hands = None
    _mp_drawing = None

# Landmarks do MediaPipe Hands usados para o centro da palma:
# punho (0) e base dos dedos (5, 9, 13, 17).
_PALMA = (0, 5, 9, 13, 17)
_PONTA_INDICADOR = 8


class Rastreamento:
    """Captura o movimento do jogador pela webcam (classe ``Rastreamento``
    do diagrama de classes).

    Uma thread própria lê a câmera e roda o MediaPipe, para que a tela do
    jogo não trave esperando a webcam. O jogo consulta o resultado mais
    recente com ``capturar_movimento``.

    Hoje rastreia as mãos; para rastrear os pés basta trocar o que é
    devolvido em ``_extrair_pontos`` (as demais partes não mudam).
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

        if _mp_hands is None:
            self.motivo_inativo = "MediaPipe indisponível"
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
        """Posições (na tela do jogo) das mãos detectadas no último frame."""
        with self._lock:
            pontos = list(self._pontos)
        self.posicao_usuario = pontos[0] if pontos else None
        return pontos

    def detectar_posicao(self, grid) -> Optional[int]:
        """Índice do quadrado da grade sob a primeira mão, ou ``None``."""
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
        """Converte coordenadas normalizadas (0 a 1) da câmera para a tela.

        Descarta uma margem nas bordas da imagem, para que os cantos da
        grade sejam alcançáveis sem a mão sair do enquadramento.
        """
        m = GameSettings.MARGEM_CAMERA
        escala = max(1e-6, 1.0 - 2 * m)
        nx = min(1.0, max(0.0, (x - m) / escala))
        ny = min(1.0, max(0.0, (y - m) / escala))
        return (
            min(self.largura - 1, int(nx * self.largura)),
            min(self.altura - 1, int(ny * self.altura)),
        )

    def _extrair_pontos(self, resultados) -> List[Tuple[float, float]]:
        """Um ponto normalizado (x, y) por mão detectada."""
        pontos = []
        if not resultados.multi_hand_landmarks:
            return pontos
        for mao in resultados.multi_hand_landmarks:
            lm = mao.landmark
            if GameSettings.PONTO_DA_MAO == "indicador":
                pontos.append((lm[_PONTA_INDICADOR].x, lm[_PONTA_INDICADOR].y))
            else:
                pontos.append(
                    (
                        sum(lm[i].x for i in _PALMA) / len(_PALMA),
                        sum(lm[i].y for i in _PALMA) / len(_PALMA),
                    )
                )
        return pontos

    def _suavizar(
        self, novos: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Média móvel exponencial por mão, para reduzir o tremor."""
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
        """Imagem (BGR) para a janela da câmera: as mãos detectadas e a área
        útil (o que fica dentro dela corresponde à tela do jogo)."""
        if resultados.multi_hand_landmarks:
            for mao in resultados.multi_hand_landmarks:
                _mp_drawing.draw_landmarks(
                    frame, mao, _mp_hands.HAND_CONNECTIONS
                )
        altura, largura = frame.shape[:2]
        m = GameSettings.MARGEM_CAMERA
        cv2.rectangle(
            frame,
            (int(m * largura), int(m * altura)),
            (int((1 - m) * largura), int((1 - m) * altura)),
            (0, 200, 0),
            2,
        )
        return frame

    # ====================== Thread ======================
    def _laco(self) -> None:
        maos = _mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        try:
            while not self._parar.is_set():
                ok, frame = self.camera.ler()
                if not ok:
                    time.sleep(0.02)
                    continue

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb.flags.writeable = False
                resultados = maos.process(rgb)
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
            maos.close()
