from collections import deque

import cv2
import numpy as np

from ttea.service import CalibrationService


class MediaPipeFilter:
    def __init__(self):  # Gamma mais suave por padrão
        self.service = CalibrationService()
        self.clahe = cv2.createCLAHE(
            clipLimit=self.service.get_filter_clahe_clip(),
            tileGridSize=(self.service.get_filter_clahe_grid()),
        )
        self.smoothing_frames = (
            self.service.get_filter_average_smooth_frames()
        )  # smoothing_frames
        self.history = {}

        # Pré-calcula Gamma
        inv_gamma = 1.0 / self.service.get_filter_gamma_factor()
        self.gamma_table = np.array(
            [((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]
        ).astype("uint8")

    def apply_enhancements(self, frame):
        """Analisa o brilho e decide quais filtros aplicar."""
        # Calcula o brilho médio da imagem (canal V do HSV)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        avg_brightness = np.mean(hsv[:, :, 2])

        # Se a imagem estiver escura (ex: < 100), aplica CLAHE para ajudar a IA
        # Se estiver em 'luz plena' (ex: > 150), aplica apenas um Gamma leve
        if avg_brightness < self.service.get_filter_clahe_lum_below():
            frame = self.apply_clahe(frame)

        if avg_brightness > self.service.get_filter_gamma_lum_above():
            frame = self.apply_gamma(frame)
        return frame

    def apply_clahe(self, frame):
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l_enhanced = self.clahe.apply(l)
        enhanced_lab = cv2.merge((l_enhanced, a, b))
        return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    def apply_gamma(self, frame):
        return cv2.LUT(frame, self.gamma_table)

    def smooth_landmarks(self, pose_landmarks_list):
        """Mantém a lógica de suavização existente."""
        if not pose_landmarks_list:
            self.history.clear()
            return []

        movement_threshold = self.service.get_filter_landmark_limit()

        for landmarks in pose_landmarks_list:
            # Agora suavizamos o corpo inteiro para evitar trepidação visual
            # mas mantemos o reset para movimentos bruscos nos pés
            for idx, pt in enumerate(landmarks):
                if idx not in self.history:
                    self.history[idx] = deque(maxlen=self.smoothing_frames)

                if len(self.history[idx]) > 0:
                    last_x, last_y = self.history[idx][-1]
                    distance = np.sqrt(
                        (pt.x - last_x) ** 2 + (pt.y - last_y) ** 2
                    )
                    if distance > movement_threshold:
                        self.history[idx].clear()

                self.history[idx].append((pt.x, pt.y))
                avg_coords = np.mean(self.history[idx], axis=0)
                pt.x = float(avg_coords[0])
                pt.y = float(avg_coords[1])

        return pose_landmarks_list
