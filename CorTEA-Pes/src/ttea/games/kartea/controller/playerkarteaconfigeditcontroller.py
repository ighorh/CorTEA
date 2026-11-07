# Adjusted playerkarteaconfigeditcontroller.py
from typing import TYPE_CHECKING, Dict, Optional, Union

from PySide6.QtCore import QObject

from ttea.games.kartea.model import PlayerKarteaConfig
from ttea.games.kartea.model.karteaphase import KarteaPhase
from ttea.games.kartea.model.karteaphaselevel import KarteaPhaseLevel
from ttea.games.kartea.service import PlayerKarteaConfigService
from ttea.games.kartea.util import KarteaPathConfig
# Local module imports
from ttea.util import MessageService

if TYPE_CHECKING:
    from ttea.games.kartea.model import PlayerKarteaSession
    from ttea.games.kartea.view import PlayerKarteaConfigEditView
    from ttea.model import Player


class PlayerKarteaConfigEditController(QObject):
    """Controller for the player Kartea config edit/create dialog.

    Manages the interaction between PlayerKarteaConfigEditView and the PlayerKarteaConfig model,
    including field population, input validation, and data extraction.

    Attributes
    ----------
    view : PlayerKarteaConfigEditView
        The dialog view containing the input widgets.
    config : Optional[PlayerKarteaConfig]
        Config instance being edited, or None when creating a new config.
    ok_clicked : bool
        True if the dialog was accepted with valid data.
    msg : MessageService
        Service used to display validation/error messages.

    Methods
    -------
    __init__(view, config=None, player_list_controller=None, message_service=None)
        Initialize controller and populate fields if editing.
    handle_ok()
        Validate inputs and accept dialog if valid.
    handle_cancel()
        Reject dialog without saving changes.
    is_input_valid()
        Check required fields and show errors if needed.
    get_data()
        Extract entered data as a dictionary.
    """

    def __init__(
        self,
        view: "PlayerKarteaConfigEditView",
        config: Optional["PlayerKarteaConfig"] = None,
        service: Optional[PlayerKarteaConfigService] = None,
        message_service: Optional[MessageService] = None,
    ) -> None:
        """Initialize the controller and prepare the dialog.

        Stores references, sets the ok_clicked flag, and pre-fills the
        form when editing an existing config.

        Parameters
        ----------
        view : PlayerKarteaConfigEditView
            The associated dialog view.
        config : Optional[PlayerKarteaConfig], optional
            Config object to edit; None creates a new config.
        message_service : Optional[MessageService], optional
            Custom message service; defaults to MessageService(view).
        """
        super().__init__()

        self.view = view
        self.config = config
        self.ok_clicked = False
        self.service = service or PlayerKarteaConfigService()
        self.msg = message_service or MessageService(view)

        # Populate resources
        self.view.populate_comboboxes()

        # Populate phase combo box with phase IDs
        phases = self.service.get_all_phases()
        self.view.cbx_current_phase.clear()
        self.view.cbx_current_phase.addItems([str(p.id) for p in phases])

        # Populate fields
        if self.config:
            self.view.cbx_player.setCurrentText(
                self.config.player.name if self.config.player else ""
            )
            self.view.lbl_session_value.setText(
                str(self.config.session.id) if self.config.session else ""
            )
            self.view.cbx_current_phase.setCurrentText(
                str(self.config.phase.id) if self.config.phase else ""
            )
            self.view.update_levels()
            self.view.cbx_current_level.setCurrentText(
                str(self.config.level.id) if self.config.level else ""
            )
            self.view.spn_level_time.setValue(self.config.level_time)
            self.view.cbx_vehicle_image.setCurrentText(self.config.car_image)
            self.view.cbx_environment_image.setCurrentText(
                self.config.environment_image
            )
            self.view.cbx_target_image.setCurrentText(self.config.target_image)
            self.view.cbx_obstacle_image.setCurrentText(
                self.config.obstacle_image
            )
            self.view.cbx_positive_feedback_image.setCurrentText(
                self.config.positive_feedback_image
            )
            self.view.cbx_neutral_feedback_image.setCurrentText(
                self.config.neutral_feedback_image
            )
            self.view.cbx_negative_feedback_image.setCurrentText(
                self.config.negative_feedback_image
            )
            self.view.cbx_positive_feedback_sound.setCurrentText(
                self.config.positive_feedback_sound
            )
            self.view.cbx_neutral_feedback_sound.setCurrentText(
                self.config.neutral_feedback_sound
            )
            self.view.cbx_negative_feedback_sound.setCurrentText(
                self.config.negative_feedback_sound
            )
            self.view.spn_palette.setValue(self.config.palette)
            self.view.chk_hud.setChecked(self.config.hud)
            self.view.chk_sound.setChecked(self.config.sound)
        else:
            default_config = self.get_kartea_ini_config()
            self.view.cbx_player.setCurrentText("")
            self.view.lbl_session_value.setText("")

            default_phase_id = int(
                default_config["game_settings"]["phase_default"]
            )
            default_phase = self.service.get_phase(default_phase_id)
            self.view.cbx_current_phase.setCurrentText(
                str(default_phase.id) if default_phase else ""
            )
            self.view.update_levels()
            default_level_id = int(
                default_config["game_settings"]["level_default"]
            )
            levels = self.service.get_levels_for_phase(default_phase)
            default_level = next(
                (level for level in levels if level.id == default_level_id),
                None,
            )
            self.view.cbx_current_level.setCurrentText(
                str(default_level.id) if default_level else ""
            )
            self.view.spn_level_time.setValue(
                int(default_config["game_settings"]["level_time_default"])
            )
            self.view.cbx_vehicle_image.setCurrentText(
                default_config["visual_resources"]["vehicle_image_default"]
            )
            self.view.cbx_environment_image.setCurrentText(
                default_config["visual_resources"]["environment_image_default"]
            )
            self.view.cbx_target_image.setCurrentText(
                default_config["visual_resources"]["target_image_default"]
            )
            self.view.cbx_obstacle_image.setCurrentText(
                default_config["visual_resources"]["obstacle_image_default"]
            )
            self.view.cbx_positive_feedback_image.setCurrentText(
                default_config["visual_feedback"][
                    "positive_feedback_image_default"
                ]
            )
            self.view.cbx_neutral_feedback_image.setCurrentText(
                default_config["visual_feedback"][
                    "neutral_feedback_image_default"
                ]
            )
            self.view.cbx_negative_feedback_image.setCurrentText(
                default_config["visual_feedback"][
                    "negative_feedback_image_default"
                ]
            )
            self.view.cbx_positive_feedback_sound.setCurrentText(
                default_config["sound_feedback"][
                    "positive_feedback_sound_default"
                ]
            )
            self.view.cbx_neutral_feedback_sound.setCurrentText(
                default_config["sound_feedback"][
                    "neutral_feedback_sound_default"
                ]
            )
            self.view.cbx_negative_feedback_sound.setCurrentText(
                default_config["sound_feedback"][
                    "negative_feedback_sound_default"
                ]
            )
            self.view.spn_palette.setValue(
                int(default_config["interface_settings"]["palette_default"])
            )
            self.view.chk_hud.setChecked(
                default_config["interface_settings"]["hud_default"].lower()
                == "true"
            )
            self.view.chk_sound.setChecked(
                default_config["interface_settings"]["sound_default"].lower()
                == "true"
            )

    def handle_ok(self) -> None:
        """Validate input and close dialog with acceptance.

        If validation passes, sets ok_clicked to True and accepts the
        dialog. Otherwise shows a critical message with errors.
        """
        if self.is_input_valid():
            self.ok_clicked = True
            self.view.accept()

    def handle_cancel(self) -> None:
        """Close the dialog without saving changes.

        Rejects the dialog, discarding any entered data.
        """
        self.view.reject()

    def is_input_valid(self) -> bool:
        """Validate required fields.

        Checks that required fields are not empty. Shows a
        critical message listing all errors if validation fails.

        Returns
        -------
        bool
            True if all inputs are valid, False otherwise.
        """
        error_message = ""

        if not self.view.cbx_player.currentText():
            error_message += self.tr("Jogador é obrigatório!\n")
        if not self.view.cbx_vehicle_image.currentText():
            error_message += self.tr("Imagem do veículo é obrigatória!\n")
        if not self.view.cbx_environment_image.currentText():
            error_message += self.tr("Imagem do ambiente é obrigatória!\n")
        if not self.view.cbx_target_image.currentText():
            error_message += self.tr("Imagem do alvo é obrigatória!\n")
        if not self.view.cbx_obstacle_image.currentText():
            error_message += self.tr("Imagem do obstáculo é obrigatória!\n")

        if error_message:
            self.msg.critical(
                self.tr("Por favor, corrija os dados inválidos:\n")
                + error_message
            )
            return False
        return True

    def get_data(
        self,
    ) -> Dict[
        str,
        Union[
            str,
            int,
            bool,
            "Player",
            "PlayerKarteaSession",
            "KarteaPhase",
            "KarteaPhaseLevel",
        ],
    ]:
        """Extract current form values into a dictionary.

        Returns
        -------
        dict
            Mapping with keys for config attributes.
        """
        player_name = self.view.cbx_player.currentText()
        player = next(
            (
                p
                for p in self.service.get_all_players()
                if p.name == player_name
            ),
            None,
        )

        session_text = self.view.lbl_session_value.text()
        session = (
            self.service.get_session(int(session_text))
            if session_text and session_text.isdigit()
            else None
        )

        phase_text = self.view.cbx_current_phase.currentText()
        phase = (
            self.service.get_phase(int(phase_text))
            if phase_text and phase_text.isdigit()
            else None
        )

        level_text = self.view.cbx_current_level.currentText()
        level = (
            self.service.get_level_by_ids(int(phase_text), int(level_text))
            if level_text and level_text.isdigit()
            else None
        )

        return {
            "player_id": player.id,
            "session_id": session.id if session else None,
            "phase_id": phase.id,
            "level_id": level.id,
            "level_time": self.view.spn_level_time.value(),
            "car_image": self.view.cbx_vehicle_image.currentText(),
            "environment_image": self.view.cbx_environment_image.currentText(),
            "target_image": self.view.cbx_target_image.currentText(),
            "obstacle_image": self.view.cbx_obstacle_image.currentText(),
            "positive_feedback_image": self.view.cbx_positive_feedback_image.currentText(),
            "neutral_feedback_image": self.view.cbx_neutral_feedback_image.currentText(),
            "negative_feedback_image": self.view.cbx_negative_feedback_image.currentText(),
            "positive_feedback_sound": self.view.cbx_positive_feedback_sound.currentText(),
            "neutral_feedback_sound": self.view.cbx_neutral_feedback_sound.currentText(),
            "negative_feedback_sound": self.view.cbx_negative_feedback_sound.currentText(),
            "palette": self.view.spn_palette.value(),
            "hud": self.view.chk_hud.isChecked(),
            "sound": self.view.chk_sound.isChecked(),
        }

    def get_kartea_ini_config(self) -> Dict[str, str]:
        return KarteaPathConfig.read_config()
