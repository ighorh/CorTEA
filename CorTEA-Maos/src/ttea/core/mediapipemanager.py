from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from ttea.service import CalibrationService
from ttea.util import PathConfig


class MediaPipeManager:
    def __init__(self):
        self.service = CalibrationService()

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

        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect(self, mp_image, timestamp_ms):
        """Executa a detecção de pose para um frame de vídeo."""
        return self.detector.detect_for_video(mp_image, timestamp_ms)
