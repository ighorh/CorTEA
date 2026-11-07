# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutview.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
                               QSizePolicy, QSpacerItem, QTextBrowser,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_AboutView(object):
    def setupUi(self, AboutView):
        if not AboutView.objectName():
            AboutView.setObjectName(u"AboutView")
        AboutView.resize(400, 504)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        AboutView.setWindowIcon(icon)
        AboutView.setSizeGripEnabled(False)
        AboutView.setModal(True)
        self.verticalLayout = QVBoxLayout(AboutView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_project = QLabel(AboutView)
        self.lbl_project.setObjectName(u"lbl_project")
        self.lbl_project.setStyleSheet(u"QLabel {\n"
"      font-size: 14px;\n"
"      padding: 5px;\n"
"      margin: 0px;\n"
"  }")
        self.lbl_project.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_project.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_project)

        self.vs_top = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_top)

        self.lbl_image = QLabel(AboutView)
        self.lbl_image.setObjectName(u"lbl_image")
        self.lbl_image.setMinimumSize(QSize(200, 100))
        self.lbl_image.setMaximumSize(QSize(200, 100))
        self.lbl_image.setPixmap(QPixmap(u":/images/ttealogo"))
        self.lbl_image.setScaledContents(True)
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_image, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.vs_top2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_top2)

        self.teb_link = QTextBrowser(AboutView)
        self.teb_link.setObjectName(u"teb_link")
        self.teb_link.setMinimumSize(QSize(0, 40))
        self.teb_link.setMaximumSize(QSize(16777215, 40))
        self.teb_link.setStyleSheet(u"QTextBrowser {\n"
"      font-size: 14px;\n"
"      padding: 5px;\n"
"      margin: 0px;\n"
"      border: none;\n"
"      background: transparent;\n"
"  }")
        self.teb_link.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.teb_link)

        self.vs_middle = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_middle)

        self.lbl_developer = QTextBrowser(AboutView)
        self.lbl_developer.setObjectName(u"lbl_developer")
        self.lbl_developer.setMinimumSize(QSize(0, 120))
        self.lbl_developer.setMaximumSize(QSize(16777215, 120))

        self.verticalLayout.addWidget(self.lbl_developer)

        self.vs_bottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_bottom)

        self.pb_ok = QPushButton(AboutView)
        self.pb_ok.setObjectName(u"pb_ok")
        self.pb_ok.setMinimumSize(QSize(100, 0))
        self.pb_ok.setMaximumSize(QSize(100, 16777215))
        self.pb_ok.setStyleSheet(u"QPushButton {\n"
"      font-size: 14px;\n"
"      padding: 5px;\n"
"      margin: 5px;\n"
"  }")

        self.verticalLayout.addWidget(self.pb_ok, 0, Qt.AlignmentFlag.AlignHCenter)

        self.vs_bottom2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.vs_bottom2)


        self.retranslateUi(AboutView)
        self.pb_ok.clicked.connect(AboutView.accept)

        QMetaObject.connectSlotsByName(AboutView)
    # setupUi

    def retranslateUi(self, AboutView):
        AboutView.setWindowTitle(QCoreApplication.translate("AboutView", u"Plataforma T-TEA - Sobre", None))
        self.lbl_project.setText(QCoreApplication.translate("AboutView", u"<html><head/><body><p><span style=\" font-weight:700;\">T-TEA</span> \u00e9 um console para exergames de Ch\u00e3o Interativo voltados ao p\u00fablico com Transtorno do Espectro Autista (TEA), mas n\u00e3o exclusivamente. Desenvolvido pela UDESC Joinville - Larva.</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.teb_link.setToolTip(QCoreApplication.translate("AboutView", u"Link plataforma T-TEA", None))
#endif // QT_CONFIG(tooltip)
        self.teb_link.setHtml(QCoreApplication.translate("AboutView", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://udescmove2learn.wordpress.com/2023/06/26/t-tea/\"><span style=\" font-size:9pt; text-decoration: underline; color:#003e92;\">Saiba mais sobre a Plataforma!</span></a></p></body></html>", None))
        self.lbl_developer.setHtml(QCoreApplication.translate("AboutView", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Desenvolvido por:</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. Marcelo da Silva Hounsell<br />2. Andr\u00e9 Bonetto Trindade<br />3. Gabriel Brunelli Pereira<br />4. Marlow Rodrigo Becker Dickel<br />5. Lu"
                        "is Eduardo Bet<br />6. Maria Julia Sales<br />7. Alexandre Altair de Melo</span></p></body></html>", None))
        self.pb_ok.setText(QCoreApplication.translate("AboutView", u"OK", None))
    # retranslateUi

