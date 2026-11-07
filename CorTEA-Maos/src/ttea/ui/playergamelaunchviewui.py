# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playergamelaunchview.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
                               QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_PlayerGameLaunchView(object):
    def setupUi(self, PlayerGameLaunchView):
        if not PlayerGameLaunchView.objectName():
            PlayerGameLaunchView.setObjectName(u"PlayerGameLaunchView")
        PlayerGameLaunchView.resize(480, 360)
        PlayerGameLaunchView.setMinimumSize(QSize(420, 300))
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PlayerGameLaunchView.setWindowIcon(icon)
        PlayerGameLaunchView.setModal(True)
        self.verticalLayout = QVBoxLayout(PlayerGameLaunchView)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 25, 30, 25)
        self.lbl_title = QLabel(PlayerGameLaunchView)
        self.lbl_title.setObjectName(u"lbl_title")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_title)

        self.vs_top = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.vs_top)

        self.frm_data = QFormLayout()
        self.frm_data.setObjectName(u"frm_data")
        self.frm_data.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.frm_data.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.frm_data.setHorizontalSpacing(12)
        self.frm_data.setVerticalSpacing(18)
        self.lbl_player = QLabel(PlayerGameLaunchView)
        self.lbl_player.setObjectName(u"lbl_player")
        font1 = QFont()
        font1.setPointSize(9)
        self.lbl_player.setFont(font1)

        self.frm_data.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_player)

        self.cbx_player = QComboBox(PlayerGameLaunchView)
        self.cbx_player.setObjectName(u"cbx_player")
        self.cbx_player.setMinimumSize(QSize(0, 0))
        self.cbx_player.setMaxVisibleItems(5)

        self.frm_data.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbx_player)

        self.lbl_professional = QLabel(PlayerGameLaunchView)
        self.lbl_professional.setObjectName(u"lbl_professional")
        self.lbl_professional.setFont(font1)

        self.frm_data.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_professional)

        self.cbx_professional = QComboBox(PlayerGameLaunchView)
        self.cbx_professional.setObjectName(u"cbx_professional")
        self.cbx_professional.setMinimumSize(QSize(0, 0))
        self.cbx_professional.setMaxVisibleItems(5)

        self.frm_data.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbx_professional)

        self.lbl_game = QLabel(PlayerGameLaunchView)
        self.lbl_game.setObjectName(u"lbl_game")
        self.lbl_game.setFont(font1)

        self.frm_data.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_game)

        self.lay_game = QHBoxLayout()
        self.lay_game.setSpacing(6)
        self.lay_game.setObjectName(u"lay_game")
        self.cbx_game = QComboBox(PlayerGameLaunchView)
        self.cbx_game.setObjectName(u"cbx_game")
        self.cbx_game.setMinimumSize(QSize(0, 0))
        self.cbx_game.setMaxVisibleItems(5)

        self.lay_game.addWidget(self.cbx_game)

        self.pb_game_info = QPushButton(PlayerGameLaunchView)
        self.pb_game_info.setObjectName(u"pb_game_info")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_game_info.sizePolicy().hasHeightForWidth())
        self.pb_game_info.setSizePolicy(sizePolicy)
        self.pb_game_info.setMinimumSize(QSize(28, 28))
        self.pb_game_info.setMaximumSize(QSize(28, 28))
        self.pb_game_info.setFont(font)

        self.lay_game.addWidget(self.pb_game_info)


        self.frm_data.setLayout(2, QFormLayout.ItemRole.FieldRole, self.lay_game)


        self.verticalLayout.addLayout(self.frm_data)

        self.vs_middle = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_middle)

        self.lay_button_play = QHBoxLayout()
        self.lay_button_play.setObjectName(u"lay_button_play")
        self.hs_left_button_play = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button_play.addItem(self.hs_left_button_play)

        self.pb_play = QPushButton(PlayerGameLaunchView)
        self.pb_play.setObjectName(u"pb_play")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.pb_play.setFont(font2)
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/playicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_play.setIcon(icon1)

        self.lay_button_play.addWidget(self.pb_play)

        self.hs_right_button_play = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button_play.addItem(self.hs_right_button_play)


        self.verticalLayout.addLayout(self.lay_button_play)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_cancel = QPushButton(PlayerGameLaunchView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        sizePolicy.setHeightForWidth(self.pb_cancel.sizePolicy().hasHeightForWidth())
        self.pb_cancel.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon2)

        self.lay_button.addWidget(self.pb_cancel)

        self.lay_button.setStretch(0, 1)

        self.verticalLayout.addLayout(self.lay_button)


        self.retranslateUi(PlayerGameLaunchView)

        QMetaObject.connectSlotsByName(PlayerGameLaunchView)
    # setupUi

    def retranslateUi(self, PlayerGameLaunchView):
        PlayerGameLaunchView.setWindowTitle(QCoreApplication.translate("PlayerGameLaunchView", u"Plataforma T-TEA - Iniciar Sess\u00e3o de Jogo", None))
        self.lbl_title.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Iniciar Sess\u00e3o de Jogo", None))
        self.lbl_player.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Jogador:", None))
        self.lbl_professional.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Profissional:", None))
        self.lbl_game.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Jogo:", None))
#if QT_CONFIG(tooltip)
        self.pb_game_info.setToolTip(QCoreApplication.translate("PlayerGameLaunchView", u"Informa\u00e7\u00f5es sobre o jogo", None))
#endif // QT_CONFIG(tooltip)
        self.pb_game_info.setText(QCoreApplication.translate("PlayerGameLaunchView", u"i", None))
#if QT_CONFIG(tooltip)
        self.pb_play.setToolTip(QCoreApplication.translate("PlayerGameLaunchView", u"Jogar", None))
#endif // QT_CONFIG(tooltip)
        self.pb_play.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Jogar", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("PlayerGameLaunchView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("PlayerGameLaunchView", u"Cancelar", None))
    # retranslateUi

