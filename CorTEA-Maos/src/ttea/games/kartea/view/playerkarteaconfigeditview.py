# Adjusted playerkarteaconfigeditview.py with single preview for visual feedback
from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import QCoreApplication, QEvent, Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QComboBox, QDialog

# Local module imports
from ttea.games.kartea.controller import PlayerKarteaConfigEditController
from ttea.games.kartea.service import PlayerKarteaConfigService
from ttea.games.kartea.ui import \
    Ui_PlayerKarteaConfigEditView  # Assuming the UI is in this module or adjust import
from ttea.games.kartea.util import KarteaPathConfig
from ttea.window import WindowConfig

if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaConfig


class PlayerKarteaConfigEditView(
    QDialog, Ui_PlayerKarteaConfigEditView, WindowConfig
):
    """Modal dialog for creating or editing a player Kartea config record.

    Loads UI from .ui file, applies consistent styling (icons, size, title),
    and delegates all validation and data handling to PlayerKarteaConfigEditController.

    Attributes
    ----------
    controller : PlayerKarteaConfigEditController
        Handles field initialization, validation, and data extraction.
    # ... (other widgets assigned from Ui)

    Methods
    -------
    __init__(parent=None, config=None)
        Initialize dialog, configure appearance, and create controller.
    update_image_preview(filename, preview_label)
        Update preview with selected image.
    play_sound(filename)
        Play selected sound.
    on_media_status_changed(status)
        Handle media status to play sound.
    update_levels()
        Update levels based on selected phase.
    """

    def __init__(
        self,
        parent=None,
        config: Optional["PlayerKarteaConfig"] = None,
        service: Optional[PlayerKarteaConfigService] = None,
    ):
        super().__init__(parent)
        self.setupUi(self)

        # Window config (mantém igual)
        action = self.tr("Novo")

        if config:
            action = self.tr("Editar")

        self.setup_window(
            f"{self.windowTitle()} - {action}",
            self.windowIcon(),
            WindowConfig.INCREMENT_SIZE_PERCENT,
            15,
            55,
            parent,
        )
        self.service = service or PlayerKarteaConfigService()

        # Controller
        self.controller = PlayerKarteaConfigEditController(self, config)

        self.pb_ok.clicked.connect(self.controller.handle_ok)
        self.pb_cancel.clicked.connect(self.controller.handle_cancel)

        self.cbx_current_phase.currentIndexChanged.connect(self.update_levels)

        self.combo_types = {
            self.cbx_vehicle_image: "Veículo",
            self.cbx_environment_image: "Ambiente",
            self.cbx_target_image: "Alvo",
            self.cbx_obstacle_image: "Obstáculo",
            self.cbx_positive_feedback_image: "Positivo",
            self.cbx_neutral_feedback_image: "Neutro",
            self.cbx_negative_feedback_image: "Negativo",
        }

        for combo in self.combo_types.keys():
            combo.installEventFilter(self)

        # ─── Conexões de preview – Recurso Visual (único) ───────────
        self.cbx_vehicle_image.currentTextChanged.connect(
            lambda text: self.update_resource_preview(text, "Veículo")
        )

        self.cbx_environment_image.currentTextChanged.connect(
            lambda text: self.update_resource_preview(text, "Ambiente")
        )

        self.cbx_target_image.currentTextChanged.connect(
            lambda text: self.update_resource_preview(text, "Alvo")
        )

        self.cbx_obstacle_image.currentTextChanged.connect(
            lambda text: self.update_resource_preview(text, "Obstáculo")
        )

        # Feedback visual (mantém igual – já usa preview único)
        self.cbx_positive_feedback_image.currentTextChanged.connect(
            lambda text: self.update_feedback_preview(text, "Positivo")
        )
        self.cbx_neutral_feedback_image.currentTextChanged.connect(
            lambda text: self.update_feedback_preview(text, "Neutro")
        )
        self.cbx_negative_feedback_image.currentTextChanged.connect(
            lambda text: self.update_feedback_preview(text, "Negativo")
        )

        # 1. Conectar a mudança de seleção ao pré-carregamento
        # Como está no QRC, o setSource fará o "unzip" do recurso para a RAM
        self.sound_positive = QSoundEffect(self)
        self.sound_neutral = QSoundEffect(self)
        self.sound_negative = QSoundEffect(self)

        self.cbx_positive_feedback_sound.currentTextChanged.connect(
            lambda t: self._prepare_qrc_sound(self.sound_positive, t)
        )
        self.cbx_neutral_feedback_sound.currentTextChanged.connect(
            lambda t: self._prepare_qrc_sound(self.sound_neutral, t)
        )
        self.cbx_negative_feedback_sound.currentTextChanged.connect(
            lambda t: self._prepare_qrc_sound(self.sound_negative, t)
        )

        # Carregamento inicial (para os itens já selecionados ao abrir o diálogo)
        self._prepare_qrc_sound(
            self.sound_positive, self.cbx_positive_feedback_sound.currentText()
        )
        self._prepare_qrc_sound(
            self.sound_neutral, self.cbx_neutral_feedback_sound.currentText()
        )
        self._prepare_qrc_sound(
            self.sound_negative, self.cbx_negative_feedback_sound.currentText()
        )

        # 2. Disparo imediato nos botões
        self.pb_positive_sound.clicked.connect(self.sound_positive.play)
        self.pb_neutral_sound.clicked.connect(self.sound_neutral.play)
        self.pb_negative_sound.clicked.connect(self.sound_negative.play)

        # Players
        players = self.service.get_all_players()
        self.cbx_player.addItems([p.name for p in players])

        # Opcional: estado inicial do preview de recursos
        self.lbl_visual_current_type.setText(
            "Selecione um recurso visual para visualizar"
        )
        self.lbl_visual_preview.clear()

    def _prepare_qrc_sound(self, effect: QSoundEffect, filename: str):
        """Carrega o som do recurso QRC para o buffer de memória."""
        if filename:
            # KarteaPathConfig.kartea_sound deve retornar algo como ":/sounds/nome.wav"
            path = KarteaPathConfig.game_builtin_sound(filename)

            # Para recursos QRC, usamos o QUrl direto com o esquema qrc
            url = QUrl(path)
            if not url.isValid():
                url = QUrl.fromLocalFile(path)  # Fallback caso não seja QRC

            effect.setSource(url)
            effect.setLoopCount(1)  # Garante que toque apenas uma vez
            QCoreApplication.processEvents()

    def update_resource_preview(
        self, filename: str, resource_type: str
    ) -> None:
        """Atualiza o preview único da aba Recurso Visual"""
        self.lbl_visual_current_type.setText(f"Visualizando: {resource_type}")

        if not filename or filename.strip() == "":
            self.lbl_visual_preview.clear()
            self.lbl_visual_preview.setText("Nenhuma imagem selecionada")
            return

        path = KarteaPathConfig.game_builtin_image(filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.lbl_visual_preview.clear()
            self.lbl_visual_preview.setText("Imagem não encontrada")
        else:
            scaled = pixmap.scaled(
                self.lbl_visual_preview.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.lbl_visual_preview.setPixmap(scaled)

    # Método update_feedback_preview → mantém praticamente igual (só ajustei nomes para clareza)
    def update_feedback_preview(
        self, filename: str, feedback_type: str
    ) -> None:
        self.lbl_current_feedback_type.setText(
            f"Feedback {feedback_type} – Pré-visualização"
        )

        if not filename:
            self.lbl_feedback_preview.clear()
            self.lbl_feedback_preview.setText("Nenhuma imagem selecionada")
            return

        path = KarteaPathConfig.game_builtin_image(filename)
        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.lbl_feedback_preview.clear()
            self.lbl_feedback_preview.setText("Imagem não encontrada")
        else:
            scaled = pixmap.scaled(
                self.lbl_feedback_preview.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.lbl_feedback_preview.setPixmap(scaled)

    def populate_comboboxes(self):
        for name, path in KarteaPathConfig.list_builtin_vehicle_images():
            self.cbx_vehicle_image.addItem(name, path)

        for name, path in KarteaPathConfig.list_builtin_environment_images():
            self.cbx_environment_image.addItem(name, path)

        for name, path in KarteaPathConfig.list_builtin_target_images():
            self.cbx_target_image.addItem(name, path)

        for name, path in KarteaPathConfig.list_builtin_obstacle_images():
            self.cbx_obstacle_image.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_positive_images():
            self.cbx_positive_feedback_image.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_neutral_images():
            self.cbx_neutral_feedback_image.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_negative_images():
            self.cbx_negative_feedback_image.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_positive_sounds():
            self.cbx_positive_feedback_sound.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_neutral_sounds():
            self.cbx_neutral_feedback_sound.addItem(name, path)

        for (
            name,
            path,
        ) in KarteaPathConfig.list_builtin_feedback_negative_sounds():
            self.cbx_negative_feedback_sound.addItem(name, path)

    def eventFilter(self, watched, event):
        # Verifica se o objeto "vigiado" é uma instância de QComboBox
        # Evento dispara quando o objeto ganha foco
        if isinstance(watched, QComboBox) and event.type() == QEvent.FocusIn:
            feedback_types = {"Positivo", "Neutro", "Negativo"}

            if self.combo_types.get(watched) in feedback_types:
                self.update_feedback_preview(
                    watched.currentText(),
                    self.combo_types.get(watched, "Desconhecido"),
                )
            else:
                self.update_resource_preview(
                    watched.currentText(),
                    self.combo_types.get(watched, "Desconhecido"),
                )
        return super().eventFilter(watched, event)

    def update_levels(self):
        """Update the cbx_current_level based on the selected phase."""
        phase_str = self.cbx_current_phase.currentText()
        self.cbx_current_level.clear()
        if phase_str:
            phase_id = int(phase_str)
            phase = self.service.get_phase(phase_id)
            if phase:
                levels = self.service.get_levels_for_phase(phase)
                self.cbx_current_level.addItems(
                    [str(level.id) for level in levels]
                )
