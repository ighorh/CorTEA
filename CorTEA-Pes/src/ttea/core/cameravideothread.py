import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose
from PIL import Image, ImageDraw, ImageFont
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QImage

from ttea.service import CalibrationService


class CameraVideoThread(QThread, QObject):
    change_pixmap_signal = Signal(QImage)
    error_signal = Signal(str)

    def __init__(self, camera_index: int, use_low_resolution: bool = False):
        from ttea.core import MediaPipeFilter, MediaPipeManager

        super().__init__()
        self.camera_index = camera_index
        self.running = True
        self.mp_manager = MediaPipeManager()
        self.use_low_resolution = use_low_resolution
        self.filter = MediaPipeFilter()
        self.service = CalibrationService()

    def _convert_to_proto(self, landmarks):
        """Converte landmarks da Task API para o formato esperado pelo draw_landmarks."""
        landmark_subset = landmark_pb2.NormalizedLandmarkList()
        for l in landmarks:
            landmark_subset.landmark.add(
                x=l.x, y=l.y, z=l.z, visibility=l.visibility
            )
        return landmark_subset

    def run(self):
        if self.service.is_windows():
            cap = cv2.VideoCapture(
                self.camera_index, self.service.get_opencv_capture_backend()
            )
        else:
            cap = cv2.VideoCapture(
                self.camera_index, self.service.get_opencv_capture_backend()
            )

        if not cap.isOpened():
            self.error_signal.emit(self.tr("Não foi possível abrir a câmera."))
            return

        prev_time = 0

        if self.use_low_resolution:
            cap.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                self.service.get_opencv_width(),
            )
            cap.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                self.service.get_opencv_height(),
            )

        while self.running:
            ret, frame = cap.read()

            if ret:
                # 1. CÁLCULO DE BRILHO (Para debug de Luz Plena)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                avg_brightness = np.mean(hsv[:, :, 2])

                # 2. PRÉ-PROCESSAMENTO: Filtros Automáticos
                if self.service.is_filter_enable_filter():
                    frame = self.filter.apply_enhancements(frame)

                # Cálculo de FPS
                curr_time = time.time()
                fps = (
                    1 / (curr_time - prev_time)
                    if (curr_time - prev_time) > 0
                    else 0
                )
                prev_time = curr_time

                if self.service.is_enable_mediapipe_pose():
                    # Preparação para MediaPipe
                    timestamp = int(time.time() * 1000)
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    mp_image = mp.Image(
                        image_format=mp.ImageFormat.SRGB, data=rgb_frame
                    )

                    # Processamento MediaPipe
                    result = self.mp_manager.detect(mp_image, timestamp)

                    if result.pose_landmarks:
                        # Suavização (agora aplicada a todos os pontos se desejar)
                        result.pose_landmarks = self.filter.smooth_landmarks(
                            result.pose_landmarks
                        )

                        for landmarks in result.pose_landmarks:
                            # Desenha Esqueleto Completo
                            mp_drawing.draw_landmarks(
                                frame,
                                self._convert_to_proto(landmarks),
                                mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(
                                    color=(0, 255, 0),
                                    thickness=2,
                                    circle_radius=2,
                                ),
                                mp_drawing.DrawingSpec(
                                    color=(0, 0, 255), thickness=2
                                ),
                            )

                            # Exibe Confiança dos Pés (Índices 31 e 32)
                            conf_esq = landmarks[31].visibility
                            conf_dir = landmarks[32].visibility
                            c_color = (
                                (0, 255, 0)
                                if (conf_esq + conf_dir) / 2 > 0.5
                                else (0, 0, 255)
                            )

                            if self.service.is_telemetry_enable_panel():
                                text = self.tr(
                                    "Rastreio Pés (%): {:.2f}"
                                ).format((conf_esq + conf_dir) / 2)
                                frame = self.put_text_unicode(
                                    frame,
                                    text,
                                    position=(
                                        15,
                                        50,
                                    ),  # Y um pouco menor porque o PIL usa o topo do texto
                                    font_size=22,
                                    color=c_color,
                                )

                # UI de Telemetria
                if self.service.is_telemetry_enable_panel():
                    fps_color = (0, 255, 0) if fps >= 15 else (0, 0, 255)
                    cv2.putText(
                        frame,
                        self.tr("FPS: {}").format(int(fps)),
                        (15, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        fps_color,
                        2,
                    )
                    cv2.putText(
                        frame,
                        self.tr("Brilho: {}").format(int(avg_brightness)),
                        (15, 105),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 0),
                        2,
                    )

                # Conversão para PySide
                display_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = display_rgb.shape
                qt_img = QImage(
                    display_rgb.data, w, h, ch * w, QImage.Format_RGB888
                )
                self.change_pixmap_signal.emit(qt_img.copy())
            else:
                self.error_signal.emit(
                    self.tr(
                        "Erro ao capturar imagem da câmera. Dispositivo desconectado.\nVerifique a conexão cabo e ou instalação da câmera.\nFeche a janela e tente novamente."
                    )
                )
                break

        cap.release()

    def stop(self):
        self.running = False
        self.wait()

    def put_text_unicode(
        self,
        img,
        text,
        position,
        font_size=20,
        color=(255, 255, 255),
        font_path=None,
    ):
        """Desenha texto com acentos no OpenCV usando PIL."""
        # Converte BGR (OpenCV) → RGB (PIL)
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Fonte (pode ser uma TrueType do sistema)
        if font_path is None:
            # Exemplos de fontes comuns no Linux/Windows
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)  # Linux
            except Exception:
                try:
                    font = ImageFont.truetype(
                        "arial.ttf", font_size
                    )  # Windows
                except Exception:
                    font = ImageFont.load_default()
        else:
            font = ImageFont.truetype(font_path, font_size)

        draw.text(position, text, font=font, fill=color[::-1])  # BGR → RGB

        # Converte de volta para OpenCV
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
