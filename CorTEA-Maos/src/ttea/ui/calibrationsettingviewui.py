# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calibrationsettingview.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QDoubleSpinBox, QFormLayout, QGroupBox,
                               QHBoxLayout, QLabel, QPushButton, QRadioButton,
                               QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
                               QVBoxLayout, QWidget)

import ttea.resources.resources_rc


class Ui_CalibrationSettingView(object):
    def setupUi(self, CalibrationSettingView):
        if not CalibrationSettingView.objectName():
            CalibrationSettingView.setObjectName(u"CalibrationSettingView")
        CalibrationSettingView.resize(800, 624)
        CalibrationSettingView.setModal(True)
        self.main_layout = QVBoxLayout(CalibrationSettingView)
        self.main_layout.setObjectName(u"main_layout")
        self.tab_widget = QTabWidget(CalibrationSettingView)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_mediapipe = QWidget()
        self.tab_mediapipe.setObjectName(u"tab_mediapipe")
        self.lay_mediapipe = QVBoxLayout(self.tab_mediapipe)
        self.lay_mediapipe.setSpacing(12)
        self.lay_mediapipe.setObjectName(u"lay_mediapipe")
        self.lay_mediapipe.setContentsMargins(12, 12, 12, 12)
        self.frm_mediapipe = QFormLayout()
        self.frm_mediapipe.setObjectName(u"frm_mediapipe")
        self.frm_mediapipe.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.frm_mediapipe.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_model_desktop = QLabel(self.tab_mediapipe)
        self.lbl_model_desktop.setObjectName(u"lbl_model_desktop")

        self.frm_mediapipe.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_model_desktop)

        self.grp_model_desktop = QGroupBox(self.tab_mediapipe)
        self.grp_model_desktop.setObjectName(u"grp_model_desktop")
        self.horizontalLayout_desktop = QHBoxLayout(self.grp_model_desktop)
        self.horizontalLayout_desktop.setObjectName(u"horizontalLayout_desktop")
        self.rb_model_desktop_lite = QRadioButton(self.grp_model_desktop)
        self.rb_model_desktop_lite.setObjectName(u"rb_model_desktop_lite")
        self.rb_model_desktop_lite.setChecked(False)
        self.rb_model_desktop_lite.setProperty(u"dataclass_property", u"mediapipe_model_desktop")
        self.rb_model_desktop_lite.setProperty(u"dataclass_property_value", u"pose_landmarker_lite.task")

        self.horizontalLayout_desktop.addWidget(self.rb_model_desktop_lite)

        self.rb_model_desktop_full = QRadioButton(self.grp_model_desktop)
        self.rb_model_desktop_full.setObjectName(u"rb_model_desktop_full")
        self.rb_model_desktop_full.setChecked(True)
        self.rb_model_desktop_full.setProperty(u"dataclass_property", u"mediapipe_model_desktop")
        self.rb_model_desktop_full.setProperty(u"dataclass_property_value", u"pose_landmarker_full.task")

        self.horizontalLayout_desktop.addWidget(self.rb_model_desktop_full)

        self.rb_model_desktop_heavy = QRadioButton(self.grp_model_desktop)
        self.rb_model_desktop_heavy.setObjectName(u"rb_model_desktop_heavy")
        self.rb_model_desktop_heavy.setProperty(u"dataclass_property", u"mediapipe_model_desktop")
        self.rb_model_desktop_heavy.setProperty(u"dataclass_property_value", u"pose_landmarker_heavy.task")

        self.horizontalLayout_desktop.addWidget(self.rb_model_desktop_heavy)

        self.hs_model_desktop = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_desktop.addItem(self.hs_model_desktop)


        self.frm_mediapipe.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grp_model_desktop)

        self.lbl_model_embedded = QLabel(self.tab_mediapipe)
        self.lbl_model_embedded.setObjectName(u"lbl_model_embedded")

        self.frm_mediapipe.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_model_embedded)

        self.grp_model_embedded = QGroupBox(self.tab_mediapipe)
        self.grp_model_embedded.setObjectName(u"grp_model_embedded")
        self.horizontalLayout_embedded = QHBoxLayout(self.grp_model_embedded)
        self.horizontalLayout_embedded.setObjectName(u"horizontalLayout_embedded")
        self.rb_model_embedded_lite = QRadioButton(self.grp_model_embedded)
        self.rb_model_embedded_lite.setObjectName(u"rb_model_embedded_lite")
        self.rb_model_embedded_lite.setChecked(True)
        self.rb_model_embedded_lite.setProperty(u"dataclass_property", u"mediapipe_model_embedded")
        self.rb_model_embedded_lite.setProperty(u"dataclass_property_value", u"pose_landmarker_lite.task")

        self.horizontalLayout_embedded.addWidget(self.rb_model_embedded_lite)

        self.rb_model_embedded_full = QRadioButton(self.grp_model_embedded)
        self.rb_model_embedded_full.setObjectName(u"rb_model_embedded_full")
        self.rb_model_embedded_full.setChecked(False)
        self.rb_model_embedded_full.setProperty(u"dataclass_property", u"mediapipe_model_embedded")
        self.rb_model_embedded_full.setProperty(u"dataclass_property_value", u"pose_landmarker_full.task")

        self.horizontalLayout_embedded.addWidget(self.rb_model_embedded_full)

        self.rb_model_embedded_heavy = QRadioButton(self.grp_model_embedded)
        self.rb_model_embedded_heavy.setObjectName(u"rb_model_embedded_heavy")
        self.rb_model_embedded_heavy.setProperty(u"dataclass_property", u"mediapipe_model_embedded")
        self.rb_model_embedded_heavy.setProperty(u"dataclass_property_value", u"pose_landmarker_heavy.task")

        self.horizontalLayout_embedded.addWidget(self.rb_model_embedded_heavy)

        self.hs_model_embedded = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_embedded.addItem(self.hs_model_embedded)


        self.frm_mediapipe.setWidget(1, QFormLayout.ItemRole.FieldRole, self.grp_model_embedded)

        self.lbl_embedded_processing = QLabel(self.tab_mediapipe)
        self.lbl_embedded_processing.setObjectName(u"lbl_embedded_processing")

        self.frm_mediapipe.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_embedded_processing)

        self.grp_embedded_processing = QGroupBox(self.tab_mediapipe)
        self.grp_embedded_processing.setObjectName(u"grp_embedded_processing")
        self.horizontalLayout_embedded_proc = QHBoxLayout(self.grp_embedded_processing)
        self.horizontalLayout_embedded_proc.setObjectName(u"horizontalLayout_embedded_proc")
        self.rb_embedded_processing_cpu = QRadioButton(self.grp_embedded_processing)
        self.rb_embedded_processing_cpu.setObjectName(u"rb_embedded_processing_cpu")
        self.rb_embedded_processing_cpu.setChecked(True)
        self.rb_embedded_processing_cpu.setProperty(u"dataclass_property", u"mediapipe_embedded_processing")

        self.horizontalLayout_embedded_proc.addWidget(self.rb_embedded_processing_cpu)

        self.rb_embedded_processing_gpu = QRadioButton(self.grp_embedded_processing)
        self.rb_embedded_processing_gpu.setObjectName(u"rb_embedded_processing_gpu")
        self.rb_embedded_processing_gpu.setProperty(u"dataclass_property", u"mediapipe_embedded_processing")

        self.horizontalLayout_embedded_proc.addWidget(self.rb_embedded_processing_gpu)

        self.hs_embedded_processing = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_embedded_proc.addItem(self.hs_embedded_processing)


        self.frm_mediapipe.setWidget(2, QFormLayout.ItemRole.FieldRole, self.grp_embedded_processing)

        self.lbl_linux_processing = QLabel(self.tab_mediapipe)
        self.lbl_linux_processing.setObjectName(u"lbl_linux_processing")

        self.frm_mediapipe.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_linux_processing)

        self.grp_linux_processing = QGroupBox(self.tab_mediapipe)
        self.grp_linux_processing.setObjectName(u"grp_linux_processing")
        self.horizontalLayout_linux = QHBoxLayout(self.grp_linux_processing)
        self.horizontalLayout_linux.setObjectName(u"horizontalLayout_linux")
        self.rb_linux_processing_cpu = QRadioButton(self.grp_linux_processing)
        self.rb_linux_processing_cpu.setObjectName(u"rb_linux_processing_cpu")
        self.rb_linux_processing_cpu.setChecked(True)
        self.rb_linux_processing_cpu.setProperty(u"dataclass_property", u"mediapipe_linux_processing")

        self.horizontalLayout_linux.addWidget(self.rb_linux_processing_cpu)

        self.rb_linux_processing_gpu = QRadioButton(self.grp_linux_processing)
        self.rb_linux_processing_gpu.setObjectName(u"rb_linux_processing_gpu")
        self.rb_linux_processing_gpu.setProperty(u"dataclass_property", u"mediapipe_linux_processing")

        self.horizontalLayout_linux.addWidget(self.rb_linux_processing_gpu)

        self.hs_linux_processing = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_linux.addItem(self.hs_linux_processing)


        self.frm_mediapipe.setWidget(3, QFormLayout.ItemRole.FieldRole, self.grp_linux_processing)

        self.lbl_mac_processing = QLabel(self.tab_mediapipe)
        self.lbl_mac_processing.setObjectName(u"lbl_mac_processing")

        self.frm_mediapipe.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_mac_processing)

        self.groupBox_mac = QGroupBox(self.tab_mediapipe)
        self.groupBox_mac.setObjectName(u"groupBox_mac")
        self.horizontalLayout_mac = QHBoxLayout(self.groupBox_mac)
        self.horizontalLayout_mac.setObjectName(u"horizontalLayout_mac")
        self.rb_mac_processing_cpu = QRadioButton(self.groupBox_mac)
        self.rb_mac_processing_cpu.setObjectName(u"rb_mac_processing_cpu")
        self.rb_mac_processing_cpu.setChecked(True)
        self.rb_mac_processing_cpu.setProperty(u"dataclass_property", u"mediapipe_mac_processing")

        self.horizontalLayout_mac.addWidget(self.rb_mac_processing_cpu)

        self.rb_mac_processing_gpu = QRadioButton(self.groupBox_mac)
        self.rb_mac_processing_gpu.setObjectName(u"rb_mac_processing_gpu")
        self.rb_mac_processing_gpu.setProperty(u"dataclass_property", u"mediapipe_mac_processing")

        self.horizontalLayout_mac.addWidget(self.rb_mac_processing_gpu)

        self.hs_mac_processing = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_mac.addItem(self.hs_mac_processing)


        self.frm_mediapipe.setWidget(4, QFormLayout.ItemRole.FieldRole, self.groupBox_mac)

        self.lbl_windows_processing = QLabel(self.tab_mediapipe)
        self.lbl_windows_processing.setObjectName(u"lbl_windows_processing")

        self.frm_mediapipe.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_windows_processing)

        self.groupBox_windows = QGroupBox(self.tab_mediapipe)
        self.groupBox_windows.setObjectName(u"groupBox_windows")
        self.horizontalLayout_windows = QHBoxLayout(self.groupBox_windows)
        self.horizontalLayout_windows.setObjectName(u"horizontalLayout_windows")
        self.rb_windows_processing_cpu = QRadioButton(self.groupBox_windows)
        self.rb_windows_processing_cpu.setObjectName(u"rb_windows_processing_cpu")
        self.rb_windows_processing_cpu.setChecked(True)
        self.rb_windows_processing_cpu.setProperty(u"dataclass_property", u"mediapipe_windows_processing")

        self.horizontalLayout_windows.addWidget(self.rb_windows_processing_cpu)

        self.rb_windows_processing_gpu = QRadioButton(self.groupBox_windows)
        self.rb_windows_processing_gpu.setObjectName(u"rb_windows_processing_gpu")
        self.rb_windows_processing_gpu.setProperty(u"dataclass_property", u"mediapipe_windows_processing")

        self.horizontalLayout_windows.addWidget(self.rb_windows_processing_gpu)

        self.hs_windows_processing = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_windows.addItem(self.hs_windows_processing)


        self.frm_mediapipe.setWidget(5, QFormLayout.ItemRole.FieldRole, self.groupBox_windows)

        self.lbl_execution_mode = QLabel(self.tab_mediapipe)
        self.lbl_execution_mode.setObjectName(u"lbl_execution_mode")

        self.frm_mediapipe.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lbl_execution_mode)

        self.groupBox_execution_mode = QGroupBox(self.tab_mediapipe)
        self.groupBox_execution_mode.setObjectName(u"groupBox_execution_mode")
        self.horizontalLayout_execution_mode = QHBoxLayout(self.groupBox_execution_mode)
        self.horizontalLayout_execution_mode.setObjectName(u"horizontalLayout_execution_mode")
        self.rb_execution_mode_video = QRadioButton(self.groupBox_execution_mode)
        self.rb_execution_mode_video.setObjectName(u"rb_execution_mode_video")
        self.rb_execution_mode_video.setChecked(True)
        self.rb_execution_mode_video.setProperty(u"dataclass_property", u"mediapipe_execution_mode")
        self.rb_execution_mode_video.setProperty(u"dataclass_property_value", u"vision.RunningMode.VIDEO")

        self.horizontalLayout_execution_mode.addWidget(self.rb_execution_mode_video)

        self.hs_execution_mode = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_execution_mode.addItem(self.hs_execution_mode)


        self.frm_mediapipe.setWidget(6, QFormLayout.ItemRole.FieldRole, self.groupBox_execution_mode)

        self.lbl_enable_mediapipe_pose = QLabel(self.tab_mediapipe)
        self.lbl_enable_mediapipe_pose.setObjectName(u"lbl_enable_mediapipe_pose")

        self.frm_mediapipe.setWidget(7, QFormLayout.ItemRole.LabelRole, self.lbl_enable_mediapipe_pose)

        self.chk_enable_mediapipe_pose = QCheckBox(self.tab_mediapipe)
        self.chk_enable_mediapipe_pose.setObjectName(u"chk_enable_mediapipe_pose")
        self.chk_enable_mediapipe_pose.setChecked(True)
        self.chk_enable_mediapipe_pose.setProperty(u"dataclass_property", u"mediapipe_enable_mediapipe_pose")

        self.frm_mediapipe.setWidget(7, QFormLayout.ItemRole.FieldRole, self.chk_enable_mediapipe_pose)

        self.lbl_detection_position = QLabel(self.tab_mediapipe)
        self.lbl_detection_position.setObjectName(u"lbl_detection_position")

        self.frm_mediapipe.setWidget(8, QFormLayout.ItemRole.LabelRole, self.lbl_detection_position)

        self.spn_detection_position = QDoubleSpinBox(self.tab_mediapipe)
        self.spn_detection_position.setObjectName(u"spn_detection_position")
        self.spn_detection_position.setDecimals(2)
        self.spn_detection_position.setMinimum(0.000000000000000)
        self.spn_detection_position.setMaximum(1.000000000000000)
        self.spn_detection_position.setSingleStep(0.010000000000000)
        self.spn_detection_position.setValue(0.500000000000000)
        self.spn_detection_position.setProperty(u"dataclass_property", u"mediapipe_detection_position")

        self.frm_mediapipe.setWidget(8, QFormLayout.ItemRole.FieldRole, self.spn_detection_position)

        self.lbl_detection_presence = QLabel(self.tab_mediapipe)
        self.lbl_detection_presence.setObjectName(u"lbl_detection_presence")

        self.frm_mediapipe.setWidget(9, QFormLayout.ItemRole.LabelRole, self.lbl_detection_presence)

        self.spn_detection_presence = QDoubleSpinBox(self.tab_mediapipe)
        self.spn_detection_presence.setObjectName(u"spn_detection_presence")
        self.spn_detection_presence.setDecimals(2)
        self.spn_detection_presence.setMinimum(0.000000000000000)
        self.spn_detection_presence.setMaximum(1.000000000000000)
        self.spn_detection_presence.setSingleStep(0.010000000000000)
        self.spn_detection_presence.setValue(0.500000000000000)
        self.spn_detection_presence.setProperty(u"dataclass_property", u"mediapipe_detection_presence")

        self.frm_mediapipe.setWidget(9, QFormLayout.ItemRole.FieldRole, self.spn_detection_presence)

        self.lbl_detection_tracking = QLabel(self.tab_mediapipe)
        self.lbl_detection_tracking.setObjectName(u"lbl_detection_tracking")

        self.frm_mediapipe.setWidget(10, QFormLayout.ItemRole.LabelRole, self.lbl_detection_tracking)

        self.spn_detection_tracking = QDoubleSpinBox(self.tab_mediapipe)
        self.spn_detection_tracking.setObjectName(u"spn_detection_tracking")
        self.spn_detection_tracking.setDecimals(2)
        self.spn_detection_tracking.setMinimum(0.000000000000000)
        self.spn_detection_tracking.setMaximum(1.000000000000000)
        self.spn_detection_tracking.setSingleStep(0.010000000000000)
        self.spn_detection_tracking.setValue(0.500000000000000)
        self.spn_detection_tracking.setProperty(u"dataclass_property", u"mediapipe_detection_tracking")

        self.frm_mediapipe.setWidget(10, QFormLayout.ItemRole.FieldRole, self.spn_detection_tracking)

        self.lbl_num_position = QLabel(self.tab_mediapipe)
        self.lbl_num_position.setObjectName(u"lbl_num_position")

        self.frm_mediapipe.setWidget(11, QFormLayout.ItemRole.LabelRole, self.lbl_num_position)

        self.spn_num_position = QSpinBox(self.tab_mediapipe)
        self.spn_num_position.setObjectName(u"spn_num_position")
        self.spn_num_position.setEnabled(False)
        self.spn_num_position.setMinimum(1)
        self.spn_num_position.setMaximum(1)
        self.spn_num_position.setValue(1)
        self.spn_num_position.setProperty(u"dataclass_property", u"mediapipe_num_position")

        self.frm_mediapipe.setWidget(11, QFormLayout.ItemRole.FieldRole, self.spn_num_position)


        self.lay_mediapipe.addLayout(self.frm_mediapipe)

        self.vs_mediapipe = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_mediapipe.addItem(self.vs_mediapipe)

        self.tab_widget.addTab(self.tab_mediapipe, "")
        self.tab_opencv = QWidget()
        self.tab_opencv.setObjectName(u"tab_opencv")
        self.lay_opencv = QVBoxLayout(self.tab_opencv)
        self.lay_opencv.setSpacing(10)
        self.lay_opencv.setObjectName(u"lay_opencv")
        self.lay_opencv.setContentsMargins(12, 12, 12, 12)
        self.frm_opencv = QFormLayout()
        self.frm_opencv.setObjectName(u"frm_opencv")
        self.frm_opencv.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_embedded_capture = QLabel(self.tab_opencv)
        self.lbl_embedded_capture.setObjectName(u"lbl_embedded_capture")

        self.frm_opencv.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_embedded_capture)

        self.grp_embedded_capture = QGroupBox(self.tab_opencv)
        self.grp_embedded_capture.setObjectName(u"grp_embedded_capture")
        self.hboxLayout = QHBoxLayout(self.grp_embedded_capture)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.rb_embedded_v4l2 = QRadioButton(self.grp_embedded_capture)
        self.rb_embedded_v4l2.setObjectName(u"rb_embedded_v4l2")
        self.rb_embedded_v4l2.setChecked(True)
        self.rb_embedded_v4l2.setProperty(u"dataclass_property", u"opencv_embedded_capture")

        self.hboxLayout.addWidget(self.rb_embedded_v4l2)

        self.rb_embedded_gstreamer = QRadioButton(self.grp_embedded_capture)
        self.rb_embedded_gstreamer.setObjectName(u"rb_embedded_gstreamer")
        self.rb_embedded_gstreamer.setProperty(u"dataclass_property", u"opencv_embedded_capture")

        self.hboxLayout.addWidget(self.rb_embedded_gstreamer)

        self.hs_embedded_capture = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.hs_embedded_capture)


        self.frm_opencv.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grp_embedded_capture)

        self.lbl_linux_capture = QLabel(self.tab_opencv)
        self.lbl_linux_capture.setObjectName(u"lbl_linux_capture")

        self.frm_opencv.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_linux_capture)

        self.grp_linux_capture = QGroupBox(self.tab_opencv)
        self.grp_linux_capture.setObjectName(u"grp_linux_capture")
        self.hboxLayout1 = QHBoxLayout(self.grp_linux_capture)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.rb_linux_v4l2 = QRadioButton(self.grp_linux_capture)
        self.rb_linux_v4l2.setObjectName(u"rb_linux_v4l2")
        self.rb_linux_v4l2.setChecked(True)
        self.rb_linux_v4l2.setProperty(u"dataclass_property", u"opencv_linux_capture")

        self.hboxLayout1.addWidget(self.rb_linux_v4l2)

        self.rb_linux_gstreamer = QRadioButton(self.grp_linux_capture)
        self.rb_linux_gstreamer.setObjectName(u"rb_linux_gstreamer")
        self.rb_linux_gstreamer.setProperty(u"dataclass_property", u"opencv_linux_capture")

        self.hboxLayout1.addWidget(self.rb_linux_gstreamer)

        self.hs_linux_capture = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout1.addItem(self.hs_linux_capture)


        self.frm_opencv.setWidget(1, QFormLayout.ItemRole.FieldRole, self.grp_linux_capture)

        self.lbl_mac_capture = QLabel(self.tab_opencv)
        self.lbl_mac_capture.setObjectName(u"lbl_mac_capture")

        self.frm_opencv.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_mac_capture)

        self.grp_mac_capture = QGroupBox(self.tab_opencv)
        self.grp_mac_capture.setObjectName(u"grp_mac_capture")
        self.hboxLayout2 = QHBoxLayout(self.grp_mac_capture)
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.rb_mac_avfoundation = QRadioButton(self.grp_mac_capture)
        self.rb_mac_avfoundation.setObjectName(u"rb_mac_avfoundation")
        self.rb_mac_avfoundation.setChecked(True)
        self.rb_mac_avfoundation.setProperty(u"dataclass_property", u"opencv_mac_capture")

        self.hboxLayout2.addWidget(self.rb_mac_avfoundation)

        self.rb_mac_any = QRadioButton(self.grp_mac_capture)
        self.rb_mac_any.setObjectName(u"rb_mac_any")
        self.rb_mac_any.setProperty(u"dataclass_property", u"opencv_mac_capture")

        self.hboxLayout2.addWidget(self.rb_mac_any)

        self.hs_mac_capture = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout2.addItem(self.hs_mac_capture)


        self.frm_opencv.setWidget(2, QFormLayout.ItemRole.FieldRole, self.grp_mac_capture)

        self.lbl_windows_capture = QLabel(self.tab_opencv)
        self.lbl_windows_capture.setObjectName(u"lbl_windows_capture")

        self.frm_opencv.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_windows_capture)

        self.grp_windows_capture = QGroupBox(self.tab_opencv)
        self.grp_windows_capture.setObjectName(u"grp_windows_capture")
        self.hboxLayout3 = QHBoxLayout(self.grp_windows_capture)
        self.hboxLayout3.setObjectName(u"hboxLayout3")
        self.rb_windows_dshow = QRadioButton(self.grp_windows_capture)
        self.rb_windows_dshow.setObjectName(u"rb_windows_dshow")
        self.rb_windows_dshow.setChecked(True)
        self.rb_windows_dshow.setProperty(u"dataclass_property", u"opencv_windows_capture")

        self.hboxLayout3.addWidget(self.rb_windows_dshow)

        self.rb_windows_msmf = QRadioButton(self.grp_windows_capture)
        self.rb_windows_msmf.setObjectName(u"rb_windows_msmf")
        self.rb_windows_msmf.setProperty(u"dataclass_property", u"opencv_windows_capture")

        self.hboxLayout3.addWidget(self.rb_windows_msmf)

        self.hs_windows_capture = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout3.addItem(self.hs_windows_capture)


        self.frm_opencv.setWidget(3, QFormLayout.ItemRole.FieldRole, self.grp_windows_capture)

        self.lbl_buffer_size = QLabel(self.tab_opencv)
        self.lbl_buffer_size.setObjectName(u"lbl_buffer_size")

        self.frm_opencv.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_buffer_size)

        self.spn_buffer_size = QSpinBox(self.tab_opencv)
        self.spn_buffer_size.setObjectName(u"spn_buffer_size")
        self.spn_buffer_size.setMinimum(1)
        self.spn_buffer_size.setMaximum(5)
        self.spn_buffer_size.setSingleStep(1)
        self.spn_buffer_size.setValue(1)
        self.spn_buffer_size.setProperty(u"dataclass_property", u"opencv_buffer_size")

        self.frm_opencv.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spn_buffer_size)

        self.lbl_custom_camera = QLabel(self.tab_opencv)
        self.lbl_custom_camera.setObjectName(u"lbl_custom_camera")

        self.frm_opencv.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_custom_camera)

        self.chk_custom_camera = QCheckBox(self.tab_opencv)
        self.chk_custom_camera.setObjectName(u"chk_custom_camera")
        self.chk_custom_camera.setChecked(False)
        self.chk_custom_camera.setProperty(u"dataclass_property", u"opencv_custom_camera")

        self.frm_opencv.setWidget(5, QFormLayout.ItemRole.FieldRole, self.chk_custom_camera)


        self.lay_opencv.addLayout(self.frm_opencv)

        self.grp_camera_info = QGroupBox(self.tab_opencv)
        self.grp_camera_info.setObjectName(u"grp_camera_info")
        self.grp_camera_info.setEnabled(False)
        self.grp_camera_info.setCheckable(False)
        self.form_camera = QFormLayout(self.grp_camera_info)
        self.form_camera.setObjectName(u"form_camera")
        self.form_camera.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_ratio = QLabel(self.grp_camera_info)
        self.lbl_ratio.setObjectName(u"lbl_ratio")

        self.form_camera.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_ratio)

        self.cbx_ratio = QComboBox(self.grp_camera_info)
        self.cbx_ratio.setObjectName(u"cbx_ratio")
        self.cbx_ratio.setEnabled(False)
        self.cbx_ratio.setEditable(False)
        self.cbx_ratio.setMaxVisibleItems(5)
        self.cbx_ratio.setProperty(u"dataclass_property", u"opencv_ratio")

        self.form_camera.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbx_ratio)

        self.lbl_width = QLabel(self.grp_camera_info)
        self.lbl_width.setObjectName(u"lbl_width")

        self.form_camera.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_width)

        self.spn_camera_width = QSpinBox(self.grp_camera_info)
        self.spn_camera_width.setObjectName(u"spn_camera_width")
        self.spn_camera_width.setMinimum(640)
        self.spn_camera_width.setMaximum(1920)
        self.spn_camera_width.setSingleStep(1)
        self.spn_camera_width.setValue(640)
        self.spn_camera_width.setProperty(u"dataclass_property", u"opencv_width")

        self.form_camera.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spn_camera_width)

        self.lbl_height = QLabel(self.grp_camera_info)
        self.lbl_height.setObjectName(u"lbl_height")

        self.form_camera.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_height)

        self.spn_camera_height = QSpinBox(self.grp_camera_info)
        self.spn_camera_height.setObjectName(u"spn_camera_height")
        self.spn_camera_height.setMinimum(480)
        self.spn_camera_height.setMaximum(1080)
        self.spn_camera_height.setSingleStep(1)
        self.spn_camera_height.setValue(480)
        self.spn_camera_height.setProperty(u"dataclass_property", u"opencv_height")

        self.form_camera.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spn_camera_height)

        self.lbl_fps = QLabel(self.grp_camera_info)
        self.lbl_fps.setObjectName(u"lbl_fps")

        self.form_camera.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_fps)

        self.grp_fps = QGroupBox(self.grp_camera_info)
        self.grp_fps.setObjectName(u"grp_fps")
        self.grp_fps.setEnabled(False)
        self.hboxLayout4 = QHBoxLayout(self.grp_fps)
        self.hboxLayout4.setObjectName(u"hboxLayout4")
        self.rb_fps_30 = QRadioButton(self.grp_fps)
        self.rb_fps_30.setObjectName(u"rb_fps_30")
        self.rb_fps_30.setChecked(True)
        self.rb_fps_30.setProperty(u"dataclass_property", u"opencv_fps")

        self.hboxLayout4.addWidget(self.rb_fps_30)

        self.rb_fps_60 = QRadioButton(self.grp_fps)
        self.rb_fps_60.setObjectName(u"rb_fps_60")
        self.rb_fps_60.setProperty(u"dataclass_property", u"opencv_fps")

        self.hboxLayout4.addWidget(self.rb_fps_60)

        self.hs_fps = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout4.addItem(self.hs_fps)


        self.form_camera.setWidget(3, QFormLayout.ItemRole.FieldRole, self.grp_fps)


        self.lay_opencv.addWidget(self.grp_camera_info)

        self.vs_opencv = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_opencv.addItem(self.vs_opencv)

        self.tab_widget.addTab(self.tab_opencv, "")
        self.tab_filter = QWidget()
        self.tab_filter.setObjectName(u"tab_filter")
        self.lay_filter = QVBoxLayout(self.tab_filter)
        self.lay_filter.setSpacing(10)
        self.lay_filter.setObjectName(u"lay_filter")
        self.lay_filter.setContentsMargins(12, 12, 12, 12)
        self.frm_filter = QFormLayout()
        self.frm_filter.setObjectName(u"frm_filter")
        self.frm_filter.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_use_filter = QLabel(self.tab_filter)
        self.lbl_use_filter.setObjectName(u"lbl_use_filter")

        self.frm_filter.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_use_filter)

        self.chk_enable_filter = QCheckBox(self.tab_filter)
        self.chk_enable_filter.setObjectName(u"chk_enable_filter")
        self.chk_enable_filter.setChecked(False)
        self.chk_enable_filter.setProperty(u"dataclass_property", u"filter_enable_filter")

        self.frm_filter.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chk_enable_filter)


        self.lay_filter.addLayout(self.frm_filter)

        self.grp_filter = QGroupBox(self.tab_filter)
        self.grp_filter.setObjectName(u"grp_filter")
        self.grp_filter.setEnabled(False)
        self.form_filters = QFormLayout(self.grp_filter)
        self.form_filters.setObjectName(u"form_filters")
        self.form_filters.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_average_smooth_frames = QLabel(self.grp_filter)
        self.lbl_average_smooth_frames.setObjectName(u"lbl_average_smooth_frames")

        self.form_filters.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_average_smooth_frames)

        self.spn_average_smooth_frames = QSpinBox(self.grp_filter)
        self.spn_average_smooth_frames.setObjectName(u"spn_average_smooth_frames")
        self.spn_average_smooth_frames.setMinimum(5)
        self.spn_average_smooth_frames.setMaximum(10)
        self.spn_average_smooth_frames.setSingleStep(1)
        self.spn_average_smooth_frames.setValue(5)
        self.spn_average_smooth_frames.setProperty(u"dataclass_property", u"filter_average_smooth_frames")

        self.form_filters.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spn_average_smooth_frames)

        self.lbl_clahe_clip = QLabel(self.grp_filter)
        self.lbl_clahe_clip.setObjectName(u"lbl_clahe_clip")

        self.form_filters.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_clahe_clip)

        self.spn_clahe_clip = QSpinBox(self.grp_filter)
        self.spn_clahe_clip.setObjectName(u"spn_clahe_clip")
        self.spn_clahe_clip.setMinimum(1)
        self.spn_clahe_clip.setMaximum(10)
        self.spn_clahe_clip.setSingleStep(1)
        self.spn_clahe_clip.setValue(2)
        self.spn_clahe_clip.setProperty(u"dataclass_property", u"filter_clahe_clip")

        self.form_filters.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spn_clahe_clip)

        self.lbl_clahe_grid = QLabel(self.grp_filter)
        self.lbl_clahe_grid.setObjectName(u"lbl_clahe_grid")

        self.form_filters.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_clahe_grid)

        self.cbx_clahe_grid = QComboBox(self.grp_filter)
        self.cbx_clahe_grid.addItem("")
        self.cbx_clahe_grid.addItem("")
        self.cbx_clahe_grid.addItem("")
        self.cbx_clahe_grid.addItem("")
        self.cbx_clahe_grid.setObjectName(u"cbx_clahe_grid")
        self.cbx_clahe_grid.setProperty(u"dataclass_property", u"filter_clahe_grid")

        self.form_filters.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbx_clahe_grid)

        self.lbl_clahe_lum_below = QLabel(self.grp_filter)
        self.lbl_clahe_lum_below.setObjectName(u"lbl_clahe_lum_below")

        self.form_filters.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_clahe_lum_below)

        self.spn_clahe_lum_below = QSpinBox(self.grp_filter)
        self.spn_clahe_lum_below.setObjectName(u"spn_clahe_lum_below")
        self.spn_clahe_lum_below.setMinimum(50)
        self.spn_clahe_lum_below.setMaximum(150)
        self.spn_clahe_lum_below.setSingleStep(1)
        self.spn_clahe_lum_below.setValue(100)
        self.spn_clahe_lum_below.setProperty(u"dataclass_property", u"filter_clahe_lum_below")

        self.form_filters.setWidget(3, QFormLayout.ItemRole.FieldRole, self.spn_clahe_lum_below)

        self.lbl_gamma_factor = QLabel(self.grp_filter)
        self.lbl_gamma_factor.setObjectName(u"lbl_gamma_factor")

        self.form_filters.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_gamma_factor)

        self.spn_gamma_factor = QDoubleSpinBox(self.grp_filter)
        self.spn_gamma_factor.setObjectName(u"spn_gamma_factor")
        self.spn_gamma_factor.setDecimals(1)
        self.spn_gamma_factor.setMinimum(1.000000000000000)
        self.spn_gamma_factor.setMaximum(10.000000000000000)
        self.spn_gamma_factor.setSingleStep(0.100000000000000)
        self.spn_gamma_factor.setValue(1.200000000000000)
        self.spn_gamma_factor.setProperty(u"dataclass_property", u"filter_gamma_factor")

        self.form_filters.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spn_gamma_factor)

        self.lbl_gamma_lum_above = QLabel(self.grp_filter)
        self.lbl_gamma_lum_above.setObjectName(u"lbl_gamma_lum_above")

        self.form_filters.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_gamma_lum_above)

        self.spn_gamma_lum_above = QSpinBox(self.grp_filter)
        self.spn_gamma_lum_above.setObjectName(u"spn_gamma_lum_above")
        self.spn_gamma_lum_above.setMinimum(100)
        self.spn_gamma_lum_above.setMaximum(200)
        self.spn_gamma_lum_above.setSingleStep(1)
        self.spn_gamma_lum_above.setValue(150)
        self.spn_gamma_lum_above.setProperty(u"dataclass_property", u"filter_gamma_lum_above")

        self.form_filters.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spn_gamma_lum_above)

        self.lbl_landmark_limit = QLabel(self.grp_filter)
        self.lbl_landmark_limit.setObjectName(u"lbl_landmark_limit")

        self.form_filters.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lbl_landmark_limit)

        self.spn_landmark_limit = QDoubleSpinBox(self.grp_filter)
        self.spn_landmark_limit.setObjectName(u"spn_landmark_limit")
        self.spn_landmark_limit.setDecimals(2)
        self.spn_landmark_limit.setMinimum(0.000000000000000)
        self.spn_landmark_limit.setMaximum(1.000000000000000)
        self.spn_landmark_limit.setSingleStep(0.010000000000000)
        self.spn_landmark_limit.setValue(0.150000000000000)
        self.spn_landmark_limit.setProperty(u"dataclass_property", u"filter_landmark_limit")

        self.form_filters.setWidget(6, QFormLayout.ItemRole.FieldRole, self.spn_landmark_limit)


        self.lay_filter.addWidget(self.grp_filter)

        self.vs_filter = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_filter.addItem(self.vs_filter)

        self.tab_widget.addTab(self.tab_filter, "")
        self.tab_telemetry = QWidget()
        self.tab_telemetry.setObjectName(u"tab_telemetry")
        self.lay_telemetry = QVBoxLayout(self.tab_telemetry)
        self.lay_telemetry.setObjectName(u"lay_telemetry")
        self.frm_telemetry = QFormLayout()
        self.frm_telemetry.setObjectName(u"frm_telemetry")
        self.frm_telemetry.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_enable_telemetry_panel = QLabel(self.tab_telemetry)
        self.lbl_enable_telemetry_panel.setObjectName(u"lbl_enable_telemetry_panel")

        self.frm_telemetry.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_enable_telemetry_panel)

        self.chk_habilitar_painel_telemetria = QCheckBox(self.tab_telemetry)
        self.chk_habilitar_painel_telemetria.setObjectName(u"chk_habilitar_painel_telemetria")
        self.chk_habilitar_painel_telemetria.setChecked(True)
        self.chk_habilitar_painel_telemetria.setProperty(u"dataclass_property", u"telemetry_enable_telemetry_panel")

        self.frm_telemetry.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chk_habilitar_painel_telemetria)


        self.lay_telemetry.addLayout(self.frm_telemetry)

        self.vs_telemetry = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_telemetry.addItem(self.vs_telemetry)

        self.tab_widget.addTab(self.tab_telemetry, "")
        self.tab_automatic_calibration = QWidget()
        self.tab_automatic_calibration.setObjectName(u"tab_automatic_calibration")
        self.lay_calibracao_automatica = QVBoxLayout(self.tab_automatic_calibration)
        self.lay_calibracao_automatica.setObjectName(u"lay_calibracao_automatica")
        self.grp_window_automatic = QGroupBox(self.tab_automatic_calibration)
        self.grp_window_automatic.setObjectName(u"grp_window_automatic")
        self.frm_janela_automatic = QFormLayout(self.grp_window_automatic)
        self.frm_janela_automatic.setObjectName(u"frm_janela_automatic")
        self.frm_janela_automatic.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_window_position_automatic = QLabel(self.grp_window_automatic)
        self.lbl_window_position_automatic.setObjectName(u"lbl_window_position_automatic")

        self.frm_janela_automatic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_window_position_automatic)

        self.grp_window_position_automatic = QGroupBox(self.grp_window_automatic)
        self.grp_window_position_automatic.setObjectName(u"grp_window_position_automatic")
        self.horizontalLayout_window_position_automatic = QHBoxLayout(self.grp_window_position_automatic)
        self.horizontalLayout_window_position_automatic.setObjectName(u"horizontalLayout_window_position_automatic")
        self.rb_top_left_automatic = QRadioButton(self.grp_window_position_automatic)
        self.rb_top_left_automatic.setObjectName(u"rb_top_left_automatic")
        self.rb_top_left_automatic.setChecked(True)
        self.rb_top_left_automatic.setProperty(u"dataclass_property", u"automatic_window_position_automatic")
        self.rb_top_left_automatic.setProperty(u"dataclass_property_value", u"topLeft")

        self.horizontalLayout_window_position_automatic.addWidget(self.rb_top_left_automatic)

        self.hs_window_position_automatic = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_window_position_automatic.addItem(self.hs_window_position_automatic)


        self.frm_janela_automatic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grp_window_position_automatic)

        self.lbl_window_open_automatic = QLabel(self.grp_window_automatic)
        self.lbl_window_open_automatic.setObjectName(u"lbl_window_open_automatic")

        self.frm_janela_automatic.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_window_open_automatic)

        self.grp_window_open_automatic = QGroupBox(self.grp_window_automatic)
        self.grp_window_open_automatic.setObjectName(u"grp_window_open_automatic")
        self.horizontalLayout_abertura_janela_automatica = QHBoxLayout(self.grp_window_open_automatic)
        self.horizontalLayout_abertura_janela_automatica.setObjectName(u"horizontalLayout_abertura_janela_automatica")
        self.rb_window_full_screen_automatic = QRadioButton(self.grp_window_open_automatic)
        self.rb_window_full_screen_automatic.setObjectName(u"rb_window_full_screen_automatic")
        self.rb_window_full_screen_automatic.setChecked(True)
        self.rb_window_full_screen_automatic.setProperty(u"dataclass_property", u"automatic_window_open_automatic")
        self.rb_window_full_screen_automatic.setProperty(u"dataclass_property_value", u"1")

        self.horizontalLayout_abertura_janela_automatica.addWidget(self.rb_window_full_screen_automatic)

        self.rb_window_maximized_screen_automatic = QRadioButton(self.grp_window_open_automatic)
        self.rb_window_maximized_screen_automatic.setObjectName(u"rb_window_maximized_screen_automatic")
        self.rb_window_maximized_screen_automatic.setProperty(u"dataclass_property", u"automatic_window_open_automatic")
        self.rb_window_maximized_screen_automatic.setProperty(u"dataclass_property_value", u"2")

        self.horizontalLayout_abertura_janela_automatica.addWidget(self.rb_window_maximized_screen_automatic)

        self.rb_window_maximized_screen_util_automatic = QRadioButton(self.grp_window_open_automatic)
        self.rb_window_maximized_screen_util_automatic.setObjectName(u"rb_window_maximized_screen_util_automatic")
        self.rb_window_maximized_screen_util_automatic.setProperty(u"dataclass_property", u"automatic_window_open_automatic")
        self.rb_window_maximized_screen_util_automatic.setProperty(u"dataclass_property_value", u"3")

        self.horizontalLayout_abertura_janela_automatica.addWidget(self.rb_window_maximized_screen_util_automatic)

        self.hs_window_open_automatic = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_abertura_janela_automatica.addItem(self.hs_window_open_automatic)


        self.frm_janela_automatic.setWidget(1, QFormLayout.ItemRole.FieldRole, self.grp_window_open_automatic)

        self.lbl_open_projector_automatic = QLabel(self.grp_window_automatic)
        self.lbl_open_projector_automatic.setObjectName(u"lbl_open_projector_automatic")

        self.frm_janela_automatic.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_open_projector_automatic)

        self.chk_open_projector_automatic = QCheckBox(self.grp_window_automatic)
        self.chk_open_projector_automatic.setObjectName(u"chk_open_projector_automatic")
        self.chk_open_projector_automatic.setChecked(True)
        self.chk_open_projector_automatic.setProperty(u"dataclass_property", u"automatic_open_projector_automatic")

        self.frm_janela_automatic.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chk_open_projector_automatic)

        self.lbl_default_calibration_automatic = QLabel(self.grp_window_automatic)
        self.lbl_default_calibration_automatic.setObjectName(u"lbl_default_calibration_automatic")

        self.frm_janela_automatic.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_default_calibration_automatic)

        self.chk_default_calibration_automatic = QCheckBox(self.grp_window_automatic)
        self.chk_default_calibration_automatic.setObjectName(u"chk_default_calibration_automatic")
        self.chk_default_calibration_automatic.setChecked(False)
        self.chk_default_calibration_automatic.setProperty(u"dataclass_property", u"automatic_default_calibration_automatic")

        self.frm_janela_automatic.setWidget(3, QFormLayout.ItemRole.FieldRole, self.chk_default_calibration_automatic)


        self.lay_calibracao_automatica.addWidget(self.grp_window_automatic)

        self.grp_calibration_points_automatic = QGroupBox(self.tab_automatic_calibration)
        self.grp_calibration_points_automatic.setObjectName(u"grp_calibration_points_automatic")
        self.frm_pontos_calibracao_automatic = QFormLayout(self.grp_calibration_points_automatic)
        self.frm_pontos_calibracao_automatic.setObjectName(u"frm_pontos_calibracao_automatic")
        self.frm_pontos_calibracao_automatic.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_mirror_mode_automatic = QLabel(self.grp_calibration_points_automatic)
        self.lbl_mirror_mode_automatic.setObjectName(u"lbl_mirror_mode_automatic")

        self.frm_pontos_calibracao_automatic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_mirror_mode_automatic)

        self.chk_mirror_mode_automatic = QCheckBox(self.grp_calibration_points_automatic)
        self.chk_mirror_mode_automatic.setObjectName(u"chk_mirror_mode_automatic")
        self.chk_mirror_mode_automatic.setChecked(True)
        self.chk_mirror_mode_automatic.setProperty(u"dataclass_property", u"automatic_mirror_mode_automatic")

        self.frm_pontos_calibracao_automatic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chk_mirror_mode_automatic)


        self.lay_calibracao_automatica.addWidget(self.grp_calibration_points_automatic)

        self.grp_automatic_marker = QGroupBox(self.tab_automatic_calibration)
        self.grp_automatic_marker.setObjectName(u"grp_automatic_marker")
        self.frm_marcador_automatic = QFormLayout(self.grp_automatic_marker)
        self.frm_marcador_automatic.setObjectName(u"frm_marcador_automatic")
        self.frm_marcador_automatic.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_num_columns_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_num_columns_automatic.setObjectName(u"lbl_num_columns_automatic")

        self.frm_marcador_automatic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_num_columns_automatic)

        self.spn_num_columns_automatic = QSpinBox(self.grp_automatic_marker)
        self.spn_num_columns_automatic.setObjectName(u"spn_num_columns_automatic")
        self.spn_num_columns_automatic.setMinimum(1)
        self.spn_num_columns_automatic.setMaximum(50)
        self.spn_num_columns_automatic.setSingleStep(1)
        self.spn_num_columns_automatic.setValue(6)
        self.spn_num_columns_automatic.setProperty(u"dataclass_property", u"automatic_num_columns_automatic")

        self.frm_marcador_automatic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spn_num_columns_automatic)

        self.lbl_num_rows_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_num_rows_automatic.setObjectName(u"lbl_num_rows_automatic")

        self.frm_marcador_automatic.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_num_rows_automatic)

        self.spn_num_rows_automatic = QSpinBox(self.grp_automatic_marker)
        self.spn_num_rows_automatic.setObjectName(u"spn_num_rows_automatic")
        self.spn_num_rows_automatic.setMinimum(1)
        self.spn_num_rows_automatic.setMaximum(50)
        self.spn_num_rows_automatic.setSingleStep(1)
        self.spn_num_rows_automatic.setValue(4)
        self.spn_num_rows_automatic.setProperty(u"dataclass_property", u"automatic_num_rows_automatic")

        self.frm_marcador_automatic.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spn_num_rows_automatic)

        self.lbl_multiplier_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_multiplier_automatic.setObjectName(u"lbl_multiplier_automatic")

        self.frm_marcador_automatic.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_multiplier_automatic)

        self.spn_multiplier_automatic = QDoubleSpinBox(self.grp_automatic_marker)
        self.spn_multiplier_automatic.setObjectName(u"spn_multiplier_automatic")
        self.spn_multiplier_automatic.setDecimals(2)
        self.spn_multiplier_automatic.setMinimum(0.010000000000000)
        self.spn_multiplier_automatic.setMaximum(1.000000000000000)
        self.spn_multiplier_automatic.setSingleStep(0.010000000000000)
        self.spn_multiplier_automatic.setValue(0.750000000000000)
        self.spn_multiplier_automatic.setProperty(u"dataclass_property", u"automatic_multiplier_automatic")

        self.frm_marcador_automatic.setWidget(2, QFormLayout.ItemRole.FieldRole, self.spn_multiplier_automatic)

        self.lbl_dictionary_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_dictionary_automatic.setObjectName(u"lbl_dictionary_automatic")

        self.frm_marcador_automatic.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_dictionary_automatic)

        self.cbx_dictionary_automatic = QComboBox(self.grp_automatic_marker)
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.addItem("")
        self.cbx_dictionary_automatic.setObjectName(u"cbx_dictionary_automatic")
        self.cbx_dictionary_automatic.setProperty(u"dataclass_property", u"automatic_dictionary_automatic")

        self.frm_marcador_automatic.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cbx_dictionary_automatic)

        self.lbl_width_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_width_automatic.setObjectName(u"lbl_width_automatic")

        self.frm_marcador_automatic.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lbl_width_automatic)

        self.spn_width_automatic = QSpinBox(self.grp_automatic_marker)
        self.spn_width_automatic.setObjectName(u"spn_width_automatic")
        self.spn_width_automatic.setMinimum(10)
        self.spn_width_automatic.setMaximum(150)
        self.spn_width_automatic.setSingleStep(1)
        self.spn_width_automatic.setValue(100)
        self.spn_width_automatic.setProperty(u"dataclass_property", u"automatic_width_automatic")

        self.frm_marcador_automatic.setWidget(4, QFormLayout.ItemRole.FieldRole, self.spn_width_automatic)

        self.lbl_height_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_height_automatic.setObjectName(u"lbl_height_automatic")

        self.frm_marcador_automatic.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lbl_height_automatic)

        self.spn_height_automatic = QSpinBox(self.grp_automatic_marker)
        self.spn_height_automatic.setObjectName(u"spn_height_automatic")
        self.spn_height_automatic.setMinimum(10)
        self.spn_height_automatic.setMaximum(150)
        self.spn_height_automatic.setSingleStep(1)
        self.spn_height_automatic.setValue(100)
        self.spn_height_automatic.setProperty(u"dataclass_property", u"automatic_height_automatic")

        self.frm_marcador_automatic.setWidget(5, QFormLayout.ItemRole.FieldRole, self.spn_height_automatic)

        self.lbl_margin_automatic = QLabel(self.grp_automatic_marker)
        self.lbl_margin_automatic.setObjectName(u"lbl_margin_automatic")

        self.frm_marcador_automatic.setWidget(6, QFormLayout.ItemRole.LabelRole, self.lbl_margin_automatic)

        self.spn_margin_automatic = QSpinBox(self.grp_automatic_marker)
        self.spn_margin_automatic.setObjectName(u"spn_margin_automatic")
        self.spn_margin_automatic.setMinimum(0)
        self.spn_margin_automatic.setMaximum(100)
        self.spn_margin_automatic.setSingleStep(1)
        self.spn_margin_automatic.setValue(0)
        self.spn_margin_automatic.setProperty(u"dataclass_property", u"automatic_margin_automatic")

        self.frm_marcador_automatic.setWidget(6, QFormLayout.ItemRole.FieldRole, self.spn_margin_automatic)


        self.lay_calibracao_automatica.addWidget(self.grp_automatic_marker)

        self.vs_calibration_automatic = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_calibracao_automatica.addItem(self.vs_calibration_automatic)

        self.tab_widget.addTab(self.tab_automatic_calibration, "")
        self.tab_semiautomatic_calibration = QWidget()
        self.tab_semiautomatic_calibration.setObjectName(u"tab_semiautomatic_calibration")
        self.lay_calibracao_semi_automatica = QVBoxLayout(self.tab_semiautomatic_calibration)
        self.lay_calibracao_semi_automatica.setObjectName(u"lay_calibracao_semi_automatica")
        self.grp_window_semiautomatic = QGroupBox(self.tab_semiautomatic_calibration)
        self.grp_window_semiautomatic.setObjectName(u"grp_window_semiautomatic")
        self.frm_janela_semiautomatic = QFormLayout(self.grp_window_semiautomatic)
        self.frm_janela_semiautomatic.setObjectName(u"frm_janela_semiautomatic")
        self.frm_janela_semiautomatic.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_window_position_semiautomatic = QLabel(self.grp_window_semiautomatic)
        self.lbl_window_position_semiautomatic.setObjectName(u"lbl_window_position_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_window_position_semiautomatic)

        self.grp_window_position_semiautomatic = QGroupBox(self.grp_window_semiautomatic)
        self.grp_window_position_semiautomatic.setObjectName(u"grp_window_position_semiautomatic")
        self.horizontalLayout_window_position_semiautomatic = QHBoxLayout(self.grp_window_position_semiautomatic)
        self.horizontalLayout_window_position_semiautomatic.setObjectName(u"horizontalLayout_window_position_semiautomatic")
        self.rb_top_left_semiautomatic = QRadioButton(self.grp_window_position_semiautomatic)
        self.rb_top_left_semiautomatic.setObjectName(u"rb_top_left_semiautomatic")
        self.rb_top_left_semiautomatic.setChecked(True)
        self.rb_top_left_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_window_position_semiautomatic")
        self.rb_top_left_semiautomatic.setProperty(u"dataclass_property_value", u"topLeft")

        self.horizontalLayout_window_position_semiautomatic.addWidget(self.rb_top_left_semiautomatic)

        self.hs_window_position_semiautomatic = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_window_position_semiautomatic.addItem(self.hs_window_position_semiautomatic)


        self.frm_janela_semiautomatic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grp_window_position_semiautomatic)

        self.lbl_window_open_semiautomatic = QLabel(self.grp_window_semiautomatic)
        self.lbl_window_open_semiautomatic.setObjectName(u"lbl_window_open_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_window_open_semiautomatic)

        self.grp_window_open_semiautomatic = QGroupBox(self.grp_window_semiautomatic)
        self.grp_window_open_semiautomatic.setObjectName(u"grp_window_open_semiautomatic")
        self.horizontalLayout_abertura_janela_semi_automatica = QHBoxLayout(self.grp_window_open_semiautomatic)
        self.horizontalLayout_abertura_janela_semi_automatica.setObjectName(u"horizontalLayout_abertura_janela_semi_automatica")
        self.rb_window_full_screen_semiautomatic = QRadioButton(self.grp_window_open_semiautomatic)
        self.rb_window_full_screen_semiautomatic.setObjectName(u"rb_window_full_screen_semiautomatic")
        self.rb_window_full_screen_semiautomatic.setChecked(True)
        self.rb_window_full_screen_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_window_open_semiautomatic")
        self.rb_window_full_screen_semiautomatic.setProperty(u"dataclass_property_value", u"1")

        self.horizontalLayout_abertura_janela_semi_automatica.addWidget(self.rb_window_full_screen_semiautomatic)

        self.rb_window_maximized_screen_semiautomatic = QRadioButton(self.grp_window_open_semiautomatic)
        self.rb_window_maximized_screen_semiautomatic.setObjectName(u"rb_window_maximized_screen_semiautomatic")
        self.rb_window_maximized_screen_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_window_open_semiautomatic")
        self.rb_window_maximized_screen_semiautomatic.setProperty(u"dataclass_property_value", u"2")

        self.horizontalLayout_abertura_janela_semi_automatica.addWidget(self.rb_window_maximized_screen_semiautomatic)

        self.rb_window_maximized_screen_util_semiautomatic = QRadioButton(self.grp_window_open_semiautomatic)
        self.rb_window_maximized_screen_util_semiautomatic.setObjectName(u"rb_window_maximized_screen_util_semiautomatic")
        self.rb_window_maximized_screen_util_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_window_open_semiautomatic")
        self.rb_window_maximized_screen_util_semiautomatic.setProperty(u"dataclass_property_value", u"3")

        self.horizontalLayout_abertura_janela_semi_automatica.addWidget(self.rb_window_maximized_screen_util_semiautomatic)

        self.hs_window_open_semiautomatic = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_abertura_janela_semi_automatica.addItem(self.hs_window_open_semiautomatic)


        self.frm_janela_semiautomatic.setWidget(1, QFormLayout.ItemRole.FieldRole, self.grp_window_open_semiautomatic)

        self.lbl_open_projector_semiautomatic = QLabel(self.grp_window_semiautomatic)
        self.lbl_open_projector_semiautomatic.setObjectName(u"lbl_open_projector_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_open_projector_semiautomatic)

        self.chk_open_projector_semiautomatic = QCheckBox(self.grp_window_semiautomatic)
        self.chk_open_projector_semiautomatic.setObjectName(u"chk_open_projector_semiautomatic")
        self.chk_open_projector_semiautomatic.setChecked(True)
        self.chk_open_projector_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_open_projector_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chk_open_projector_semiautomatic)

        self.lbl_default_calibration_semiautomatic = QLabel(self.grp_window_semiautomatic)
        self.lbl_default_calibration_semiautomatic.setObjectName(u"lbl_default_calibration_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_default_calibration_semiautomatic)

        self.chk_default_calibration_semiautomatic = QCheckBox(self.grp_window_semiautomatic)
        self.chk_default_calibration_semiautomatic.setObjectName(u"chk_default_calibration_semiautomatic")
        self.chk_default_calibration_semiautomatic.setChecked(False)
        self.chk_default_calibration_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_default_calibration_semiautomatic")

        self.frm_janela_semiautomatic.setWidget(3, QFormLayout.ItemRole.FieldRole, self.chk_default_calibration_semiautomatic)


        self.lay_calibracao_semi_automatica.addWidget(self.grp_window_semiautomatic)

        self.grp_calibration_points_semiautomatic = QGroupBox(self.tab_semiautomatic_calibration)
        self.grp_calibration_points_semiautomatic.setObjectName(u"grp_calibration_points_semiautomatic")
        self.frm_pontos_calibracao_semiautomatic = QFormLayout(self.grp_calibration_points_semiautomatic)
        self.frm_pontos_calibracao_semiautomatic.setObjectName(u"frm_pontos_calibracao_semiautomatic")
        self.frm_pontos_calibracao_semiautomatic.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_mirror_mode_semiautomatic = QLabel(self.grp_calibration_points_semiautomatic)
        self.lbl_mirror_mode_semiautomatic.setObjectName(u"lbl_mirror_mode_semiautomatic")

        self.frm_pontos_calibracao_semiautomatic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_mirror_mode_semiautomatic)

        self.chk_mirror_mode_semiautomatic = QCheckBox(self.grp_calibration_points_semiautomatic)
        self.chk_mirror_mode_semiautomatic.setObjectName(u"chk_mirror_mode_semiautomatic")
        self.chk_mirror_mode_semiautomatic.setChecked(True)
        self.chk_mirror_mode_semiautomatic.setProperty(u"dataclass_property", u"semiautomatic_mirror_mode_semiautomatic")

        self.frm_pontos_calibracao_semiautomatic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chk_mirror_mode_semiautomatic)


        self.lay_calibracao_semi_automatica.addWidget(self.grp_calibration_points_semiautomatic)

        self.vs_calibration_semiautomatic = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_calibracao_semi_automatica.addItem(self.vs_calibration_semiautomatic)

        self.tab_widget.addTab(self.tab_semiautomatic_calibration, "")
        self.tab_manual_calibration = QWidget()
        self.tab_manual_calibration.setObjectName(u"tab_manual_calibration")
        self.lay_calibracao_manual = QVBoxLayout(self.tab_manual_calibration)
        self.lay_calibracao_manual.setObjectName(u"lay_calibracao_manual")
        self.grp_window_manual = QGroupBox(self.tab_manual_calibration)
        self.grp_window_manual.setObjectName(u"grp_window_manual")
        self.frm_janela_manual = QFormLayout(self.grp_window_manual)
        self.frm_janela_manual.setObjectName(u"frm_janela_manual")
        self.frm_janela_manual.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_window_position_manual = QLabel(self.grp_window_manual)
        self.lbl_window_position_manual.setObjectName(u"lbl_window_position_manual")

        self.frm_janela_manual.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_window_position_manual)

        self.grp_window_position_manual = QGroupBox(self.grp_window_manual)
        self.grp_window_position_manual.setObjectName(u"grp_window_position_manual")
        self.horizontalLayout_window_position_manual = QHBoxLayout(self.grp_window_position_manual)
        self.horizontalLayout_window_position_manual.setObjectName(u"horizontalLayout_window_position_manual")
        self.rb_top_left_manual = QRadioButton(self.grp_window_position_manual)
        self.rb_top_left_manual.setObjectName(u"rb_top_left_manual")
        self.rb_top_left_manual.setChecked(True)
        self.rb_top_left_manual.setProperty(u"dataclass_property", u"manual_window_position_manual")
        self.rb_top_left_manual.setProperty(u"dataclass_property_value", u"topLeft")

        self.horizontalLayout_window_position_manual.addWidget(self.rb_top_left_manual)

        self.hs_window_position_manual = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_window_position_manual.addItem(self.hs_window_position_manual)


        self.frm_janela_manual.setWidget(0, QFormLayout.ItemRole.FieldRole, self.grp_window_position_manual)

        self.lbl_window_open_manual = QLabel(self.grp_window_manual)
        self.lbl_window_open_manual.setObjectName(u"lbl_window_open_manual")

        self.frm_janela_manual.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lbl_window_open_manual)

        self.grp_window_open_manual = QGroupBox(self.grp_window_manual)
        self.grp_window_open_manual.setObjectName(u"grp_window_open_manual")
        self.horizontalLayout_abertura_janela_manual = QHBoxLayout(self.grp_window_open_manual)
        self.horizontalLayout_abertura_janela_manual.setObjectName(u"horizontalLayout_abertura_janela_manual")
        self.rb_window_full_screen_manual = QRadioButton(self.grp_window_open_manual)
        self.rb_window_full_screen_manual.setObjectName(u"rb_window_full_screen_manual")
        self.rb_window_full_screen_manual.setChecked(True)
        self.rb_window_full_screen_manual.setProperty(u"dataclass_property", u"manual_window_open_manual")
        self.rb_window_full_screen_manual.setProperty(u"dataclass_property_value", u"1")

        self.horizontalLayout_abertura_janela_manual.addWidget(self.rb_window_full_screen_manual)

        self.rb_window_maximized_screen_manual = QRadioButton(self.grp_window_open_manual)
        self.rb_window_maximized_screen_manual.setObjectName(u"rb_window_maximized_screen_manual")
        self.rb_window_maximized_screen_manual.setProperty(u"dataclass_property", u"manual_window_open_manual")
        self.rb_window_maximized_screen_manual.setProperty(u"dataclass_property_value", u"2")

        self.horizontalLayout_abertura_janela_manual.addWidget(self.rb_window_maximized_screen_manual)

        self.rb_window_maximized_screen_util_manual = QRadioButton(self.grp_window_open_manual)
        self.rb_window_maximized_screen_util_manual.setObjectName(u"rb_window_maximized_screen_util_manual")
        self.rb_window_maximized_screen_util_manual.setProperty(u"dataclass_property", u"manual_window_open_manual")
        self.rb_window_maximized_screen_util_manual.setProperty(u"dataclass_property_value", u"3")

        self.horizontalLayout_abertura_janela_manual.addWidget(self.rb_window_maximized_screen_util_manual)

        self.hs_window_open_manual = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_abertura_janela_manual.addItem(self.hs_window_open_manual)


        self.frm_janela_manual.setWidget(1, QFormLayout.ItemRole.FieldRole, self.grp_window_open_manual)

        self.lbl_open_projector_manual = QLabel(self.grp_window_manual)
        self.lbl_open_projector_manual.setObjectName(u"lbl_open_projector_manual")

        self.frm_janela_manual.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lbl_open_projector_manual)

        self.chk_open_projector_manual = QCheckBox(self.grp_window_manual)
        self.chk_open_projector_manual.setObjectName(u"chk_open_projector_manual")
        self.chk_open_projector_manual.setChecked(True)
        self.chk_open_projector_manual.setProperty(u"dataclass_property", u"manual_open_projector_manual")

        self.frm_janela_manual.setWidget(2, QFormLayout.ItemRole.FieldRole, self.chk_open_projector_manual)

        self.lbl_default_calibration_manual = QLabel(self.grp_window_manual)
        self.lbl_default_calibration_manual.setObjectName(u"lbl_default_calibration_manual")

        self.frm_janela_manual.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lbl_default_calibration_manual)

        self.chk_default_calibration_manual = QCheckBox(self.grp_window_manual)
        self.chk_default_calibration_manual.setObjectName(u"chk_default_calibration_manual")
        self.chk_default_calibration_manual.setChecked(False)
        self.chk_default_calibration_manual.setProperty(u"dataclass_property", u"manual_default_calibration_manual")

        self.frm_janela_manual.setWidget(3, QFormLayout.ItemRole.FieldRole, self.chk_default_calibration_manual)


        self.lay_calibracao_manual.addWidget(self.grp_window_manual)

        self.grp_calibration_points_manual = QGroupBox(self.tab_manual_calibration)
        self.grp_calibration_points_manual.setObjectName(u"grp_calibration_points_manual")
        self.frm_pontos_calibracao_manual = QFormLayout(self.grp_calibration_points_manual)
        self.frm_pontos_calibracao_manual.setObjectName(u"frm_pontos_calibracao_manual")
        self.frm_pontos_calibracao_manual.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.lbl_mirror_mode_manual = QLabel(self.grp_calibration_points_manual)
        self.lbl_mirror_mode_manual.setObjectName(u"lbl_mirror_mode_manual")

        self.frm_pontos_calibracao_manual.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lbl_mirror_mode_manual)

        self.chk_mirror_mode_manual = QCheckBox(self.grp_calibration_points_manual)
        self.chk_mirror_mode_manual.setObjectName(u"chk_mirror_mode_manual")
        self.chk_mirror_mode_manual.setChecked(True)
        self.chk_mirror_mode_manual.setProperty(u"dataclass_property", u"manual_mirror_mode_manual")

        self.frm_pontos_calibracao_manual.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chk_mirror_mode_manual)


        self.lay_calibracao_manual.addWidget(self.grp_calibration_points_manual)

        self.vs_calibration_manual = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lay_calibracao_manual.addItem(self.vs_calibration_manual)

        self.tab_widget.addTab(self.tab_manual_calibration, "")

        self.main_layout.addWidget(self.tab_widget)

        self.lay_button = QHBoxLayout()
        self.lay_button.setObjectName(u"lay_button")
        self.hs_button = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.lay_button.addItem(self.hs_button)

        self.pb_ok = QPushButton(CalibrationSettingView)
        self.pb_ok.setObjectName(u"pb_ok")
        icon = QIcon()
        icon.addFile(u":/icons/ui/buttons/okicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ok.setIcon(icon)

        self.lay_button.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(CalibrationSettingView)
        self.pb_cancel.setObjectName(u"pb_cancel")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ui/buttons/cancelicon", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_cancel.setIcon(icon1)

        self.lay_button.addWidget(self.pb_cancel)


        self.main_layout.addLayout(self.lay_button)


        self.retranslateUi(CalibrationSettingView)

        self.tab_widget.setCurrentIndex(0)
        self.cbx_clahe_grid.setCurrentIndex(1)
        self.cbx_dictionary_automatic.setCurrentIndex(2)
        self.pb_ok.setDefault(True)


        QMetaObject.connectSlotsByName(CalibrationSettingView)
    # setupUi

    def retranslateUi(self, CalibrationSettingView):
        CalibrationSettingView.setWindowTitle(QCoreApplication.translate("CalibrationSettingView", u"Configura\u00e7\u00e3o de Calibra\u00e7\u00e3o", None))
        self.lbl_model_desktop.setText(QCoreApplication.translate("CalibrationSettingView", u"Modelo MediaPipe Desktop:", None))
        self.grp_model_desktop.setTitle("")
        self.rb_model_desktop_lite.setText(QCoreApplication.translate("CalibrationSettingView", u"Lite", None))
        self.rb_model_desktop_full.setText(QCoreApplication.translate("CalibrationSettingView", u"Full", None))
        self.rb_model_desktop_heavy.setText(QCoreApplication.translate("CalibrationSettingView", u"Heavy", None))
        self.lbl_model_embedded.setText(QCoreApplication.translate("CalibrationSettingView", u"Modelo MediaPipe Embarcado:", None))
        self.grp_model_embedded.setTitle("")
        self.rb_model_embedded_lite.setText(QCoreApplication.translate("CalibrationSettingView", u"Lite", None))
        self.rb_model_embedded_full.setText(QCoreApplication.translate("CalibrationSettingView", u"Full", None))
        self.rb_model_embedded_heavy.setText(QCoreApplication.translate("CalibrationSettingView", u"Heavy", None))
        self.lbl_embedded_processing.setText(QCoreApplication.translate("CalibrationSettingView", u"Embarcado Processamento:", None))
        self.grp_embedded_processing.setTitle("")
        self.rb_embedded_processing_cpu.setText(QCoreApplication.translate("CalibrationSettingView", u"CPU", None))
        self.rb_embedded_processing_gpu.setText(QCoreApplication.translate("CalibrationSettingView", u"GPU", None))
        self.lbl_linux_processing.setText(QCoreApplication.translate("CalibrationSettingView", u"Linux Processamento:", None))
        self.grp_linux_processing.setTitle("")
        self.rb_linux_processing_cpu.setText(QCoreApplication.translate("CalibrationSettingView", u"CPU", None))
        self.rb_linux_processing_gpu.setText(QCoreApplication.translate("CalibrationSettingView", u"GPU", None))
        self.lbl_mac_processing.setText(QCoreApplication.translate("CalibrationSettingView", u"Mac Processamento:", None))
        self.groupBox_mac.setTitle("")
        self.rb_mac_processing_cpu.setText(QCoreApplication.translate("CalibrationSettingView", u"CPU", None))
        self.rb_mac_processing_gpu.setText(QCoreApplication.translate("CalibrationSettingView", u"GPU", None))
        self.lbl_windows_processing.setText(QCoreApplication.translate("CalibrationSettingView", u"Windows Processamento:", None))
        self.groupBox_windows.setTitle("")
        self.rb_windows_processing_cpu.setText(QCoreApplication.translate("CalibrationSettingView", u"CPU", None))
        self.rb_windows_processing_gpu.setText(QCoreApplication.translate("CalibrationSettingView", u"GPU", None))
        self.lbl_execution_mode.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo de Execu\u00e7\u00e3o:", None))
        self.groupBox_execution_mode.setTitle("")
        self.rb_execution_mode_video.setText(QCoreApplication.translate("CalibrationSettingView", u"V\u00eddeo", None))
        self.lbl_enable_mediapipe_pose.setText(QCoreApplication.translate("CalibrationSettingView", u"Habilitar MediaPipe Pose?", None))
        self.chk_enable_mediapipe_pose.setText("")
        self.lbl_detection_position.setText(QCoreApplication.translate("CalibrationSettingView", u"Detec\u00e7\u00e3o de Posi\u00e7\u00e3o (0\u20131):", None))
        self.lbl_detection_presence.setText(QCoreApplication.translate("CalibrationSettingView", u"Detec\u00e7\u00e3o de Presen\u00e7a (0\u20131):", None))
        self.lbl_detection_tracking.setText(QCoreApplication.translate("CalibrationSettingView", u"Detec\u00e7\u00e3o de Rastreio (0\u20131):", None))
        self.lbl_num_position.setText(QCoreApplication.translate("CalibrationSettingView", u"N\u00famero de posi\u00e7\u00f5es:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_mediapipe), QCoreApplication.translate("CalibrationSettingView", u"MediaPipe", None))
        self.lbl_embedded_capture.setText(QCoreApplication.translate("CalibrationSettingView", u"Embarcado Captura de V\u00eddeo:", None))
        self.grp_embedded_capture.setTitle("")
        self.rb_embedded_v4l2.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_V4L2", None))
        self.rb_embedded_gstreamer.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_GSTREAMER", None))
        self.lbl_linux_capture.setText(QCoreApplication.translate("CalibrationSettingView", u"Linux Captura de V\u00eddeo:", None))
        self.grp_linux_capture.setTitle("")
        self.rb_linux_v4l2.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_V4L2", None))
        self.rb_linux_gstreamer.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_GSTREAMER", None))
        self.lbl_mac_capture.setText(QCoreApplication.translate("CalibrationSettingView", u"Mac Captura de V\u00eddeo:", None))
        self.grp_mac_capture.setTitle("")
        self.rb_mac_avfoundation.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_AVFOUNDATION", None))
        self.rb_mac_any.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_ANY", None))
        self.lbl_windows_capture.setText(QCoreApplication.translate("CalibrationSettingView", u"Windows Captura de V\u00eddeo:", None))
        self.grp_windows_capture.setTitle("")
        self.rb_windows_dshow.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_DSHOW", None))
        self.rb_windows_msmf.setText(QCoreApplication.translate("CalibrationSettingView", u"CAP_MSMF", None))
        self.lbl_buffer_size.setText(QCoreApplication.translate("CalibrationSettingView", u"Tamanho do Buffer:", None))
        self.lbl_custom_camera.setText(QCoreApplication.translate("CalibrationSettingView", u"Customizar Informa\u00e7\u00f5es C\u00e2mera?", None))
        self.grp_camera_info.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Informa\u00e7\u00f5es da C\u00e2mera", None))
        self.lbl_ratio.setText(QCoreApplication.translate("CalibrationSettingView", u"Propor\u00e7\u00e3o:", None))
        self.lbl_width.setText(QCoreApplication.translate("CalibrationSettingView", u"Largura:", None))
        self.lbl_height.setText(QCoreApplication.translate("CalibrationSettingView", u"Altura:", None))
        self.lbl_fps.setText(QCoreApplication.translate("CalibrationSettingView", u"FPS:", None))
        self.grp_fps.setTitle("")
        self.rb_fps_30.setText(QCoreApplication.translate("CalibrationSettingView", u"30", None))
        self.rb_fps_60.setText(QCoreApplication.translate("CalibrationSettingView", u"60", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_opencv), QCoreApplication.translate("CalibrationSettingView", u"OpenCV", None))
        self.lbl_use_filter.setText(QCoreApplication.translate("CalibrationSettingView", u"Usar Filtros?", None))
        self.grp_filter.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Configura\u00e7\u00f5es de Filtros", None))
        self.lbl_average_smooth_frames.setText(QCoreApplication.translate("CalibrationSettingView", u"M\u00e9dia M\u00f3vel Smooth Frames:", None))
        self.lbl_clahe_clip.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Clahe Limite Clip:", None))
        self.lbl_clahe_grid.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Clahe Tamanho Grid:", None))
        self.cbx_clahe_grid.setItemText(0, QCoreApplication.translate("CalibrationSettingView", u"4:4", None))
        self.cbx_clahe_grid.setItemText(1, QCoreApplication.translate("CalibrationSettingView", u"8:8", None))
        self.cbx_clahe_grid.setItemText(2, QCoreApplication.translate("CalibrationSettingView", u"16:16", None))
        self.cbx_clahe_grid.setItemText(3, QCoreApplication.translate("CalibrationSettingView", u"32:32", None))

        self.lbl_clahe_lum_below.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Clahe Aplicar Quando Valor de Luminosidade Abaixo de:", None))
        self.lbl_gamma_factor.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Gamma Fator de Divis\u00e3o:", None))
        self.lbl_gamma_lum_above.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Gamma Aplicar Quando Valor de Luminosidade Acima de:", None))
        self.lbl_landmark_limit.setText(QCoreApplication.translate("CalibrationSettingView", u"Filtro Landmark Limite de Movimento:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_filter), QCoreApplication.translate("CalibrationSettingView", u"Filtros", None))
        self.lbl_enable_telemetry_panel.setText(QCoreApplication.translate("CalibrationSettingView", u"Habilitar painel telemetria?", None))
        self.chk_habilitar_painel_telemetria.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_telemetry), QCoreApplication.translate("CalibrationSettingView", u"Telemetria", None))
        self.grp_window_automatic.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Janela de Calibra\u00e7\u00e3o", None))
        self.lbl_window_position_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Posi\u00e7\u00e3o da abertura:", None))
        self.grp_window_position_automatic.setTitle("")
        self.rb_top_left_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Topo-Esquerda", None))
        self.lbl_window_open_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo de abertura:", None))
        self.grp_window_open_automatic.setTitle("")
        self.rb_window_full_screen_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Tela Cheia", None))
        self.rb_window_maximized_screen_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada)", None))
        self.rb_window_maximized_screen_util_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada \u00c1rea \u00datil)", None))
        self.lbl_open_projector_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Abrir diretamente no projetor?", None))
        self.chk_open_projector_automatic.setText("")
        self.lbl_default_calibration_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o padr\u00e3o?", None))
        self.chk_default_calibration_automatic.setText("")
        self.grp_calibration_points_automatic.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Leitura Pontos de Calibra\u00e7\u00e3o", None))
        self.lbl_mirror_mode_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo espelho?", None))
        self.chk_mirror_mode_automatic.setText("")
        self.grp_automatic_marker.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Marcador", None))
        self.lbl_num_columns_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Quantidade de colunas:", None))
        self.lbl_num_rows_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Quantidade de linhas:", None))
        self.lbl_multiplier_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Multiplicador:", None))
        self.lbl_dictionary_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Dicion\u00e1rio:", None))
        self.cbx_dictionary_automatic.setItemText(0, QCoreApplication.translate("CalibrationSettingView", u"DICT_4X4_50", None))
        self.cbx_dictionary_automatic.setItemText(1, QCoreApplication.translate("CalibrationSettingView", u"DICT_4X4_100", None))
        self.cbx_dictionary_automatic.setItemText(2, QCoreApplication.translate("CalibrationSettingView", u"DICT_4X4_250", None))
        self.cbx_dictionary_automatic.setItemText(3, QCoreApplication.translate("CalibrationSettingView", u"DICT_4X4_1000", None))
        self.cbx_dictionary_automatic.setItemText(4, QCoreApplication.translate("CalibrationSettingView", u"DICT_5X5_50", None))
        self.cbx_dictionary_automatic.setItemText(5, QCoreApplication.translate("CalibrationSettingView", u"DICT_5X5_100", None))
        self.cbx_dictionary_automatic.setItemText(6, QCoreApplication.translate("CalibrationSettingView", u"DICT_5X5_250", None))
        self.cbx_dictionary_automatic.setItemText(7, QCoreApplication.translate("CalibrationSettingView", u"DICT_5X5_1000", None))
        self.cbx_dictionary_automatic.setItemText(8, QCoreApplication.translate("CalibrationSettingView", u"DICT_6X6_50", None))
        self.cbx_dictionary_automatic.setItemText(9, QCoreApplication.translate("CalibrationSettingView", u"DICT_6X6_100", None))
        self.cbx_dictionary_automatic.setItemText(10, QCoreApplication.translate("CalibrationSettingView", u"DICT_6X6_250", None))
        self.cbx_dictionary_automatic.setItemText(11, QCoreApplication.translate("CalibrationSettingView", u"DICT_6X6_1000", None))
        self.cbx_dictionary_automatic.setItemText(12, QCoreApplication.translate("CalibrationSettingView", u"DICT_7X7_50", None))
        self.cbx_dictionary_automatic.setItemText(13, QCoreApplication.translate("CalibrationSettingView", u"DICT_7X7_100", None))
        self.cbx_dictionary_automatic.setItemText(14, QCoreApplication.translate("CalibrationSettingView", u"DICT_7X7_250", None))
        self.cbx_dictionary_automatic.setItemText(15, QCoreApplication.translate("CalibrationSettingView", u"DICT_7X7_1000", None))

        self.lbl_width_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Largura em pixels:", None))
        self.lbl_height_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Altura em pixels:", None))
        self.lbl_margin_automatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Tamanho da margem em pixels:", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_automatic_calibration), QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o Autom\u00e1tica", None))
        self.grp_window_semiautomatic.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Janela de Calibra\u00e7\u00e3o", None))
        self.lbl_window_position_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Posi\u00e7\u00e3o da abertura:", None))
        self.grp_window_position_semiautomatic.setTitle("")
        self.rb_top_left_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Topo-Esquerda", None))
        self.lbl_window_open_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo de abertura:", None))
        self.grp_window_open_semiautomatic.setTitle("")
        self.rb_window_full_screen_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Tela Cheia", None))
        self.rb_window_maximized_screen_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada)", None))
        self.rb_window_maximized_screen_util_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada \u00c1rea \u00datil)", None))
        self.lbl_open_projector_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Abrir diretamente no projetor?", None))
        self.chk_open_projector_semiautomatic.setText("")
        self.lbl_default_calibration_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o padr\u00e3o?", None))
        self.chk_default_calibration_semiautomatic.setText("")
        self.grp_calibration_points_semiautomatic.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Leitura Pontos de Calibra\u00e7\u00e3o", None))
        self.lbl_mirror_mode_semiautomatic.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo espelho?", None))
        self.chk_mirror_mode_semiautomatic.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_semiautomatic_calibration), QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o Semi-Autom\u00e1tica", None))
        self.grp_window_manual.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Janela de Calibra\u00e7\u00e3o", None))
        self.lbl_window_position_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Posi\u00e7\u00e3o da abertura:", None))
        self.grp_window_position_manual.setTitle("")
        self.rb_top_left_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Topo-Esquerda", None))
        self.lbl_window_open_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo de abertura:", None))
        self.grp_window_open_manual.setTitle("")
        self.rb_window_full_screen_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Tela Cheia", None))
        self.rb_window_maximized_screen_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada)", None))
        self.rb_window_maximized_screen_util_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo Janela (Maximizada \u00c1rea \u00datil)", None))
        self.lbl_open_projector_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Abrir diretamente no projetor?", None))
        self.chk_open_projector_manual.setText("")
        self.lbl_default_calibration_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o padr\u00e3o?", None))
        self.chk_default_calibration_manual.setText("")
        self.grp_calibration_points_manual.setTitle(QCoreApplication.translate("CalibrationSettingView", u"Leitura Pontos de Calibra\u00e7\u00e3o", None))
        self.lbl_mirror_mode_manual.setText(QCoreApplication.translate("CalibrationSettingView", u"Modo espelho?", None))
        self.chk_mirror_mode_manual.setText("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_manual_calibration), QCoreApplication.translate("CalibrationSettingView", u"Calibra\u00e7\u00e3o Manual", None))
#if QT_CONFIG(tooltip)
        self.pb_ok.setToolTip(QCoreApplication.translate("CalibrationSettingView", u"Gravar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ok.setText(QCoreApplication.translate("CalibrationSettingView", u"OK", None))
#if QT_CONFIG(tooltip)
        self.pb_cancel.setToolTip(QCoreApplication.translate("CalibrationSettingView", u"Cancelar opera\u00e7\u00e3o corrente", None))
#endif // QT_CONFIG(tooltip)
        self.pb_cancel.setText(QCoreApplication.translate("CalibrationSettingView", u"Cancelar", None))
    # retranslateUi

