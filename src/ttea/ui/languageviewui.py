# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'languageview.ui'
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


class Ui_LanguageView(object):
    def setupUi(self, LanguageView):
        if not LanguageView.objectName():
            LanguageView.setObjectName(u"LanguageView")
        LanguageView.resize(300, 192)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        LanguageView.setWindowIcon(icon)
        LanguageView.setModal(True)
        self.verticalLayout = QVBoxLayout(LanguageView)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_instruction = QLabel(LanguageView)
        self.lbl_instruction.setObjectName(u"lbl_instruction")
        self.lbl_instruction.setStyleSheet(u"font-size: 14px;")
        self.lbl_instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_instruction)

        self.cbx_language = QComboBox(LanguageView)
        self.cbx_language.setObjectName(u"cbx_language")
        self.cbx_language.setMinimumSize(QSize(260, 40))
        self.cbx_language.setStyleSheet(u"QComboBox { padding-left: 10px; }")
        self.cbx_language.setMaxVisibleItems(5)
        self.cbx_language.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.cbx_language)

        self.vs_language = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_language)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.pb_ok = QPushButton(LanguageView)
        self.pb_ok.setObjectName(u"pb_ok")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ok.sizePolicy().hasHeightForWidth())
        self.pb_ok.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/okicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ok.setIcon(icon1)
        self.pb_ok.setIconSize(QSize(16, 16))
        self.pb_ok.setAutoDefault(True)
        self.pb_ok.setFlat(False)

        self.lay_button.addWidget(self.pb_ok)


        self.verticalLayout.addLayout(self.lay_button)


        self.retranslateUi(LanguageView)

        self.pb_ok.setDefault(False)


        QMetaObject.connectSlotsByName(LanguageView)
    # setupUi

    def retranslateUi(self, LanguageView):
        LanguageView.setWindowTitle(QCoreApplication.translate("LanguageView", u"Plataforma T-TEA", None))
        self.lbl_instruction.setText(QCoreApplication.translate("LanguageView", u"Selecione o idioma da aplica\u00e7\u00e3o:", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("LanguageView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("LanguageView", u"OK", None))
    # retranslateUi

