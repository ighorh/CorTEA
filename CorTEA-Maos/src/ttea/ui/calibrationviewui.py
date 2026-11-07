# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibrationview.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
                               QLabel, QPushButton, QSizePolicy, QSpacerItem,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_CalibrationView(object):
    def setupUi(self, CalibrationView):
        if not CalibrationView.objectName():
            CalibrationView.setObjectName(u"CalibrationView")
        CalibrationView.resize(796, 806)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        CalibrationView.setWindowIcon(icon)
        CalibrationView.setModal(True)
        self.verticalLayout = QVBoxLayout(CalibrationView)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.lay_combobox = QHBoxLayout()
        self.lay_combobox.setObjectName(u"lay_combobox")
        self.lbl_proportion = QLabel(CalibrationView)
        self.lbl_proportion.setObjectName(u"lbl_proportion")
        font = QFont()
        font.setBold(True)
        self.lbl_proportion.setFont(font)

        self.lay_combobox.addWidget(self.lbl_proportion)

        self.cbx_proportion = QComboBox(CalibrationView)
        self.cbx_proportion.setObjectName(u"cbx_proportion")
        self.cbx_proportion.setMinimumSize(QSize(140, 32))
        self.cbx_proportion.setMaxVisibleItems(5)

        self.lay_combobox.addWidget(self.cbx_proportion)

        self.lbl_monitor = QLabel(CalibrationView)
        self.lbl_monitor.setObjectName(u"lbl_monitor")
        self.lbl_monitor.setFont(font)

        self.lay_combobox.addWidget(self.lbl_monitor)

        self.cbx_monitor = QComboBox(CalibrationView)
        self.cbx_monitor.setObjectName(u"cbx_monitor")
        self.cbx_monitor.setMinimumSize(QSize(140, 32))
        self.cbx_monitor.setMaxVisibleItems(5)

        self.lay_combobox.addWidget(self.cbx_monitor)

        self.lbl_camera = QLabel(CalibrationView)
        self.lbl_camera.setObjectName(u"lbl_camera")
        self.lbl_camera.setFont(font)

        self.lay_combobox.addWidget(self.lbl_camera)

        self.cbx_camera = QComboBox(CalibrationView)
        self.cbx_camera.setObjectName(u"cbx_camera")
        self.cbx_camera.setMinimumSize(QSize(180, 32))
        self.cbx_camera.setMaxVisibleItems(5)

        self.lay_combobox.addWidget(self.cbx_camera)

        self.lay_combobox.setStretch(1, 1)
        self.lay_combobox.setStretch(3, 1)
        self.lay_combobox.setStretch(5, 1)

        self.verticalLayout.addLayout(self.lay_combobox)

        self.lbl_video = QLabel(CalibrationView)
        self.lbl_video.setObjectName(u"lbl_video")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_video.sizePolicy().hasHeightForWidth())
        self.lbl_video.setSizePolicy(sizePolicy)
        self.lbl_video.setMinimumSize(QSize(640, 480))
        self.lbl_video.setStyleSheet(u"background-color: black; color: white; font-size: 18px; border: 1px solid #444;")
        self.lbl_video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_video)

        self.pb_camera = QPushButton(CalibrationView)
        self.pb_camera.setObjectName(u"pb_camera")
        self.pb_camera.setMinimumSize(QSize(0, 42))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.pb_camera.setFont(font1)

        self.verticalLayout.addWidget(self.pb_camera)

        self.lay_calibration_buttons = QHBoxLayout()
        self.lay_calibration_buttons.setSpacing(8)
        self.lay_calibration_buttons.setObjectName(u"lay_calibration_buttons")
        self.pb_calibrate_auto = QPushButton(CalibrationView)
        self.pb_calibrate_auto.setObjectName(u"pb_calibrate_auto")
        self.pb_calibrate_auto.setMinimumSize(QSize(0, 38))
        self.pb_calibrate_auto.setFont(font1)

        self.lay_calibration_buttons.addWidget(self.pb_calibrate_auto)

        self.pb_calibrate_semi = QPushButton(CalibrationView)
        self.pb_calibrate_semi.setObjectName(u"pb_calibrate_semi")
        self.pb_calibrate_semi.setMinimumSize(QSize(0, 38))
        self.pb_calibrate_semi.setFont(font1)

        self.lay_calibration_buttons.addWidget(self.pb_calibrate_semi)

        self.pb_calibrate_manual = QPushButton(CalibrationView)
        self.pb_calibrate_manual.setObjectName(u"pb_calibrate_manual")
        self.pb_calibrate_manual.setMinimumSize(QSize(0, 38))
        self.pb_calibrate_manual.setFont(font1)

        self.lay_calibration_buttons.addWidget(self.pb_calibrate_manual)


        self.verticalLayout.addLayout(self.lay_calibration_buttons)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(CalibrationView)
        self.pb_ok.setObjectName(u"pb_ok")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pb_ok.sizePolicy().hasHeightForWidth())
        self.pb_ok.setSizePolicy(sizePolicy1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/okicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ok.setIcon(icon1)

        self.lay_button.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(CalibrationView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        sizePolicy1.setHeightForWidth(self.pb_cancel.sizePolicy().hasHeightForWidth())
        self.pb_cancel.setSizePolicy(sizePolicy1)
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon2)

        self.lay_button.addWidget(self.pb_cancel)

        self.lay_button.setStretch(0, 1)

        self.verticalLayout.addLayout(self.lay_button)


        self.retranslateUi(CalibrationView)

        QMetaObject.connectSlotsByName(CalibrationView)
    # setupUi

    def retranslateUi(self, CalibrationView):
        CalibrationView.setWindowTitle(QCoreApplication.translate("CalibrationView", u"Plataforma T-TEA - Calibra\u00e7\u00e3o", None))
        self.lbl_proportion.setText(QCoreApplication.translate("CalibrationView", u"Propor\u00e7\u00e3o:", None))
        self.lbl_monitor.setText(QCoreApplication.translate("CalibrationView", u"Monitor:", None))
        self.lbl_camera.setText(QCoreApplication.translate("CalibrationView", u"C\u00e2mera:", None))
        self.lbl_video.setText(QCoreApplication.translate("CalibrationView", u"V\u00eddeo aparecer\u00e1 aqui", None))
        self.pb_camera.setText(QCoreApplication.translate("CalibrationView", u"Iniciar C\u00e2mera - F5", None))
#if QT_CONFIG(shortcut)
        self.pb_camera.setShortcut(QCoreApplication.translate("CalibrationView", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.pb_calibrate_auto.setText(QCoreApplication.translate("CalibrationView", u"Calibra\u00e7\u00e3o Autom\u00e1tica - F6", None))
#if QT_CONFIG(shortcut)
        self.pb_calibrate_auto.setShortcut(QCoreApplication.translate("CalibrationView", u"F6", None))
#endif // QT_CONFIG(shortcut)
        self.pb_calibrate_semi.setText(QCoreApplication.translate("CalibrationView", u"Calibra\u00e7\u00e3o Semi-Autom\u00e1tica - F7", None))
#if QT_CONFIG(shortcut)
        self.pb_calibrate_semi.setShortcut(QCoreApplication.translate("CalibrationView", u"F7", None))
#endif // QT_CONFIG(shortcut)
        self.pb_calibrate_manual.setText(QCoreApplication.translate("CalibrationView", u"Calibra\u00e7\u00e3o Manual - F8", None))
#if QT_CONFIG(shortcut)
        self.pb_calibrate_manual.setShortcut(QCoreApplication.translate("CalibrationView", u"F8", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("CalibrationView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("CalibrationView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("CalibrationView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("CalibrationView", u"Cancelar", None))
    # retranslateUi

