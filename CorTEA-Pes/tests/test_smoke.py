import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import cv2
import pygame
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QApplication, QMainWindow

from ttea.games.kartea.gamecore.camera import camera_backend
from ttea.games.kartea.gameutil.alphablit import alpha_blit_flags
from ttea.main import App
from ttea.ui import Ui_MainView
from ttea.util import PathConfig


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QApplication.instance() or QApplication([])

    def test_application_components_load(self):
        self.assertIsNotNone(App)

        window = QMainWindow()
        Ui_MainView().setupUi(window)

        self.assertTrue(QFile(":/icons/system/appicon").exists())
        self.assertTrue(
            (PathConfig.MODELS_DIR / "pose_landmarker_full.task").is_file()
        )

        window.close()

    def test_camera_uses_native_backends(self):
        with patch("ttea.games.kartea.gamecore.camera.sys.platform", "win32"):
            self.assertEqual(camera_backend(), cv2.CAP_DSHOW)

        with patch("ttea.games.kartea.gamecore.camera.sys.platform", "darwin"):
            self.assertEqual(camera_backend(), cv2.CAP_AVFOUNDATION)

        with patch("ttea.games.kartea.gamecore.camera.sys.platform", "linux"):
            self.assertEqual(camera_backend(), cv2.CAP_V4L2)

        with patch(
            "ttea.games.kartea.gamecore.camera.sys.platform", "freebsd14"
        ):
            self.assertEqual(camera_backend(), cv2.CAP_ANY)

    def test_macos_uses_sdl2_alpha_blitter(self):
        with patch(
            "ttea.games.kartea.gameutil.alphablit.sys.platform", "darwin"
        ):
            self.assertEqual(alpha_blit_flags(), pygame.BLEND_ALPHA_SDL2)

        with patch(
            "ttea.games.kartea.gameutil.alphablit.sys.platform", "win32"
        ):
            self.assertEqual(alpha_blit_flags(), 0)


if __name__ == "__main__":
    unittest.main()
