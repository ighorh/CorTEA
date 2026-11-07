# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'professionaleditview.ui'
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
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QSpacerItem, QTabWidget,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_ProfessionalEditView(object):
    def setupUi(self, ProfessionalEditView):
        if not ProfessionalEditView.objectName():
            ProfessionalEditView.setObjectName(u"ProfessionalEditView")
        ProfessionalEditView.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ProfessionalEditView.setWindowIcon(icon)
        ProfessionalEditView.setModal(True)
        self.main_layout = QVBoxLayout(ProfessionalEditView)
        self.main_layout.setObjectName(u"main_layout")
        self.tab_professional = QTabWidget(ProfessionalEditView)
        self.tab_professional.setObjectName(u"tab_professional")
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

        self.lbl_type = QLabel(self.tab_data)
        self.lbl_type.setObjectName(u"lbl_type")

        self.details_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_type)

        self.cbx_type = QComboBox(self.tab_data)
        self.cbx_type.setObjectName(u"cbx_type")
        self.cbx_type.setMaxVisibleItems(5)

        self.details_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbx_type)

        self.lbl_institution = QLabel(self.tab_data)
        self.lbl_institution.setObjectName(u"lbl_institution")
        self.lbl_institution.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_institution.setWordWrap(True)

        self.details_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_institution)

        self.cbx_institution = QComboBox(self.tab_data)
        self.cbx_institution.setObjectName(u"cbx_institution")
        self.cbx_institution.setMaxVisibleItems(5)

        self.details_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbx_institution)

        self.tab_professional.addTab(self.tab_data, "")

        self.main_layout.addWidget(self.tab_professional)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(ProfessionalEditView)
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

        self.pb_cancel = QPushButton(ProfessionalEditView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        sizePolicy.setHeightForWidth(self.pb_cancel.sizePolicy().hasHeightForWidth())
        self.pb_cancel.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon2)
        self.pb_cancel.setAutoDefault(False)

        self.lay_button.addWidget(self.pb_cancel)


        self.main_layout.addLayout(self.lay_button)


        self.retranslateUi(ProfessionalEditView)

        self.tab_professional.setCurrentIndex(0)
        self.cbx_type.setCurrentIndex(-1)
        self.cbx_institution.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(ProfessionalEditView)
    # setupUi

    def retranslateUi(self, ProfessionalEditView):
        ProfessionalEditView.setWindowTitle(QCoreApplication.translate("ProfessionalEditView", u"Plataforma T-TEA - Profissional", None))
        self.lbl_name.setText(QCoreApplication.translate("ProfessionalEditView", u"Nome:", None))
        self.led_name.setPlaceholderText(QCoreApplication.translate("ProfessionalEditView", u"Nome", None))
        self.lbl_type.setText(QCoreApplication.translate("ProfessionalEditView", u"Tipo:", None))
        self.lbl_institution.setText(QCoreApplication.translate("ProfessionalEditView", u"Institui\u00e7\u00e3o/Estabelecimento:", None))
        self.tab_professional.setTabText(self.tab_professional.indexOf(self.tab_data), QCoreApplication.translate("ProfessionalEditView", u"Dados", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("ProfessionalEditView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("ProfessionalEditView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("ProfessionalEditView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("ProfessionalEditView", u"Cancelar", None))
    # retranslateUi

