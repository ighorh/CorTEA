# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playereditview.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QDialog, QFormLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QSpacerItem, QTabWidget, QTextEdit,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_PlayerEditView(object):
    def setupUi(self, PlayerEditView):
        if not PlayerEditView.objectName():
            PlayerEditView.setObjectName(u"PlayerEditView")
        PlayerEditView.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PlayerEditView.setWindowIcon(icon)
        PlayerEditView.setModal(True)
        self.main_layout = QVBoxLayout(PlayerEditView)
        self.main_layout.setObjectName(u"main_layout")
        self.tab_player = QTabWidget(PlayerEditView)
        self.tab_player.setObjectName(u"tab_player")
        self.tab_data = QWidget()
        self.tab_data.setObjectName(u"tab_data")
        self.details_layout = QFormLayout(self.tab_data)
        self.details_layout.setObjectName(u"details_layout")
        self.details_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_name = QLabel(self.tab_data)
        self.lbl_name.setObjectName(u"lbl_name")

        self.details_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_name)

        self.led_name = QLineEdit(self.tab_data)
        self.led_name.setObjectName(u"led_name")

        self.details_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.led_name)

        self.lbl_birth_date = QLabel(self.tab_data)
        self.lbl_birth_date.setObjectName(u"lbl_birth_date")

        self.details_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_birth_date)

        self.ded_birth_date = QDateEdit(self.tab_data)
        self.ded_birth_date.setObjectName(u"ded_birth_date")
        self.ded_birth_date.setCalendarPopup(True)
        self.ded_birth_date.setDate(QDate(2025, 9, 29))

        self.details_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.ded_birth_date)

        self.lbl_observation = QLabel(self.tab_data)
        self.lbl_observation.setObjectName(u"lbl_observation")

        self.details_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_observation)

        self.ted_observation = QTextEdit(self.tab_data)
        self.ted_observation.setObjectName(u"ted_observation")

        self.details_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.ted_observation)

        self.tab_player.addTab(self.tab_data, "")

        self.main_layout.addWidget(self.tab_player)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(PlayerEditView)
        self.pb_ok.setObjectName(u"pb_ok")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ok.sizePolicy().hasHeightForWidth())
        self.pb_ok.setSizePolicy(sizePolicy)
        self.pb_ok.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/okicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ok.setIcon(icon1)
        self.pb_ok.setAutoDefault(False)

        self.lay_button.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(PlayerEditView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        sizePolicy.setHeightForWidth(self.pb_cancel.sizePolicy().hasHeightForWidth())
        self.pb_cancel.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon2)
        self.pb_cancel.setAutoDefault(False)

        self.lay_button.addWidget(self.pb_cancel)


        self.main_layout.addLayout(self.lay_button)


        self.retranslateUi(PlayerEditView)

        self.tab_player.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PlayerEditView)
    # setupUi

    def retranslateUi(self, PlayerEditView):
        PlayerEditView.setWindowTitle(QCoreApplication.translate("PlayerEditView", u"Plataforma T-TEA - Jogador", None))
        self.lbl_name.setText(QCoreApplication.translate("PlayerEditView", u"Nome:", None))
        self.led_name.setPlaceholderText(QCoreApplication.translate("PlayerEditView", u"Nome", None))
        self.lbl_birth_date.setText(QCoreApplication.translate("PlayerEditView", u"Data de Nascimento:", None))
        self.ded_birth_date.setDisplayFormat(QCoreApplication.translate("PlayerEditView", u"dd/MM/yyyy", None))
        self.lbl_observation.setText(QCoreApplication.translate("PlayerEditView", u"Observa\u00e7\u00e3o:", None))
        self.ted_observation.setPlaceholderText(QCoreApplication.translate("PlayerEditView", u"Observa\u00e7\u00e3o", None))
        self.tab_player.setTabText(self.tab_player.indexOf(self.tab_data), QCoreApplication.translate("PlayerEditView", u"Dados", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("PlayerEditView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("PlayerEditView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("PlayerEditView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("PlayerEditView", u"Cancelar", None))
    # retranslateUi

