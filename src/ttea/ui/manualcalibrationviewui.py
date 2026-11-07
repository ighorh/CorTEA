# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manualcalibrationview.ui'
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


class Ui_ManualCalibrationView(object):
    def setupUi(self, ManualCalibrationView):
        if not ManualCalibrationView.objectName():
            ManualCalibrationView.setObjectName(u"ManualCalibrationView")
        ManualCalibrationView.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ManualCalibrationView.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ManualCalibrationView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_image = QLabel(ManualCalibrationView)
        self.lbl_image.setObjectName(u"lbl_image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image.sizePolicy().hasHeightForWidth())
        self.lbl_image.setSizePolicy(sizePolicy)
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_image)


        self.retranslateUi(ManualCalibrationView)

        QMetaObject.connectSlotsByName(ManualCalibrationView)
    # setupUi

    def retranslateUi(self, ManualCalibrationView):
        ManualCalibrationView.setWindowTitle(QCoreApplication.translate("ManualCalibrationView", u"Plataforma T-TEA - Calibra\u00e7\u00e3o da Visualiza\u00e7\u00e3o da Tela do Jogo", None))
        self.lbl_image.setText("")
    # retranslateUi

