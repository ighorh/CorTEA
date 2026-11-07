# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playerlistview.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                               QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                               QLineEdit, QPushButton, QSizePolicy,
                               QSpacerItem, QTableWidget, QTableWidgetItem,
                               QTabWidget, QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_PlayerListView(object):
    def setupUi(self, PlayerListView):
        if not PlayerListView.objectName():
            PlayerListView.setObjectName(u"PlayerListView")
        PlayerListView.resize(600, 400)
        icon = QIcon()
        icon.addFile(u":/icons/system/appicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PlayerListView.setWindowIcon(icon)
        PlayerListView.setModal(True)
        self.mainLayout = QHBoxLayout(PlayerListView)
        self.mainLayout.setObjectName(u"mainLayout")
        self.lay_left = QVBoxLayout()
        self.lay_left.setObjectName(u"lay_left")
        self.lay_search = QHBoxLayout()
        self.lay_search.setObjectName(u"lay_search")
        self.lbl_search = QLabel(PlayerListView)
        self.lbl_search.setObjectName(u"lbl_search")

        self.lay_search.addWidget(self.lbl_search)

        self.led_search = QLineEdit(PlayerListView)
        self.led_search.setObjectName(u"led_search")

        self.lay_search.addWidget(self.led_search)


        self.lay_left.addLayout(self.lay_search)

        self.tbl_player = QTableWidget(PlayerListView)
        if (self.tbl_player.columnCount() < 2):
            self.tbl_player.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_player.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_player.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tbl_player.setObjectName(u"tbl_player")
        self.tbl_player.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbl_player.setAlternatingRowColors(True)
        self.tbl_player.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tbl_player.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbl_player.setSortingEnabled(True)
        self.tbl_player.setColumnCount(2)
        self.tbl_player.horizontalHeader().setStretchLastSection(True)

        self.lay_left.addWidget(self.tbl_player)


        self.mainLayout.addLayout(self.lay_left)

        self.lay_right = QVBoxLayout()
        self.lay_right.setObjectName(u"lay_right")
        self.tab_player = QTabWidget(PlayerListView)
        self.tab_player.setObjectName(u"tab_player")
        self.lay_detail = QWidget()
        self.lay_detail.setObjectName(u"lay_detail")
        self.detailsLayout = QVBoxLayout(self.lay_detail)
        self.detailsLayout.setObjectName(u"detailsLayout")
        self.grd_detail = QGridLayout()
        self.grd_detail.setObjectName(u"grd_detail")
        self.lbl_id = QLabel(self.lay_detail)
        self.lbl_id.setObjectName(u"lbl_id")
        self.lbl_id.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_id, 0, 0, 1, 1)

        self.lbl_id_value = QLabel(self.lay_detail)
        self.lbl_id_value.setObjectName(u"lbl_id_value")
        self.lbl_id_value.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_id_value, 0, 1, 1, 1)

        self.lbl_name = QLabel(self.lay_detail)
        self.lbl_name.setObjectName(u"lbl_name")
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_name, 1, 0, 1, 1)

        self.lbl_name_value = QLabel(self.lay_detail)
        self.lbl_name_value.setObjectName(u"lbl_name_value")
        self.lbl_name_value.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_name_value, 1, 1, 1, 1)

        self.lbl_birth_date = QLabel(self.lay_detail)
        self.lbl_birth_date.setObjectName(u"lbl_birth_date")
        self.lbl_birth_date.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_birth_date, 2, 0, 1, 1)

        self.lbl_birth_date_value = QLabel(self.lay_detail)
        self.lbl_birth_date_value.setObjectName(u"lbl_birth_date_value")
        self.lbl_birth_date_value.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_birth_date_value, 2, 1, 1, 1)

        self.lbl_observation = QLabel(self.lay_detail)
        self.lbl_observation.setObjectName(u"lbl_observation")
        self.lbl_observation.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_observation, 3, 0, 1, 1)

        self.lbl_observation_value = QLabel(self.lay_detail)
        self.lbl_observation_value.setObjectName(u"lbl_observation_value")
        self.lbl_observation_value.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.grd_detail.addWidget(self.lbl_observation_value, 3, 1, 1, 1)


        self.detailsLayout.addLayout(self.grd_detail)

        self.sp_detail = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.detailsLayout.addItem(self.sp_detail)

        self.tab_player.addTab(self.lay_detail, "")

        self.lay_right.addWidget(self.tab_player)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.pb_new = QPushButton(PlayerListView)
        self.pb_new.setObjectName(u"pb_new")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/newicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_new.setIcon(icon1)

        self.lay_button.addWidget(self.pb_new)

        self.pb_edit = QPushButton(PlayerListView)
        self.pb_edit.setObjectName(u"pb_edit")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ui/buttons/editicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_edit.setIcon(icon2)

        self.lay_button.addWidget(self.pb_edit)

        self.pb_delete = QPushButton(PlayerListView)
        self.pb_delete.setObjectName(u"pb_delete")
        icon3 = QIcon()
        icon3.addFile(u":/icons/ui/buttons/trashicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_delete.setIcon(icon3)

        self.lay_button.addWidget(self.pb_delete)


        self.lay_right.addLayout(self.lay_button)


        self.mainLayout.addLayout(self.lay_right)


        self.retranslateUi(PlayerListView)

        self.tab_player.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PlayerListView)
    # setupUi

    def retranslateUi(self, PlayerListView):
        PlayerListView.setWindowTitle(QCoreApplication.translate("PlayerListView", u"Plataforma T-TEA - Jogador", None))
        self.lbl_search.setText(QCoreApplication.translate("PlayerListView", u"Pesquisar:", None))
        self.led_search.setPlaceholderText(QCoreApplication.translate("PlayerListView", u"Digite o nome ou ID", None))
        ___qtablewidgetitem = self.tbl_player.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PlayerListView", u"ID", None))
        ___qtablewidgetitem1 = self.tbl_player.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PlayerListView", u"Nome", None))
        self.lbl_id.setText(QCoreApplication.translate("PlayerListView", u"ID:", None))
        self.lbl_id_value.setText(QCoreApplication.translate("PlayerListView", u"ID: ", None))
        self.lbl_name.setText(QCoreApplication.translate("PlayerListView", u"Nome:", None))
        self.lbl_name_value.setText(QCoreApplication.translate("PlayerListView", u"Nome: ", None))
        self.lbl_birth_date.setText(QCoreApplication.translate("PlayerListView", u"Data de Nascimento:", None))
        self.lbl_birth_date_value.setText(QCoreApplication.translate("PlayerListView", u"Data de Nascimento: ", None))
        self.lbl_observation.setText(QCoreApplication.translate("PlayerListView", u"Observa\u00e7\u00e3o:", None))
        self.lbl_observation_value.setText(QCoreApplication.translate("PlayerListView", u"Observa\u00e7\u00e3o: ", None))
        self.tab_player.setTabText(self.tab_player.indexOf(self.lay_detail), QCoreApplication.translate("PlayerListView", u"Detalhes", None))
#if QT_CONFIG(tooltip)
        self.pb_new.setToolTip(QCoreApplication.translate("PlayerListView", u"Criar um novo registro", None))
#endif // QT_CONFIG(tooltip)
        self.pb_new.setText(QCoreApplication.translate("PlayerListView", u"Novo", None))
#if QT_CONFIG(tooltip)
        self.pb_edit.setToolTip(QCoreApplication.translate("PlayerListView", u"Editar o registro selecionado", None))
#endif // QT_CONFIG(tooltip)
        self.pb_edit.setText(QCoreApplication.translate("PlayerListView", u"Editar", None))
#if QT_CONFIG(tooltip)
        self.pb_delete.setToolTip(QCoreApplication.translate("PlayerListView", u"Excluir o registro selecionado", None))
#endif // QT_CONFIG(tooltip)
        self.pb_delete.setText(QCoreApplication.translate("PlayerListView", u"Excluir", None))
    # retranslateUi

