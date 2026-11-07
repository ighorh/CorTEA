# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playerkarteaconfiglistview.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                               QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                               QLineEdit, QPushButton, QSizePolicy,
                               QSpacerItem, QTableWidget, QTableWidgetItem,
                               QTabWidget, QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_PlayerKarteaConfigListView(object):
    def setupUi(self, PlayerKarteaConfigListView):
        if not PlayerKarteaConfigListView.objectName():
            PlayerKarteaConfigListView.setObjectName(u"PlayerKarteaConfigListView")
        PlayerKarteaConfigListView.resize(600, 400)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PlayerKarteaConfigListView.setWindowIcon(icon)
        PlayerKarteaConfigListView.setModal(True)
        self.mainLayout = QHBoxLayout(PlayerKarteaConfigListView)
        self.mainLayout.setObjectName(u"mainLayout")
        self.lay_left = QVBoxLayout()
        self.lay_left.setObjectName(u"lay_left")
        self.lay_search = QHBoxLayout()
        self.lay_search.setObjectName(u"lay_search")
        self.lbl_search = QLabel(PlayerKarteaConfigListView)
        self.lbl_search.setObjectName(u"lbl_search")

        self.lay_search.addWidget(self.lbl_search)

        self.led_search = QLineEdit(PlayerKarteaConfigListView)
        self.led_search.setObjectName(u"led_search")

        self.lay_search.addWidget(self.led_search)


        self.lay_left.addLayout(self.lay_search)

        self.tbl_config = QTableWidget(PlayerKarteaConfigListView)
        if (self.tbl_config.columnCount() < 2):
            self.tbl_config.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_config.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_config.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tbl_config.setObjectName(u"tbl_config")
        self.tbl_config.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_config.setAlternatingRowColors(True)
        self.tbl_config.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl_config.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_config.setSortingEnabled(True)
        self.tbl_config.setColumnCount(2)
        self.tbl_config.horizontalHeader().setStretchLastSection(True)

        self.lay_left.addWidget(self.tbl_config)


        self.mainLayout.addLayout(self.lay_left)

        self.lay_right = QVBoxLayout()
        self.lay_right.setObjectName(u"lay_right")
        self.tab_config = QTabWidget(PlayerKarteaConfigListView)
        self.tab_config.setObjectName(u"tab_config")
        self.lay_details = QWidget()
        self.lay_details.setObjectName(u"lay_details")
        self.detailsLayout = QVBoxLayout(self.lay_details)
        self.detailsLayout.setObjectName(u"detailsLayout")
        self.grd_detail = QGridLayout()
        self.grd_detail.setObjectName(u"grd_detail")
        self.lbl_id = QLabel(self.lay_details)
        self.lbl_id.setObjectName(u"lbl_id")

        self.grd_detail.addWidget(self.lbl_id, 0, 0, 1, 1)

        self.lbl_id_value = QLabel(self.lay_details)
        self.lbl_id_value.setObjectName(u"lbl_id_value")

        self.grd_detail.addWidget(self.lbl_id_value, 0, 1, 1, 1)

        self.lbl_name = QLabel(self.lay_details)
        self.lbl_name.setObjectName(u"lbl_name")

        self.grd_detail.addWidget(self.lbl_name, 1, 0, 1, 1)

        self.lbl_name_value = QLabel(self.lay_details)
        self.lbl_name_value.setObjectName(u"lbl_name_value")

        self.grd_detail.addWidget(self.lbl_name_value, 1, 1, 1, 1)

        self.lbl_phase = QLabel(self.lay_details)
        self.lbl_phase.setObjectName(u"lbl_phase")

        self.grd_detail.addWidget(self.lbl_phase, 2, 0, 1, 1)

        self.lbl_phase_value = QLabel(self.lay_details)
        self.lbl_phase_value.setObjectName(u"lbl_phase_value")

        self.grd_detail.addWidget(self.lbl_phase_value, 2, 1, 1, 1)

        self.lbl_level = QLabel(self.lay_details)
        self.lbl_level.setObjectName(u"lbl_level")

        self.grd_detail.addWidget(self.lbl_level, 3, 0, 1, 1)

        self.lbl_level_value = QLabel(self.lay_details)
        self.lbl_level_value.setObjectName(u"lbl_level_value")

        self.grd_detail.addWidget(self.lbl_level_value, 3, 1, 1, 1)

        self.lbl_time = QLabel(self.lay_details)
        self.lbl_time.setObjectName(u"lbl_time")

        self.grd_detail.addWidget(self.lbl_time, 4, 0, 1, 1)

        self.lbl_time_value = QLabel(self.lay_details)
        self.lbl_time_value.setObjectName(u"lbl_time_value")

        self.grd_detail.addWidget(self.lbl_time_value, 4, 1, 1, 1)


        self.detailsLayout.addLayout(self.grd_detail)

        self.sp_detail = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.detailsLayout.addItem(self.sp_detail)

        self.tab_config.addTab(self.lay_details, "")

        self.lay_right.addWidget(self.tab_config)

        self.lay_buttons = QHBoxLayout()
        self.lay_buttons.setObjectName(u"lay_buttons")
        self.pb_new = QPushButton(PlayerKarteaConfigListView)
        self.pb_new.setObjectName(u"pb_new")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/newicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_new.setIcon(icon1)

        self.lay_buttons.addWidget(self.pb_new)

        self.pb_edit = QPushButton(PlayerKarteaConfigListView)
        self.pb_edit.setObjectName(u"pb_edit")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/editicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_edit.setIcon(icon2)

        self.lay_buttons.addWidget(self.pb_edit)

        self.pb_delete = QPushButton(PlayerKarteaConfigListView)
        self.pb_delete.setObjectName(u"pb_delete")
        icon3 = QIcon()
        icon3.addFile(u":/icons/ui/buttons/trashicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_delete.setIcon(icon3)

        self.lay_buttons.addWidget(self.pb_delete)


        self.lay_right.addLayout(self.lay_buttons)


        self.mainLayout.addLayout(self.lay_right)


        self.retranslateUi(PlayerKarteaConfigListView)

        self.tab_config.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PlayerKarteaConfigListView)
    # setupUi

    def retranslateUi(self, PlayerKarteaConfigListView):
        PlayerKarteaConfigListView.setWindowTitle(QCoreApplication.translate("PlayerKarteaConfigListView", u"Plataforma T-TEA - Configura\u00e7\u00f5es Kartea", None))
        self.lbl_search.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Pesquisar:", None))
        self.led_search.setPlaceholderText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Digite o nome ou ID do jogador", None))
        ___qtablewidgetitem = self.tbl_config.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"ID", None));
        ___qtablewidgetitem1 = self.tbl_config.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Nome", None));
        self.lbl_id.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"ID:", None))
        self.lbl_id_value.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"ID: ", None))
        self.lbl_name.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Nome:", None))
        self.lbl_name_value.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Nome: ", None))
        self.lbl_phase.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Fase Atual:", None))
        self.lbl_phase_value.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Fase Atual: ", None))
        self.lbl_level.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"N\u00edvel Atual:", None))
        self.lbl_level_value.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"N\u00edvel Atual: ", None))
        self.lbl_time.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Tempo do N\u00edvel:", None))
        self.lbl_time_value.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Tempo do N\u00edvel: ", None))
        self.tab_config.setTabText(self.tab_config.indexOf(self.lay_details), QCoreApplication.translate("PlayerKarteaConfigListView", u"Detalhes", None))
#if QT_CONFIG(tooltip)
        self.pb_new.setToolTip(QCoreApplication.translate("PlayerKarteaConfigListView", u"Criar um novo registro", None))
#endif // QT_CONFIG(tooltip)
        self.pb_new.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Novo", None))
#if QT_CONFIG(tooltip)
        self.pb_edit.setToolTip(QCoreApplication.translate("PlayerKarteaConfigListView", u"Editar o registro selecionado", None))
#endif // QT_CONFIG(tooltip)
        self.pb_edit.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Editar", None))
#if QT_CONFIG(tooltip)
        self.pb_delete.setToolTip(QCoreApplication.translate("PlayerKarteaConfigListView", u"Excluir o registro selecionado", None))
#endif // QT_CONFIG(tooltip)
        self.pb_delete.setText(QCoreApplication.translate("PlayerKarteaConfigListView", u"Excluir", None))
    # retranslateUi

