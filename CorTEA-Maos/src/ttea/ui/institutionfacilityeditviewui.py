# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'institutionfacilityeditview.ui'
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


class Ui_InstitutionFacilityEditView(object):
    def setupUi(self, InstitutionFacilityEditView):
        if not InstitutionFacilityEditView.objectName():
            InstitutionFacilityEditView.setObjectName(u"InstitutionFacilityEditView")
        InstitutionFacilityEditView.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        InstitutionFacilityEditView.setWindowIcon(icon)
        InstitutionFacilityEditView.setModal(True)
        self.main_layout = QVBoxLayout(InstitutionFacilityEditView)
        self.main_layout.setObjectName(u"main_layout")
        self.tab_institution = QTabWidget(InstitutionFacilityEditView)
        self.tab_institution.setObjectName(u"tab_institution")
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

        self.lbl_address = QLabel(self.tab_data)
        self.lbl_address.setObjectName(u"lbl_address")

        self.details_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_address)

        self.led_address = QLineEdit(self.tab_data)
        self.led_address.setObjectName(u"led_address")
        self.led_address.setClearButtonEnabled(True)

        self.details_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.led_address)

        self.lbl_phone = QLabel(self.tab_data)
        self.lbl_phone.setObjectName(u"lbl_phone")

        self.details_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_phone)

        self.led_phone = QLineEdit(self.tab_data)
        self.led_phone.setObjectName(u"led_phone")
        self.led_phone.setClearButtonEnabled(True)

        self.details_layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.led_phone)

        self.lbl_email = QLabel(self.tab_data)
        self.lbl_email.setObjectName(u"lbl_email")

        self.details_layout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_email)

        self.led_email = QLineEdit(self.tab_data)
        self.led_email.setObjectName(u"led_email")
        self.led_email.setClearButtonEnabled(True)

        self.details_layout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.led_email)

        self.lbl_website = QLabel(self.tab_data)
        self.lbl_website.setObjectName(u"lbl_website")

        self.details_layout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_website)

        self.led_website = QLineEdit(self.tab_data)
        self.led_website.setObjectName(u"led_website")
        self.led_website.setClearButtonEnabled(True)

        self.details_layout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.led_website)

        self.lbl_social_network = QLabel(self.tab_data)
        self.lbl_social_network.setObjectName(u"lbl_social_network")

        self.details_layout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lbl_social_network)

        self.led_social_network = QLineEdit(self.tab_data)
        self.led_social_network.setObjectName(u"led_social_network")
        self.led_social_network.setClearButtonEnabled(True)

        self.details_layout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.led_social_network)

        self.tab_institution.addTab(self.tab_data, "")

        self.main_layout.addWidget(self.tab_institution)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(InstitutionFacilityEditView)
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

        self.pb_cancel = QPushButton(InstitutionFacilityEditView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        sizePolicy.setHeightForWidth(self.pb_cancel.sizePolicy().hasHeightForWidth())
        self.pb_cancel.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon2)
        self.pb_cancel.setAutoDefault(False)

        self.lay_button.addWidget(self.pb_cancel)


        self.main_layout.addLayout(self.lay_button)


        self.retranslateUi(InstitutionFacilityEditView)

        self.tab_institution.setCurrentIndex(0)
        self.cbx_type.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(InstitutionFacilityEditView)
    # setupUi

    def retranslateUi(self, InstitutionFacilityEditView):
        InstitutionFacilityEditView.setWindowTitle(QCoreApplication.translate("InstitutionFacilityEditView", u"Plataforma T-TEA - Institui\u00e7\u00e3o / Estabelecimento", None))
        self.lbl_name.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Nome:", None))
        self.led_name.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"Nome", None))
        self.lbl_type.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Tipo:", None))
        self.lbl_address.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Endere\u00e7o:", None))
        self.led_address.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"Rua, n\u00famero, bairro, cidade - UF - Pa\u00eds", None))
        self.lbl_phone.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Telefone:", None))
#if QT_CONFIG(tooltip)
        self.led_phone.setToolTip(QCoreApplication.translate("InstitutionFacilityEditView", u"Digite o n\u00famero com c\u00f3digo do pa\u00eds (ex: +55 para Brasil)", None))
#endif // QT_CONFIG(tooltip)
        self.led_phone.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"+99 99 99999-9999", None))
        self.lbl_email.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"E-mail:", None))
        self.led_email.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"email@email.com", None))
        self.lbl_website.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Site / Website:", None))
        self.led_website.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"https://www.exemplo.com", None))
        self.lbl_social_network.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Rede Social:", None))
        self.led_social_network.setPlaceholderText(QCoreApplication.translate("InstitutionFacilityEditView", u"@instituicao ou link completo", None))
        self.tab_institution.setTabText(self.tab_institution.indexOf(self.tab_data), QCoreApplication.translate("InstitutionFacilityEditView", u"Dados", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("InstitutionFacilityEditView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("InstitutionFacilityEditView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("InstitutionFacilityEditView", u"Cancelar", None))
    # retranslateUi

