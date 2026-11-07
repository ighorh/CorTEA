# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playerkarteaconfigeditview.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QFormLayout, QHBoxLayout, QLabel, QPushButton,
                               QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_PlayerKarteaConfigEditView(object):
    def setupUi(self, PlayerKarteaConfigEditView):
        if not PlayerKarteaConfigEditView.objectName():
            PlayerKarteaConfigEditView.setObjectName(u"PlayerKarteaConfigEditView")
        PlayerKarteaConfigEditView.resize(650, 633)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PlayerKarteaConfigEditView.setWindowIcon(icon)
        PlayerKarteaConfigEditView.setModal(True)
        self.main_layout = QVBoxLayout(PlayerKarteaConfigEditView)
        self.main_layout.setObjectName(u"main_layout")
        self.tab_widget = QTabWidget(PlayerKarteaConfigEditView)
        self.tab_widget.setObjectName(u"tab_widget")
        self.lay_game_setting = QWidget()
        self.lay_game_setting.setObjectName(u"lay_game_setting")
        self.tab_game_setting = QVBoxLayout(self.lay_game_setting)
        self.tab_game_setting.setObjectName(u"tab_game_setting")
        self.frm_game_setting = QFormLayout()
        self.frm_game_setting.setObjectName(u"frm_game_setting")
        self.frm_game_setting.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_player = QLabel(self.lay_game_setting)
        self.lbl_player.setObjectName(u"lbl_player")

        self.frm_game_setting.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_player)

        self.cbx_player = QComboBox(self.lay_game_setting)
        self.cbx_player.setObjectName(u"cbx_player")
        self.cbx_player.setEnabled(True)
        self.cbx_player.setMaxVisibleItems(5)

        self.frm_game_setting.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbx_player)

        self.lbl_session = QLabel(self.lay_game_setting)
        self.lbl_session.setObjectName(u"lbl_session")

        self.frm_game_setting.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_session)

        self.lbl_session_value = QLabel(self.lay_game_setting)
        self.lbl_session_value.setObjectName(u"lbl_session_value")

        self.frm_game_setting.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lbl_session_value)

        self.lbl_current_phase = QLabel(self.lay_game_setting)
        self.lbl_current_phase.setObjectName(u"lbl_current_phase")

        self.frm_game_setting.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_current_phase)

        self.cbx_current_phase = QComboBox(self.lay_game_setting)
        self.cbx_current_phase.setObjectName(u"cbx_current_phase")
        self.cbx_current_phase.setMaxVisibleItems(5)

        self.frm_game_setting.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbx_current_phase)

        self.lbl_current_level = QLabel(self.lay_game_setting)
        self.lbl_current_level.setObjectName(u"lbl_current_level")

        self.frm_game_setting.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_current_level)

        self.cbx_current_level = QComboBox(self.lay_game_setting)
        self.cbx_current_level.setObjectName(u"cbx_current_level")
        self.cbx_current_level.setMaxVisibleItems(5)

        self.frm_game_setting.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cbx_current_level)

        self.lbl_level_time = QLabel(self.lay_game_setting)
        self.lbl_level_time.setObjectName(u"lbl_level_time")

        self.frm_game_setting.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_level_time)

        self.spn_level_time = QSpinBox(self.lay_game_setting)
        self.spn_level_time.setObjectName(u"spn_level_time")
        self.spn_level_time.setMinimum(0)
        self.spn_level_time.setMaximum(999999)

        self.frm_game_setting.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spn_level_time)


        self.tab_game_setting.addLayout(self.frm_game_setting)

        self.vs_game_setting = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tab_game_setting.addItem(self.vs_game_setting)

        self.tab_widget.addTab(self.lay_game_setting, "")
        self.lay_visual_resources = QWidget()
        self.lay_visual_resources.setObjectName(u"lay_visual_resources")
        self.visual_resources_layout = QVBoxLayout(self.lay_visual_resources)
        self.visual_resources_layout.setSpacing(10)
        self.visual_resources_layout.setObjectName(u"visual_resources_layout")
        self.visual_resources_layout.setContentsMargins(10, 10, 10, 10)
        self.lbl_visual_current_type = QLabel(self.lay_visual_resources)
        self.lbl_visual_current_type.setObjectName(u"lbl_visual_current_type")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.lbl_visual_current_type.setFont(font)
        self.lbl_visual_current_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_visual_current_type.setMargin(10)

        self.visual_resources_layout.addWidget(self.lbl_visual_current_type)

        self.lbl_visual_preview = QLabel(self.lay_visual_resources)
        self.lbl_visual_preview.setObjectName(u"lbl_visual_preview")
        self.lbl_visual_preview.setMinimumSize(QSize(280, 280))
        self.lbl_visual_preview.setMaximumSize(QSize(350, 350))
        self.lbl_visual_preview.setStyleSheet(u"border: 2px solid #666666; background-color: #ffffff; border-radius: 10px;")
        self.lbl_visual_preview.setScaledContents(True)
        self.lbl_visual_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.visual_resources_layout.addWidget(self.lbl_visual_preview, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_preview = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.visual_resources_layout.addItem(self.verticalSpacer_preview)

        self.visual_form = QFormLayout()
        self.visual_form.setObjectName(u"visual_form")
        self.visual_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_vehicle_image = QLabel(self.lay_visual_resources)
        self.lbl_vehicle_image.setObjectName(u"lbl_vehicle_image")

        self.visual_form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_vehicle_image)

        self.cbx_vehicle_image = QComboBox(self.lay_visual_resources)
        self.cbx_vehicle_image.setObjectName(u"cbx_vehicle_image")
        self.cbx_vehicle_image.setEditable(True)
        self.cbx_vehicle_image.setMaxVisibleItems(5)

        self.visual_form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbx_vehicle_image)

        self.lbl_environment_image = QLabel(self.lay_visual_resources)
        self.lbl_environment_image.setObjectName(u"lbl_environment_image")

        self.visual_form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_environment_image)

        self.cbx_environment_image = QComboBox(self.lay_visual_resources)
        self.cbx_environment_image.setObjectName(u"cbx_environment_image")
        self.cbx_environment_image.setEditable(True)
        self.cbx_environment_image.setMaxVisibleItems(5)

        self.visual_form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbx_environment_image)

        self.lbl_target_image = QLabel(self.lay_visual_resources)
        self.lbl_target_image.setObjectName(u"lbl_target_image")

        self.visual_form.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_target_image)

        self.cbx_target_image = QComboBox(self.lay_visual_resources)
        self.cbx_target_image.setObjectName(u"cbx_target_image")
        self.cbx_target_image.setEditable(True)
        self.cbx_target_image.setMaxVisibleItems(5)

        self.visual_form.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbx_target_image)

        self.lbl_obstracle_image = QLabel(self.lay_visual_resources)
        self.lbl_obstracle_image.setObjectName(u"lbl_obstracle_image")

        self.visual_form.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_obstracle_image)

        self.cbx_obstacle_image = QComboBox(self.lay_visual_resources)
        self.cbx_obstacle_image.setObjectName(u"cbx_obstacle_image")
        self.cbx_obstacle_image.setEditable(True)
        self.cbx_obstacle_image.setMaxVisibleItems(5)

        self.visual_form.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cbx_obstacle_image)


        self.visual_resources_layout.addLayout(self.visual_form)

        self.vs_visual_resource = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.visual_resources_layout.addItem(self.vs_visual_resource)

        self.tab_widget.addTab(self.lay_visual_resources, "")
        self.lay_visual_feedback = QWidget()
        self.lay_visual_feedback.setObjectName(u"lay_visual_feedback")
        self.verticalLayout_visual_feedback = QVBoxLayout(self.lay_visual_feedback)
        self.verticalLayout_visual_feedback.setObjectName(u"verticalLayout_visual_feedback")
        self.lbl_current_feedback_type = QLabel(self.lay_visual_feedback)
        self.lbl_current_feedback_type.setObjectName(u"lbl_current_feedback_type")
        self.lbl_current_feedback_type.setFont(font)
        self.lbl_current_feedback_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_current_feedback_type.setMargin(10)

        self.verticalLayout_visual_feedback.addWidget(self.lbl_current_feedback_type, 0, Qt.AlignmentFlag.AlignHCenter)

        self.lbl_feedback_preview = QLabel(self.lay_visual_feedback)
        self.lbl_feedback_preview.setObjectName(u"lbl_feedback_preview")
        self.lbl_feedback_preview.setMinimumSize(QSize(280, 280))
        self.lbl_feedback_preview.setMaximumSize(QSize(350, 350))
        self.lbl_feedback_preview.setStyleSheet(u"border: 2px solid #666666; background-color: #ffffff; border-radius: 10px;")
        self.lbl_feedback_preview.setScaledContents(True)
        self.lbl_feedback_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_visual_feedback.addWidget(self.lbl_feedback_preview, 0, Qt.AlignmentFlag.AlignHCenter)

        self.vs_preview = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_visual_feedback.addItem(self.vs_preview)

        self.frm_visual_feedback = QFormLayout()
        self.frm_visual_feedback.setObjectName(u"frm_visual_feedback")
        self.frm_visual_feedback.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_positive_feedback_image = QLabel(self.lay_visual_feedback)
        self.lbl_positive_feedback_image.setObjectName(u"lbl_positive_feedback_image")

        self.frm_visual_feedback.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_positive_feedback_image)

        self.cbx_positive_feedback_image = QComboBox(self.lay_visual_feedback)
        self.cbx_positive_feedback_image.setObjectName(u"cbx_positive_feedback_image")
        self.cbx_positive_feedback_image.setEditable(True)
        self.cbx_positive_feedback_image.setMaxVisibleItems(5)

        self.frm_visual_feedback.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbx_positive_feedback_image)

        self.lbl_neutral_feedback_image = QLabel(self.lay_visual_feedback)
        self.lbl_neutral_feedback_image.setObjectName(u"lbl_neutral_feedback_image")

        self.frm_visual_feedback.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_neutral_feedback_image)

        self.cbx_neutral_feedback_image = QComboBox(self.lay_visual_feedback)
        self.cbx_neutral_feedback_image.setObjectName(u"cbx_neutral_feedback_image")
        self.cbx_neutral_feedback_image.setEditable(True)
        self.cbx_neutral_feedback_image.setMaxVisibleItems(5)

        self.frm_visual_feedback.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbx_neutral_feedback_image)

        self.lbl_negative_feedback_image = QLabel(self.lay_visual_feedback)
        self.lbl_negative_feedback_image.setObjectName(u"lbl_negative_feedback_image")

        self.frm_visual_feedback.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_negative_feedback_image)

        self.cbx_negative_feedback_image = QComboBox(self.lay_visual_feedback)
        self.cbx_negative_feedback_image.setObjectName(u"cbx_negative_feedback_image")
        self.cbx_negative_feedback_image.setEditable(True)
        self.cbx_negative_feedback_image.setMaxVisibleItems(5)

        self.frm_visual_feedback.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbx_negative_feedback_image)


        self.verticalLayout_visual_feedback.addLayout(self.frm_visual_feedback)

        self.vs_visual_feedback = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_visual_feedback.addItem(self.vs_visual_feedback)

        self.tab_widget.addTab(self.lay_visual_feedback, "")
        self.lay_sound_feedback = QWidget()
        self.lay_sound_feedback.setObjectName(u"lay_sound_feedback")
        self.vboxLayout = QVBoxLayout(self.lay_sound_feedback)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.frm_sound_feedback = QFormLayout()
        self.frm_sound_feedback.setObjectName(u"frm_sound_feedback")
        self.lbl_sound_feedback_positive = QLabel(self.lay_sound_feedback)
        self.lbl_sound_feedback_positive.setObjectName(u"lbl_sound_feedback_positive")

        self.frm_sound_feedback.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_sound_feedback_positive)

        self.lay_positive_feedback_sound = QHBoxLayout()
        self.lay_positive_feedback_sound.setObjectName(u"lay_positive_feedback_sound")
        self.cbx_positive_feedback_sound = QComboBox(self.lay_sound_feedback)
        self.cbx_positive_feedback_sound.setObjectName(u"cbx_positive_feedback_sound")
        self.cbx_positive_feedback_sound.setEditable(True)
        self.cbx_positive_feedback_sound.setMaxVisibleItems(5)

        self.lay_positive_feedback_sound.addWidget(self.cbx_positive_feedback_sound)

        self.pb_positive_sound = QPushButton(self.lay_sound_feedback)
        self.pb_positive_sound.setObjectName(u"pb_positive_sound")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/playicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_positive_sound.setIcon(icon1)

        self.lay_positive_feedback_sound.addWidget(self.pb_positive_sound)


        self.frm_sound_feedback.setLayout(0, QFormLayout.ItemRole.FieldRole, self.lay_positive_feedback_sound)

        self.lbl_sound_feedback_neutral = QLabel(self.lay_sound_feedback)
        self.lbl_sound_feedback_neutral.setObjectName(u"lbl_sound_feedback_neutral")

        self.frm_sound_feedback.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_sound_feedback_neutral)

        self.lay_neutral_feedback_sound = QHBoxLayout()
        self.lay_neutral_feedback_sound.setObjectName(u"lay_neutral_feedback_sound")
        self.cbx_neutral_feedback_sound = QComboBox(self.lay_sound_feedback)
        self.cbx_neutral_feedback_sound.setObjectName(u"cbx_neutral_feedback_sound")
        self.cbx_neutral_feedback_sound.setEditable(True)
        self.cbx_neutral_feedback_sound.setMaxVisibleItems(5)

        self.lay_neutral_feedback_sound.addWidget(self.cbx_neutral_feedback_sound)

        self.pb_neutral_sound = QPushButton(self.lay_sound_feedback)
        self.pb_neutral_sound.setObjectName(u"pb_neutral_sound")
        self.pb_neutral_sound.setIcon(icon1)

        self.lay_neutral_feedback_sound.addWidget(self.pb_neutral_sound)


        self.frm_sound_feedback.setLayout(1, QFormLayout.ItemRole.FieldRole, self.lay_neutral_feedback_sound)

        self.lbl_sound_feedback_negative = QLabel(self.lay_sound_feedback)
        self.lbl_sound_feedback_negative.setObjectName(u"lbl_sound_feedback_negative")

        self.frm_sound_feedback.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_sound_feedback_negative)

        self.lay_negative_feedback_sound = QHBoxLayout()
        self.lay_negative_feedback_sound.setObjectName(u"lay_negative_feedback_sound")
        self.cbx_negative_feedback_sound = QComboBox(self.lay_sound_feedback)
        self.cbx_negative_feedback_sound.setObjectName(u"cbx_negative_feedback_sound")
        self.cbx_negative_feedback_sound.setEditable(True)
        self.cbx_negative_feedback_sound.setMaxVisibleItems(5)

        self.lay_negative_feedback_sound.addWidget(self.cbx_negative_feedback_sound)

        self.pb_negative_sound = QPushButton(self.lay_sound_feedback)
        self.pb_negative_sound.setObjectName(u"pb_negative_sound")
        self.pb_negative_sound.setIcon(icon1)

        self.lay_negative_feedback_sound.addWidget(self.pb_negative_sound)


        self.frm_sound_feedback.setLayout(2, QFormLayout.ItemRole.FieldRole, self.lay_negative_feedback_sound)


        self.vboxLayout.addLayout(self.frm_sound_feedback)

        self.vs_sound_feedback = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vboxLayout.addItem(self.vs_sound_feedback)

        self.tab_widget.addTab(self.lay_sound_feedback, "")
        self.lay_interface_setting = QWidget()
        self.lay_interface_setting.setObjectName(u"lay_interface_setting")
        self.vboxLayout1 = QVBoxLayout(self.lay_interface_setting)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.frm_interface_setting = QFormLayout()
        self.frm_interface_setting.setObjectName(u"frm_interface_setting")
        self.lbl_palette = QLabel(self.lay_interface_setting)
        self.lbl_palette.setObjectName(u"lbl_palette")

        self.frm_interface_setting.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_palette)

        self.spn_palette = QSpinBox(self.lay_interface_setting)
        self.spn_palette.setObjectName(u"spn_palette")
        self.spn_palette.setMinimum(0)
        self.spn_palette.setMaximum(999999)

        self.frm_interface_setting.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spn_palette)

        self.lbl_hud = QLabel(self.lay_interface_setting)
        self.lbl_hud.setObjectName(u"lbl_hud")

        self.frm_interface_setting.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_hud)

        self.chk_hud = QCheckBox(self.lay_interface_setting)
        self.chk_hud.setObjectName(u"chk_hud")

        self.frm_interface_setting.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chk_hud)

        self.lbl_sound = QLabel(self.lay_interface_setting)
        self.lbl_sound.setObjectName(u"lbl_sound")

        self.frm_interface_setting.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_sound)

        self.chk_sound = QCheckBox(self.lay_interface_setting)
        self.chk_sound.setObjectName(u"chk_sound")

        self.frm_interface_setting.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chk_sound)


        self.vboxLayout1.addLayout(self.frm_interface_setting)

        self.vs_interface_setting = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.vboxLayout1.addItem(self.vs_interface_setting)

        self.tab_widget.addTab(self.lay_interface_setting, "")

        self.main_layout.addWidget(self.tab_widget)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(PlayerKarteaConfigEditView)
        self.pb_ok.setObjectName(u"pb_ok")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/okicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ok.setIcon(icon2)

        self.lay_button.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(PlayerKarteaConfigEditView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        icon3 = QIcon()
        icon3.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon3)

        self.lay_button.addWidget(self.pb_cancel)


        self.main_layout.addLayout(self.lay_button)


        self.retranslateUi(PlayerKarteaConfigEditView)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PlayerKarteaConfigEditView)
    # setupUi

    def retranslateUi(self, PlayerKarteaConfigEditView):
        PlayerKarteaConfigEditView.setWindowTitle(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Plataforma T-TEA - Configura\u00e7\u00e3o Kartea", None))
        self.lbl_player.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Jogador:", None))
        self.lbl_session.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Sess\u00e3o:", None))
        self.lbl_session_value.setText("")
        self.lbl_current_phase.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Fase Atual:", None))
        self.lbl_current_level.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"N\u00edvel Atual:", None))
        self.lbl_level_time.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Tempo de N\u00edvel:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lay_game_setting), QCoreApplication.translate("PlayerKarteaConfigEditView", u"Configura\u00e7\u00e3o de Jogo", None))
        self.lbl_visual_current_type.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Selecione um recurso visual para visualizar", None))
        self.lbl_visual_preview.setText("")
        self.lbl_vehicle_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem do Ve\u00edculo:", None))
        self.lbl_environment_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem do Ambiente:", None))
        self.lbl_target_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem do Alvo:", None))
        self.lbl_obstracle_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem do Obst\u00e1culo:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lay_visual_resources), QCoreApplication.translate("PlayerKarteaConfigEditView", u"Recurso Visual", None))
        self.lbl_current_feedback_type.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Selecione uma imagem de feedback para visualizar", None))
        self.lbl_feedback_preview.setText("")
        self.lbl_positive_feedback_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem de Feedback Positivo:", None))
        self.lbl_neutral_feedback_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem de Feedback Neutro:", None))
        self.lbl_negative_feedback_image.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Imagem de Feedback Negativo:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lay_visual_feedback), QCoreApplication.translate("PlayerKarteaConfigEditView", u"Feedback Visual", None))
        self.lbl_sound_feedback_positive.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Som de Feedback Positivo:", None))
        self.pb_positive_sound.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Play", None))
        self.lbl_sound_feedback_neutral.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Som de Feedback Neutro:", None))
        self.pb_neutral_sound.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Play", None))
        self.lbl_sound_feedback_negative.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Som de Feedback Negativo:", None))
        self.pb_negative_sound.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Play", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lay_sound_feedback), QCoreApplication.translate("PlayerKarteaConfigEditView", u"Feedback Sonoro", None))
        self.lbl_palette.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Paleta:", None))
        self.lbl_hud.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"HUD:", None))
        self.lbl_sound.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Som:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.lay_interface_setting), QCoreApplication.translate("PlayerKarteaConfigEditView", u"Configura\u00e7\u00e3o de Interface", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("PlayerKarteaConfigEditView", u"Cancelar", None))
    # retranslateUi

