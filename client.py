# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 737)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 611, 411))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.user_label = QtWidgets.QLabel(self.widget)
        self.user_label.setObjectName("user_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.user_label)
        self.user = QtWidgets.QLabel(self.widget)
        self.user.setObjectName("user")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.user)
        self.query_path_label = QtWidgets.QLabel(self.widget)
        self.query_path_label.setObjectName("query_path_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.query_path_label)
        self.query_path_button = QtWidgets.QPushButton(self.widget)
        self.query_path_button.setObjectName("query_path_button")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.query_path_button)
        self.query_path_browser = QtWidgets.QTextBrowser(self.widget)
        self.query_path_browser.setObjectName("query_path_browser")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.query_path_browser)
        self.choose_path_label = QtWidgets.QLabel(self.widget)
        self.choose_path_label.setObjectName("choose_path_label")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.choose_path_label)
        self.choose_path_layout = QtWidgets.QFormLayout()
        self.choose_path_layout.setObjectName("choose_path_layout")
        self.formLayout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.choose_path_layout)
        self.remaining_bandwidth_label = QtWidgets.QLabel(self.widget)
        self.remaining_bandwidth_label.setObjectName("remaining_bandwidth_label")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.remaining_bandwidth_label)
        self.max_bandwidth_label = QtWidgets.QLabel(self.widget)
        self.max_bandwidth_label.setObjectName("max_bandwidth_label")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.max_bandwidth_label)
        self.limit_bw_layout = QtWidgets.QHBoxLayout()
        self.limit_bw_layout.setObjectName("limit_bw_layout")
        self.formLayout.setLayout(13, QtWidgets.QFormLayout.FieldRole, self.limit_bw_layout)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dst_comboBox = QtWidgets.QComboBox(self.widget)
        self.dst_comboBox.setObjectName("dst_comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dst_comboBox)
        self.query_bw_layout = QtWidgets.QHBoxLayout()
        self.query_bw_layout.setObjectName("query_bw_layout")
        self.formLayout.setLayout(12, QtWidgets.QFormLayout.FieldRole, self.query_bw_layout)
        self.user_label.raise_()
        self.user.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client GUI"))
        self.user_label.setText(_translate("MainWindow", "Current user:"))
        self.user.setText(_translate("MainWindow", "None"))
        self.query_path_label.setText(_translate("MainWindow", "Query Path"))
        self.query_path_button.setText(_translate("MainWindow", "Query !"))
        self.choose_path_label.setText(_translate("MainWindow", "Choose Path"))
        self.remaining_bandwidth_label.setText(_translate("MainWindow", "Remaining bandwidth"))
        self.max_bandwidth_label.setText(_translate("MainWindow", "Max bandwidth"))
        self.label.setText(_translate("MainWindow", "Destination host"))


