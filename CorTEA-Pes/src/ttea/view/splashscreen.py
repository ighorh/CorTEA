"""
Splash screen module for application startup display.

This module provides a splash screen widget that displays an animated
progress bar and rotating status messages during application
initialization. It includes resource pre-loading for audio system
warm-up to tests sounds on personal games configuration.
"""

from PySide6.QtCore import QPropertyAnimation, Qt, QTimer
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QProgressBar, QSplashScreen, QWidget

from ttea.util import PathConfig


class SplashScreen(QSplashScreen):
    """
    Splash screen widget for application startup with animated progress.

    Displays a splash screen during application initialization with a
    status label and animated progress bar. Shows rotating status messages
    every 1.2 seconds and includes sound effect initialization.

    Attributes
    ----------
    status_label : QLabel
        Label widget displaying current loading status message.
    progress_bar : QProgressBar
        Progress bar widget with infinite animation effect during
        startup.
    animation : QPropertyAnimation
        Animation object controlling the progress bar's value with
        infinite loop.
    messages : list of str
        List of rotating status messages to display during loading.
    msg_index : int
        Current index in the messages list, used by the timer
        callback.
    timer : QTimer
        Timer object that triggers message updates every 1.2 seconds.

    Methods
    -------
    __init__()
        Initialize the splash screen with animated progress and
        messages.
    _update_geometry()
        Update positions and sizes of child widgets based on splash
        size.
    _next_message()
        Rotate to the next status message in the message list.
    finish(main_window)
        Complete the splash screen animation and close the widget.
    load_resource()
        Initialize sound effect resources for warm-up.
    resizeEvent(event)
        Handle resize events by updating widget geometry.

    Notes
    -----
    The progress bar operates in "indeterminate" mode (infinite
    animation) during startup. When finish() is called, it switches to
    determinate mode and shows 100% completion. The class supports
    localization through QCoreApplication.translate() calls
    (self.tr()).
    """

    def __init__(self) -> None:
        """
        Initialize the splash screen with animated progress and
        messages.

        Sets up the splash screen widget with TTea logo, status label,
        animated progress bar, and a timer for rotating status messages
        every 1.2 seconds.
        """
        pixmap = QPixmap(PathConfig.image("ttealogo"))
        if pixmap.isNull():
            # Fill with a black pixmap if the image fails to load
            pixmap = QPixmap(600, 400)
            pixmap.fill(Qt.black)

        super().__init__(pixmap)
        self.setWindowFlags(
            Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Label de status
        self.status_label = QLabel(self.tr("Iniciando aplicação..."), self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 15px;
                font-weight: bold;
                background: rgba(0, 0, 0, 160);
                padding: 8px;
                border-radius: 6px;
            }
        """)

        # Progress bar animated
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # mode "indeterminate" while loading
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid white;
                border-radius: 5px;
                background: rgba(0,0,0,180);
                height: 24px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:0.5 #00cc00, stop:1 #006600);
                border-radius: 3px;
            }
        """)

        self._update_geometry()

        # Infinite bar animation ("loading" effect)
        self.animation = QPropertyAnimation(self.progress_bar, b"value")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.setLoopCount(-1)  # repeats forever
        self.animation.start()

        # Message exchange every 1.2s
        self.messages = [
            self.tr("Iniciando aplicação..."),
            self.tr("Carregando módulos..."),
            self.tr("Inicializando interface..."),
            self.tr("Verificando configurações..."),
            self.tr("Quase lá..."),
        ]
        self.msg_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_message)
        self.timer.start(1200)

    def _update_geometry(self) -> None:
        """
        Update positions and sizes of child widgets based on splash
        size.

        Repositions the progress bar and status label relative to the
        current splash screen dimensions to maintain proper layout when
        the window is resized.

        Returns
        -------
        None
        """
        w = self.width()
        h = self.height()
        bar_w = int(w * 0.7)
        self.progress_bar.setGeometry((w - bar_w) // 2, h - 70, bar_w, 24)
        self.status_label.setGeometry(0, h - 110, w, 40)

    def _next_message(self) -> None:
        """
        Rotate to the next status message in the message list.

        Updates the status label with the next message in the rotation
        and increments the message index. Called by the internal timer
        every 1.2 seconds.

        Returns
        -------
        None
        """
        self.status_label.setText(self.messages[self.msg_index])
        self.msg_index = (self.msg_index + 1) % len(self.messages)

    def finish(self, main_window: QWidget) -> None:
        """
        Complete the splash screen animation and close the widget.

        Stops timers and animations, sets the progress bar to 100%
        completion, displays the final "Concluído!" message, and calls
        the parent QSplashScreen.finish() to properly close the splash
        screen and show the main window.

        Parameters
        ----------
        main_window : QWidget
            The main application window to display after splash closes.

        Returns
        -------
        None
        """

        self.load_resource()
        self.timer.stop()
        self.animation.stop()
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.status_label.setText(self.tr("Concluído!"))

        # Call the original Qt finish()
        super().finish(main_window)

    def load_resource(self) -> None:
        """
        Initialize sound effect resources for warm-up.

        Instantiates a QSoundEffect object to ensure audio system
        initialization before the main application starts. This prevents
        audio-related delays during gameplay.

        Returns
        -------
        None
        """
        # Warm up instance of sound libraries
        _ = QSoundEffect(self)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Handle resize events by updating widget geometry.

        Calls the parent resize event handler and updates the positions
        of child widgets (progress bar and status label) to maintain
        proper layout when the splash screen is resized.

        Parameters
        ----------
        event : QResizeEvent
            The resize event object containing size information.

        Returns
        -------
        None
        """
        super().resizeEvent(event)
        self._update_geometry()
