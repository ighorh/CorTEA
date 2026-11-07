from typing import TYPE_CHECKING, Dict, Optional

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PySide6.QtCore import QCoreApplication, QObject, QRect, Qt, QTimer
from PySide6.QtGui import QKeyEvent, QPixmap

from ttea.model import AppModel, CalibrationPoint, Language
from ttea.service import CalibrationService
from ttea.util import PathConfig

if TYPE_CHECKING:
    from ttea.view import ManualCalibrationView

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class ManualCalibrationController(QObject):

    def __init__(
        self,
        view: "ManualCalibrationView",
        camera_index: int,
        monitor_index: int,
        service: Optional[CalibrationService] = None,
    ):
        super().__init__()
        self.view = view
        self.service = service or CalibrationService()
        self.monitor_index = monitor_index
        self.camera_index = camera_index
        self.camera = None
        self.monitor_screen: str = QCoreApplication.translate(
            "ManualCalibrationController", "Tela de Monitoramento"
        )

        # ==================== MediaPipe Tasks (Pose Landmarker) =============
        if self.service.is_raspberry_pi():
            model_path = PathConfig.model(
                self.service.get_mediapipe_model_embedded()
            )
        else:
            model_path = PathConfig.model(
                self.service.get_mediapipe_model_desktop()
            )

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=self.service.get_mediapipe_execution_mode(),
            num_poses=self.service.get_mediapipe_num_position(),
            min_pose_detection_confidence=self.service.get_mediapipe_detection_position(),
            min_pose_presence_confidence=self.service.get_mediapipe_detection_presence(),
            min_tracking_confidence=self.service.get_mediapipe_detection_tracking(),
        )
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)
        self.frame_timestamp = 0
        # ========================================================================

        self.calibration_points = np.zeros(
            (4, 2), dtype=np.int64
        )  # 4 pontos de calibração
        self.click_calibration_count = 0

        self.language_app = AppModel.get_instance().current_language
        for lang in Language.LANGUAGES:
            if self.language_app == lang["code"]:
                self._load_image(f"warning{lang['code'][:2]}")
                break

        # self._load_image("warningpt")
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self._update_camera_feed)

    def _setup_calibration_window(self):
        """Cria/restaura a janela do OpenCV e (re)vincula o callback do mouse."""
        cv2.namedWindow(self.monitor_screen, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.monitor_screen, self._mouse_click_callback)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_C:
            # Troca para imagem de calibração
            for lang in Language.LANGUAGES:
                if self.language_app == lang["code"]:
                    self._load_image(f"calibration{lang['code'][:2]}")
                    break

            # Inicia a câmera (se ainda não estiver aberta)
            if self.camera is None or not self.camera.isOpened():
                self.camera = cv2.VideoCapture(
                    self.camera_index,
                    self.service.get_opencv_capture_backend(),
                )
                if self.camera.isOpened():
                    self._setup_calibration_window()
                    self.camera_timer.start(30)
                else:
                    self.view.msg.critical(
                        self.tr("Não foi possível abrir a câmera.")
                    )
                    self.camera = None

        elif event.key() == Qt.Key_Q:
            self.view.close()

    def _mouse_click_callback(self, event, x, y, flags, param):
        """Callback para capturar cliques na janela da câmera"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.click_calibration_count < 4:
                self.calibration_points[self.click_calibration_count] = [x, y]
                self.click_calibration_count += 1

                if self.click_calibration_count == 4:
                    for lang in Language.LANGUAGES:
                        if self.language_app == lang["code"]:
                            self._load_image(
                                f"calibrationok{lang['code'][:2]}"
                            )
                            break
                    self.view.msg.info(
                        self.tr("Calibração concluída com sucesso!")
                    )

    def _load_image(self, image_name: str):
        """Carrega imagem via utilitário e exibe centralizada"""

        qimage = PathConfig.image(image_name)
        pixmap = QPixmap(qimage)

        self.view.lbl_image.setScaledContents(True)
        self.view.lbl_image.setPixmap(pixmap)

    def _update_camera_feed(self):
        """Atualiza o feed da câmera na janela do OpenCV"""
        from mediapipe.framework.formats import landmark_pb2

        if self.camera is not None and self.camera.isOpened():
            if (
                cv2.getWindowProperty(
                    self.monitor_screen, cv2.WND_PROP_VISIBLE
                )
                < 1
            ):
                self._setup_calibration_window()

            ret, frame = self.camera.read()
            if ret:
                # 1. Ajustar o frame (espelhar se necessário)
                if self.service.is_manual_mirror_mode():
                    control_screen = cv2.flip(frame, 1)
                else:
                    control_screen = frame

                if self.service.is_enable_mediapipe_pose():
                    # 2. Converter BGR para RGB (necessário para o MediaPipe)
                    rgb_frame = cv2.cvtColor(control_screen, cv2.COLOR_BGR2RGB)

                    # 3. Criar a estrutura mp.Image exigida pela Tasks API
                    mp_image = mp.Image(
                        image_format=mp.ImageFormat.SRGB, data=rgb_frame
                    )

                    # 4. Processar a imagem com PoseLandmarker
                    # Trata modo IMAGE ou VIDEO conforme configurado no service
                    if (
                        self.service.get_mediapipe_execution_mode()
                        == vision.RunningMode.VIDEO
                    ):
                        self.frame_timestamp += (
                            33  # Incremento aproximado para 30 FPS (ms)
                        )
                        detection_result = self.pose_detector.detect_for_video(
                            mp_image, self.frame_timestamp
                        )
                    else:
                        detection_result = self.pose_detector.detect(mp_image)

                    # 5. Desenhar o Esqueleto do MediaPipe se houver detecção
                    if detection_result.pose_landmarks:
                        for pose_landmarks in detection_result.pose_landmarks:
                            # Converte a estrutura de NormalizedLandmark para o formato do drawing_utils
                            pose_landmarks_proto = (
                                landmark_pb2.NormalizedLandmarkList()
                            )
                            pose_landmarks_proto.landmark.extend(
                                [
                                    landmark_pb2.NormalizedLandmark(
                                        x=landmark.x,
                                        y=landmark.y,
                                        z=landmark.z,
                                        visibility=landmark.visibility,
                                        presence=landmark.presence,
                                    )
                                    for landmark in pose_landmarks
                                ]
                            )

                            mp_drawing.draw_landmarks(
                                control_screen,  # Desenha diretamente na imagem BGR do OpenCV
                                pose_landmarks_proto,
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

                # 6. Desenhar os 4 pontos de calibração por cima
                for i in range(4):
                    cv2.circle(
                        control_screen,
                        tuple(self.calibration_points[i]),
                        8,
                        (255, 0, 0),  # Azul
                        -1,
                    )

                # 7. Desenhar retângulo de calibração caso finalizado
                if self.click_calibration_count == 4:
                    pts = self.calibration_points
                    cv2.line(
                        control_screen,
                        tuple(pts[0]),
                        tuple(pts[1]),
                        (0, 255, 0),
                        2,
                    )
                    cv2.line(
                        control_screen,
                        tuple(pts[1]),
                        tuple(pts[3]),
                        (0, 255, 0),
                        2,
                    )
                    cv2.line(
                        control_screen,
                        tuple(pts[2]),
                        tuple(pts[0]),
                        (0, 255, 0),
                        2,
                    )
                    cv2.line(
                        control_screen,
                        tuple(pts[2]),
                        tuple(pts[3]),
                        (0, 255, 0),
                        2,
                    )

                # Exibe o frame com esqueleto e pontos na janela
                cv2.imshow(self.monitor_screen, control_screen)

            else:
                self.view.msg.critical(
                    self.tr("Falha ao capturar imagem da câmera.")
                )

    def get_available_geometry_of_screen(
        self, monitor_index: Optional[int] = None
    ) -> Optional[QRect]:
        if monitor_index is None:
            monitor_index = self.monitor_index
        return self.service.get_available_geometry_of_screen(monitor_index)

    def create_calibration_point(self) -> None:
        data = self.get_data()
        if self.service.create_calibration_point(data):
            self.view.msg.info(
                self.tr("Calibração manual cadastrada com sucesso!")
            )
        else:
            self.view.msg.critical(
                self.tr("Erro ao salvar os pontos da calibração manual.")
            )

    def get_data(self) -> Dict[str, int]:
        """Extrai os pontos de calibração
        utilizando as propriedades definidas no model."""
        # Transforma a matriz (4, 2) em uma lista unidimensional
        # de 8 elementos [x1, y1, x2, y2, ...]
        flat_points = self.calibration_points.flatten().tolist()

        # Mapeia dinamicamente cada propriedade de CalibrationPoint.PROPERTIES ao valor capturado
        return {
            prop: int(val)
            for prop, val in zip(CalibrationPoint.PROPERTIES, flat_points)
        }
