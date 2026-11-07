import time
from typing import TYPE_CHECKING, Dict, Optional

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PySide6.QtCore import QCoreApplication, QObject, QRect, Signal
from PySide6.QtGui import QImage, QPixmap

from ttea.model import CalibrationPoint
from ttea.service import CalibrationService
from ttea.util import PathConfig

if TYPE_CHECKING:
    from ttea.view import AutomaticCalibrationView

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class AutomaticCalibrationController(QObject):
    msg_info_signal = Signal(str)
    msg_warning_signal = Signal(str)
    msg_critical_signal = Signal(str)

    close_view_signal = Signal()

    def __init__(
        self,
        view: "AutomaticCalibrationView",
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
        self.modo_preview = False
        self.monitor_screen: str = QCoreApplication.translate(
            "AutomaticCalibrationController", "Tela de Monitoramento"
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
        # ========================================================================

        self.calibration_points = np.zeros((4, 2), dtype=np.int64)

    def numpy_to_pixmap(self, img: np.ndarray) -> QPixmap:
        """Converte um ndarray do OpenCV (Grayscale ou BGR) para QPixmap do PySide6."""
        if len(img.shape) == 2:  # Grayscale
            height, width = img.shape
            bytes_per_line = width
            q_img = QImage(
                img.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_Grayscale8,
            )
        else:  # BGR
            height, width, channels = img.shape
            bytes_per_line = channels * width
            q_img = QImage(
                img.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_BGR888,
            )

        return QPixmap.fromImage(q_img)

    def generate_board_pixmap(self) -> QPixmap:
        """
        Gera a imagem do tabuleiro ChArUco ajustada às dimensões do monitor/projetor
        e a converte para QPixmap para ser exibida na tela do PySide6.
        """
        screen_geometry = self.get_available_geometry_of_screen(
            self.monitor_index
        )
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        aruco_cols = self.service.get_automatic_num_columns()
        aruco_rows = self.service.get_automatic_num_rows()

        square_width = screen_width // aruco_cols
        square_height = screen_height // aruco_rows
        square_size_average = (square_width + square_height) / 2
        marker_size = int(
            square_size_average * self.service.get_automatic_multiplier()
        )

        aruco = cv2.aruco
        dictionary = aruco.getPredefinedDictionary(
            self.service.get_automatic_dictionary()
        )
        board = aruco.CharucoBoard(
            (aruco_cols, aruco_rows),
            square_size_average,
            marker_size,
            dictionary,
        )

        base_img = board.generateImage(
            (aruco_cols * 100, aruco_rows * 100),
            marginSize=self.service.get_automatic_margin(),
        )
        board_img = cv2.resize(
            base_img,
            (screen_width, screen_height),
            interpolation=cv2.INTER_NEAREST,
        )

        return self.numpy_to_pixmap(board_img)

    def _process_frame_geometry(
        self,
        frame: np.ndarray,
        detector: cv2.aruco.ArucoDetector,
        board: cv2.aruco.CharucoBoard,
        square_size_average: float,
        square_width: int,
        square_height: int,
        screen_width: int,
        screen_height: int,
    ) -> Optional[np.ndarray]:
        """
        Método auxiliar privado que processa um frame da câmera, detecta os marcadores
        ChArUco, estima a homografia e retorna os 4 vértices projetados da tela.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is None:
            return None

        try:
            retval, charuco_corners, charuco_ids = (
                cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
            )

            if retval < 4:
                return None

            chess_corners = board.getChessboardCorners()
            src_points = []
            dst_points = []

            for corner_id, detected_corner in zip(
                charuco_ids.flatten(), charuco_corners
            ):
                world_pt = chess_corners[corner_id][:2]
                pixel_x = (world_pt[0] / square_size_average) * square_width
                pixel_y = (world_pt[1] / square_size_average) * square_height

                src_points.append([pixel_x, pixel_y])
                dst_points.append(detected_corner[0])

            src_pts = np.array(src_points, dtype=np.float32)
            dst_pts = np.array(dst_points, dtype=np.float32)

            H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            if H is not None:
                rect_expandido = np.array(
                    [
                        [0, 0],
                        [screen_width, 0],
                        [0, screen_height],
                        [screen_width, screen_height],
                    ],
                    dtype=np.float32,
                ).reshape(-1, 1, 2)

                projected = cv2.perspectiveTransform(rect_expandido, H)
                return np.round(projected.reshape(4, 2)).astype(int)

        except Exception as e_charuco:
            mensagem = f"{self.tr('Aviso detecção Charuco.')}\nDetalhes: {str(e_charuco)}"
            self.msg_warning_signal.emit(mensagem)

        return None

    def _draw_quadrilateral(
        self, img: np.ndarray, vertices: np.ndarray, with_labels: bool = False
    ) -> None:
        """Desenha o polígono e os pontos identificadores no frame."""
        render_pts = np.array(
            [vertices[0], vertices[1], vertices[3], vertices[2]],
            dtype=np.int32,
        )
        cv2.polylines(img, [render_pts], True, (0, 255, 255), 4)

        for pt in vertices:
            cv2.circle(img, (pt[0], pt[1]), 10, (0, 0, 255), -1)

        if with_labels:
            rotulos = [
                ("SE", vertices[0], (-25, -15)),
                ("SD", vertices[1], (15, -15)),
                ("IE", vertices[2], (-25, 25)),
                ("ID", vertices[3], (15, 25)),
            ]
            for texto, pt, offset in rotulos:
                pos_x, pos_y = pt[0] + offset[0], pt[1] + offset[1]
                cv2.putText(
                    img,
                    texto,
                    (pos_x, pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 0),
                    3,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img,
                    texto,
                    (pos_x, pos_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

    def run_auto_calibration(self) -> None:
        """
        Lógica de leitura da câmera, detecção do ChArUco e cálculo da calibração.
        A exibição do tabuleiro é gerenciada pela View do PySide6.
        """
        cap = None
        try:
            # -------------------------------------------------
            # DETECÇÃO E MÉTRICAS DA TELA
            # -------------------------------------------------
            screen_geometry = self.get_available_geometry_of_screen(
                self.monitor_index
            )
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

            # -------------------------------------------------
            # CONFIGURAÇÃO DO CHARUCO
            # -------------------------------------------------
            aruco_cols = self.service.get_automatic_num_columns()
            aruco_rows = self.service.get_automatic_num_rows()

            square_width = screen_width // aruco_cols
            square_height = screen_height // aruco_rows
            square_size_average = (square_width + square_height) / 2
            marker_size = int(
                square_size_average * self.service.get_automatic_multiplier()
            )

            aruco = cv2.aruco
            dictionary = aruco.getPredefinedDictionary(
                self.service.get_automatic_dictionary()
            )
            board = aruco.CharucoBoard(
                (aruco_cols, aruco_rows),
                square_size_average,
                marker_size,
                dictionary,
            )

            # -------------------------------------------------
            # CONFIGURAÇÃO DA CÂMERA
            # -------------------------------------------------
            cap = cv2.VideoCapture(
                self.camera_index, self.service.get_opencv_capture_backend()
            )
            if not cap.isOpened():
                self.msg_critical_signal.emit(
                    self.tr("Não foi possível abrir a câmera.")
                )
                return

            detector = aruco.ArucoDetector(dictionary)
            cv2.namedWindow(self.monitor_screen, cv2.WINDOW_AUTOSIZE)

            last_camera_vertices = None
            frozen_frame = None

            # -------------------------------------------------
            # LOOP PRINCIPAL
            # -------------------------------------------------
            while True:
                if not self.modo_preview:
                    if not cap.isOpened():
                        self.msg_critical_signal.emit(
                            self.tr("Não foi possível abrir a câmera.")
                        )
                        break

                    ret, frame = cap.read()
                    if not ret:
                        self.msg_critical_signal.emit(
                            self.tr(
                                "Erro ao capturar imagem da câmera. Dispositivo desconectado.\nVerifique a conexão cabo e ou instalação da câmera.\nFeche a janela e tente novamente."
                            )
                        )
                        break

                    # Processamento da geometria utilizando o método modularizado
                    vertices = self._process_frame_geometry(
                        frame,
                        detector,
                        board,
                        square_size_average,
                        square_width,
                        square_height,
                        screen_width,
                        screen_height,
                    )

                    if vertices is not None:
                        last_camera_vertices = vertices
                        self._draw_quadrilateral(frame, vertices)

                    display_frame = frame.copy()
                    hud_lines = [
                        self.tr(
                            "Tecle [S] para ocultar a tela e capturar a imagem."
                        ),
                        self.tr(
                            "Tecle [ESC] para sair da tela de monitoramento."
                        ),
                        self.tr(
                            "Tecle [ALT+F4 ou CMD+W] para fechar a tela das figuras."
                        ),
                    ]

                    start_x_pos = 20  # Posição horizontal inicial
                    start_y_pos = 40  # Posição vertical da primeira linha
                    space_line = 30  # Distância vertical entre linhas

                    for i, line in enumerate(hud_lines):
                        y = start_y_pos + (i * space_line)
                        cv2.putText(
                            display_frame,
                            line,
                            (start_x_pos, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 0),
                            3,
                            cv2.LINE_AA,
                        )
                        cv2.putText(
                            display_frame,
                            line,
                            (start_x_pos, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 255),
                            1,
                            cv2.LINE_AA,
                        )
                else:
                    display_frame = frozen_frame.copy()
                    msg_hud = self.tr(
                        "Amostra: Tecle [ESC] para salvar | Tecle [R] para repetir."
                    )
                    cv2.putText(
                        display_frame,
                        msg_hud,
                        (22, 42),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 0, 0),
                        3,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        display_frame,
                        msg_hud,
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

                cv2.imshow(self.monitor_screen, display_frame)
                key = cv2.waitKey(1) & 0xFF

                # --- AÇÃO S: FECHAMENTO DA JANELA E CAPTURA LIMPA ---
                if (
                    key == ord("s") or key == ord("S")
                ) and not self.modo_preview:
                    cv2.destroyWindow(self.monitor_screen)
                    cv2.waitKey(1)

                    time.sleep(1.0)

                    # Descarte seguro de buffer com verificação de cabo puxado
                    buffer_ok = True
                    for _ in range(5):
                        if not cap.grab():
                            buffer_ok = False
                            break

                    if not buffer_ok:
                        self.msg_critical_signal.emit(
                            self.tr(
                                "Erro ao capturar imagem da câmera. Dispositivo desconectado.\nVerifique a conexão cabo e ou instalação da câmera.\nFeche a janela e tente novamente."
                            )
                        )
                        break

                    ret, clean_frame = cap.read()

                    if ret:
                        clean_vertices = self._process_frame_geometry(
                            clean_frame,
                            detector,
                            board,
                            square_size_average,
                            square_width,
                            square_height,
                            screen_width,
                            screen_height,
                        )

                        if clean_vertices is not None:
                            last_camera_vertices = clean_vertices
                            self._draw_quadrilateral(
                                clean_frame, clean_vertices, with_labels=True
                            )
                            frozen_frame = clean_frame.copy()
                            self.modo_preview = True
                            self.msg_info_signal.emit(
                                self.tr(
                                    "Sucesso! Captura realizada sem obstruções."
                                )
                            )
                        else:
                            self.msg_warning_signal.emit(
                                self.tr(
                                    "O Tabuleiro não pôde ser lido na foto limpa. Retornando..."
                                )
                            )
                    else:
                        self.msg_critical_signal.emit(
                            self.tr(
                                "Erro ao capturar imagem da câmera. Dispositivo desconectado.\nVerifique a conexão cabo e ou instalação da câmera.\nFeche a janela e tente novamente."
                            )
                        )
                        break

                    cv2.namedWindow(self.monitor_screen, cv2.WINDOW_AUTOSIZE)

                # --- AÇÃO R: VOLTA AO RASTREAMENTO REAL ---
                elif (
                    key == ord("r") or key == ord("R")
                ) and self.modo_preview:
                    self.modo_preview = False
                    frozen_frame = None
                    self.msg_warning_signal.emit(
                        self.tr("Captura descartada. Rastreamento reativado.")
                    )

                # --- AÇÃO ESC: SALVA E FECHA ---
                elif key == 27:
                    if self.modo_preview and last_camera_vertices is not None:
                        se, sd, ie, id_pt = last_camera_vertices

                        if self.service.is_automatic_mirror_mode():
                            largura_cam = frozen_frame.shape[1]
                            self.calibration_points = np.array(
                                [
                                    [largura_cam - se[0], se[1]],  # SD
                                    [largura_cam - sd[0], sd[1]],  # SE
                                    [largura_cam - ie[0], ie[1]],  # ID
                                    [largura_cam - id_pt[0], id_pt[1]],  # IE
                                ],
                                dtype=np.int64,
                            )
                        else:
                            self.calibration_points = np.array(
                                [sd, se, id_pt, ie], dtype=np.int64
                            )

                        self.create_calibration_point()
                    else:
                        self.msg_info_signal.emit(
                            self.tr("Fechando sem salvar.")
                        )
                    break

        except Exception as e:
            mensagem = f"{self.tr('Erro crítico na calibração automática.')}\nDetalhes: {str(e)}."
            self.msg_critical_signal.emit(mensagem)
        finally:
            if cap is not None and cap.isOpened():
                cap.release()
            cv2.destroyAllWindows()

    def get_available_geometry_of_screen(
        self, monitor_index: Optional[int] = None
    ) -> Optional[QRect]:
        if monitor_index is None:
            monitor_index = self.monitor_index
        return self.service.get_available_geometry_of_screen(monitor_index)

    def create_calibration_point(self) -> None:
        data = self.get_data()
        if self.service.create_calibration_point(data):
            self.msg_info_signal.emit(
                self.tr("Calibração automática cadastrada com sucesso!")
            )
        else:
            self.msg_critical_signal.emit(
                self.tr("Erro ao salvar os pontos da calibração automática.")
            )

    def get_data(self) -> Dict[str, int]:
        """Extrai os pontos de calibração utilizando as propriedades definidas no model."""
        flat_points = self.calibration_points.flatten().tolist()
        return {
            prop: int(val)
            for prop, val in zip(CalibrationPoint.PROPERTIES, flat_points)
        }
