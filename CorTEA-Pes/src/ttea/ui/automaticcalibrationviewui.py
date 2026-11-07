# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'automaticcalibrationview.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
                               QWidget)

import ttea.resources.resources_rc


class Ui_AutomaticCalibrationView(object):
    def setupUi(self, AutomaticCalibrationView):
        if not AutomaticCalibrationView.objectName():
            AutomaticCalibrationView.setObjectName(u"AutomaticCalibrationView")
        AutomaticCalibrationView.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AutomaticCalibrationView.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AutomaticCalibrationView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_image = QLabel(AutomaticCalibrationView)
        self.lbl_image.setObjectName(u"lbl_image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image.sizePolicy().hasHeightForWidth())
        self.lbl_image.setSizePolicy(sizePolicy)
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_image)


        self.retranslateUi(AutomaticCalibrationView)

        QMetaObject.connectSlotsByName(AutomaticCalibrationView)
    # setupUi

    def retranslateUi(self, AutomaticCalibrationView):
        AutomaticCalibrationView.setWindowTitle(QCoreApplication.translate("AutomaticCalibrationView", u"Plataforma T-TEA - Calibra\u00e7\u00e3o Autom\u00e1tica da Visualiza\u00e7\u00e3o da Tela do Jogo", None))
        self.lbl_image.setText("")
    # retranslateUi

