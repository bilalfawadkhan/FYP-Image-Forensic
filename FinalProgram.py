# -*- coding: utf-8 -*-
import os

import matplotlib as plt
import exifread, cv2

plt.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, QObject, pyqtSignal, QThread, QRunnable, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem

import ChangeofLaplacian as cl

import tifffile as tf


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)


# self.progress.emit(i + 1)
# self.finished.emit()





class UiMainWindow(object):
	def __init__(self):
		self.logoLabel = None

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		flag = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
		MainWindow.setWindowFlags(flag)
		MainWindow.setFixedSize(1272, 769)
		MainWindow.setStyleSheet("#MainWindow{border :200px solid rgb(36, 34, 34);}")
		MainWindow.setIconSize(QtCore.QSize(27, 27))
		MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.mainwind = QtWidgets.QGroupBox(self.centralwidget)
		self.mainwind.setGeometry(QtCore.QRect(0, 0, 1271, 761))
		self.mainwind.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.mainwind.setStyleSheet("#mainwind{background-Color :#121212;\n"
									"color : rgb(255, 255, 255);\n"
									"border-radius : 20px;\n"
									"}")
		self.mainwind.setTitle("")
		self.mainwind.setObjectName("mainwind")

		self.toolbar = QtWidgets.QGroupBox(self.mainwind)
		self.toolbar.setGeometry(QtCore.QRect(0, 0, 1271, 51))
		self.toolbar.setStyleSheet("#toolbar{border-radius: 20px;}")
		self.toolbar.setTitle("")
		self.toolbar.setObjectName("toolbar")
		self.minButton = QtWidgets.QPushButton(self.toolbar)
		self.minButton.setGeometry(QtCore.QRect(1079, 0, 61, 41))
		self.minButton.setStyleSheet(
			"#minButton{background-Color : #121212;;border:0px solid black} #minButton:hover{background-Color : #57A773;}")
		self.minButton.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/line.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.minButton.setIcon(icon)
		self.minButton.setIconSize(QtCore.QSize(25, 25))
		self.minButton.setObjectName("minButton")
		self.minButton.clicked.connect(lambda: MainWindow.showMinimized())
		self.closeButton = QtWidgets.QPushButton(self.toolbar)
		self.closeButton.setGeometry(QtCore.QRect(1201, 0, 71, 41))
		self.closeButton.setStyleSheet(
			"#closeButton{border-radius: 20px;background-Color : #121212;} #closeButton:hover{background-Color :#A71D31;border-radius: 20px}")
		self.closeButton.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/cross 1.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.closeButton.setIcon(icon1)
		self.closeButton.setIconSize(QtCore.QSize(25, 25))
		self.closeButton.setObjectName("closeButton")
		self.closeButton.clicked.connect(lambda: MainWindow.close())
		self.maximButton = QtWidgets.QPushButton(self.toolbar)
		self.maximButton.setGeometry(QtCore.QRect(1140, 0, 61, 41))
		self.maximButton.setStyleSheet(
			"#maximButton{background-Color :#121212;;border:0px solid black} #maximButton:hover{background-Color :#F4A259}")
		self.maximButton.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/Square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.maximButton.setIcon(icon2)
		self.maximButton.setIconSize(QtCore.QSize(25, 25))
		self.maximButton.setObjectName("maximButton")
		self.botBox = QtWidgets.QGroupBox(self.mainwind)
		self.botBox.setGeometry(QtCore.QRect(220, 550, 901, 141))
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
		self.botBox.setPalette(palette)
		self.botBox.setStyleSheet("#botBox{background-Color :  #1f2327;;\n"
								  "border-radius : 20px;\n"
								  "border : 2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
								  "color:rgb(255,255,255);}\n"
								  "")
		self.botBox.setTitle("")
		self.botBox.setObjectName("botBox")
		self.commwinlabel = QtWidgets.QLabel(self.botBox)
		self.commwinlabel.setGeometry(QtCore.QRect(20, 10, 121, 16))
		self.commwinlabel.setStyleSheet("#commwinlabel{border: 0 solid;\n"
										"color:rgb(255,255,255);\n"
										"} \n"
										"")
		self.commwinlabel.setObjectName("commwinlabel")
		self.commwinlabel.setText("Command Window")
		self.commwinlabel
		self.commwin = QtWidgets.QTextEdit(self.botBox)
		self.commwin.setGeometry(QtCore.QRect(20, 26, 611, 101))
		self.commwin.setMouseTracking(False)
		self.commwin.setStyleSheet("background-Color :  #1f2327;\n"
								   "color:rgb(255,255,255); border: 0px")
		self.commwin.setReadOnly(True)
		self.commwin.setObjectName("commwin")
		self.midBox = QtWidgets.QGroupBox(self.mainwind)
		self.midBox.setGeometry(QtCore.QRect(220, 140, 901, 391))
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
		brush = QtGui.QBrush(QtGui.QColor(0, 255, 127))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
		brush = QtGui.QBrush(QtGui.QColor(31, 35, 39))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
		brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
		brush.setStyle(QtCore.Qt.NoBrush)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
		self.midBox.setPalette(palette)
		self.midBox.setStyleSheet("#midBox{\n"
								  "border-radius : 20px;\n"
								  "color:rgb(255,255,255);\n"
								  " QFrame:Raised;\n"
								  "border : 2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
								  "\n"
								  "background-Color :  #1f2327;\n"
								  "}\n"
								  "")
		self.midBox.setTitle("")
		self.midBox.setObjectName("midBox")
		self.mainImage = QtWidgets.QLabel(self.midBox)
		self.mainImage.setGeometry(QtCore.QRect(250, 30, 381, 271))
		self.mainImage.setText("")
		self.mainImage.setPixmap(QtGui.QPixmap("UI Resources/uploadimg.png"))
		self.mainImage.setScaledContents(True)
		self.mainImage.setObjectName("mainImage")
		self.uploadhintGroup = QtWidgets.QGroupBox(self.midBox)
		self.uploadhintGroup.setGeometry(QtCore.QRect(250, 340, 401, 41))
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.uploadhintGroup.setFont(font)
		self.uploadhintGroup.setStyleSheet(
			"#uploadhintGroup{background-Color :qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
			"color : rgb(255, 255, 255);\n"
			"border-radius : 20px;}")
		self.uploadhintGroup.setTitle("")
		self.uploadhintGroup.setObjectName("uploadhintGroup")
		self.label_2 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_2.setGeometry(QtCore.QRect(130, 10, 241, 21))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(10)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.label_2.setFont(font)
		self.label_2.setStyleSheet("color:rgb(255,255,255);")
		self.label_2.setText("Please Upload the Image First ")
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_3.setGeometry(QtCore.QRect(90, 10, 31, 24))
		self.label_3.setText("")
		self.label_3.setPixmap(QtGui.QPixmap("UI Resources/plus Icon/plus 1.png"))
		self.label_3.setScaledContents(True)
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_4.setGeometry(QtCore.QRect(30, 10, 51, 21))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(10)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setStyleSheet("color:rgb(255,255,255);\n"
								   "")
		self.label_4.setText("Press")
		self.label_4.setObjectName("label_4")
		self.navbarleft = QtWidgets.QGroupBox(self.mainwind)
		self.navbarleft.setGeometry(QtCore.QRect(0, 0, 181, 761))
		self.navbarleft.setStyleSheet("#navbarleft{color:rgb(255,255,255);\n"
									  "border-radius: 20px;\n"
									  "border : 3px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));}")
		self.navbarleft.setTitle("")
		self.navbarleft.setObjectName("navbarleft")
		self.projectBox = QtWidgets.QGroupBox(self.navbarleft)
		self.projectBox.setGeometry(QtCore.QRect(10, 300, 161, 441))
		self.projectBox.setStyleSheet("#projectBox{background-Color : #1f2327;\n"
									  "color : rgb(255, 255, 255);\n"
									  "border-radius : 10px;\n"
									  "border: 0px solid ;\n"
									  "}")
		self.projectBox.setTitle("")
		self.projectBox.setObjectName("projectBox")
		self.projectDirList = QtWidgets.QListWidget(self.projectBox)
		self.projectDirList.setGeometry(QtCore.QRect(10, 10, 141, 381))
		self.projectDirList.setWhatsThis("")

		self.projectDirList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.projectDirList.setItemAlignment(QtCore.Qt.AlignHCenter)
		self.projectDirList.setObjectName("projectDirList")
		self.projectDirList.setStyleSheet("#projectDirList{background-color : #1f2327;\n"
										  "color:rgb(255,255,255);\n"
										  "border: 0px}")
		self.projectDirList.currentItemChanged.connect(self.selectImageonChange)
		self.deleteImgButton = QtWidgets.QPushButton(self.projectBox)
		self.deleteImgButton.setGeometry(QtCore.QRect(120, 400, 31, 31))
		self.deleteImgButton.setStyleSheet('#deleteImgButton{background-color : #1f2327 ;border-radius : 0 px;}')
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap("UI Resources/Trash Can/trashcan1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.deleteImgButton.setIcon(icon3)
		self.deleteImgButton.setIconSize(QtCore.QSize(27, 27))
		self.deleteImgButton.setObjectName("deleteImgButton")
		self.deleteImgButton.clicked.connect(self.deleteimagefromDir)
		self.logolabel = QtWidgets.QLabel(self.navbarleft)
		self.logolabel.setGeometry(QtCore.QRect(10, 0, 161, 101))
		self.logolabel.setStyleSheet("#logolabe{border-radius: 20px}")
		self.logolabel.setText("")
		self.logolabel.setPixmap(QtGui.QPixmap("UI Resources/logo/logo.png"))
		self.logolabel.setScaledContents(True)
		self.logolabel.setObjectName("logolabel")
		self.uploadButton = QtWidgets.QPushButton(self.navbarleft)
		self.uploadButton.setGeometry(QtCore.QRect(60, 100, 61, 61))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.uploadButton.setFont(font)
		self.uploadButton.setAutoFillBackground(False)
		self.uploadButton.setStyleSheet(
			"#uploadButton{border-radius: 20px;border:2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255)); background-color :#121212};\n"
			"#uploadButton:hover{background-color : qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255))}")
		self.uploadButton.setText("")
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap("UI Resources/plus Icon/plus 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.uploadButton.setIcon(icon4)
		self.uploadButton.setIconSize(QtCore.QSize(40, 40))
		self.uploadButton.setObjectName("uploadButton")
		self.uploadButton.clicked.connect(self.dialogOpen)
		self.mthistgroup = QtWidgets.QGroupBox(self.navbarleft)
		self.mthistgroup.setGeometry(QtCore.QRect(19, 240, 141, 51))
		self.mthistgroup.setStyleSheet("#mthistgroup{border-radius: 20px;\n"
									   "border:2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
									   "\n"
									   "}")
		self.mthistgroup.setTitle("")
		self.mthistgroup.setObjectName("mthistgroup")
		self.metaDataButton = QtWidgets.QPushButton(self.mthistgroup)
		self.metaDataButton.setGeometry(QtCore.QRect(0, 0, 61, 51))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.metaDataButton.setFont(font)
		self.metaDataButton.setStyleSheet("#metaDataButton{border-radius: 20px;\n"
										  "color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));;}\n"
										  "#metaDataButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
										  "color: rgb(255,255,255)\n"
										  "}")
		self.metaDataButton.setText("MT")
		self.metaDataButton.setObjectName("metaDataButton")
		self.metaDataButton.clicked.connect(self.showMeta)
		self.histogramButton = QtWidgets.QPushButton(self.mthistgroup)
		self.histogramButton.setGeometry(QtCore.QRect(80, 0, 61, 51))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.histogramButton.setFont(font)
		self.histogramButton.setStyleSheet("#histogramButton{border-radius: 20px;\n"
										   "color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));;}\n"
										   "#histogramButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
										   "color: rgb(255,255,255)\n"
										   "}")
		self.histogramButton.setText("HIST")
		self.histogramButton.setObjectName("histogramButton")
		self.histogramButton.clicked.connect(self.showHist)
		self.playstopgroup = QtWidgets.QGroupBox(self.navbarleft)
		self.playstopgroup.setGeometry(QtCore.QRect(20, 170, 141, 61))
		self.playstopgroup.setStyleSheet("#playstopgroup{border-radius: 20px;\n"
										 "border:2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
										 "}")
		self.playstopgroup.setTitle("")
		self.playstopgroup.setObjectName("playstopgroup")
		self.runbutton = QtWidgets.QPushButton(self.playstopgroup)
		self.runbutton.setGeometry(QtCore.QRect(0, 0, 61, 61))
		self.runbutton.setStyleSheet("#runbutton{border-radius: 20px;}\n"
									 "\n"
									 "#runbutton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
									 "border-radius: 20px;}\n"
									 "")
		self.runbutton.setText("")
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap("UI Resources/runicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.runbutton.setIcon(icon5)
		self.runbutton.setIconSize(QtCore.QSize(35, 35))
		self.runbutton.setObjectName("runbutton")
		self.runbutton.clicked.connect(self.runForensics)
		self.stopbutton = QtWidgets.QPushButton(self.playstopgroup)
		self.stopbutton.setGeometry(QtCore.QRect(80, 0, 61, 61))
		self.stopbutton.setStyleSheet("#stopbutton{border-radius: 20px;}\n"
									  "\n"
									  "#stopbutton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
									  "border-radius: 20px;}\n"
									  "")
		self.stopbutton.setText("")
		icon6 = QtGui.QIcon()
		icon6.addPixmap(QtGui.QPixmap("UI Resources/stopicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.stopbutton.setIcon(icon6)
		self.stopbutton.setIconSize(QtCore.QSize(35, 35))
		self.stopbutton.setObjectName("stopbutton")
		self.logolabel.raise_()
		self.projectBox.raise_()
		self.mthistgroup.raise_()
		self.uploadButton.raise_()
		self.playstopgroup.raise_()
		self.toolbar.raise_()
		self.botBox.raise_()
		self.midBox.raise_()
		self.navbarleft.raise_()
		MainWindow.setCentralWidget(self.centralwidget)

		# self.menubar = QtWidgets.QMenuBar(MainWindow)
		# self.menubar.setGeometry(QtCore.QRect(0, 0, 1272, 26))
		# self.menubar.setObjectName("menubar")
		# MainWindow.setMenuBar(self.menubar)
		# self.statusbar = QtWidgets.QStatusBar(MainWindow)
		# self.statusbar.setObjectName("statusbar")
		# MainWindow.setStatusBar(self.statusbar)

		## Changing the Tab order ##
		# self.retranslateUi(MainWindow)
		# QtCore.QMetaObject.connectSlotsByName(MainWindow)
		# MainWindow.setTabOrder(self.minButton, self.maximButton)
		# MainWindow.setTabOrder(self.maximButton, self.closeButton)
		# MainWindow.setTabOrder(self.closeButton, self.metaDataButton)
		# MainWindow.setTabOrder(self.metaDataButton, self.histogramButton)
		# MainWindow.setTabOrder(self.histogramButton, self.uploadButton)
		# MainWindow.setTabOrder(self.uploadButton, self.projectDirList)
		# MainWindow.setTabOrder(self.projectDirList, self.deleteImgButton)

		## Side Group box appearing with Meta Data ##
		self.rSideGroup = QtWidgets.QGroupBox(self.mainwind)
		self.rSideGroup.setGeometry(QtCore.QRect(1241, 80, 0, 501))
		self.rSideGroup.setStyleSheet("#rSideGroup{\n"
									  "border-radius : 20px;\n"
									  "color:rgb(255,255,255);\n"
									  "border : 2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
									  "background-Color :  #121212;}")
		self.rSideGroup.setTitle("")
		self.rSideGroup.setObjectName("rSideGroup")
		self.rsideGroupCrossB = QtWidgets.QPushButton(self.rSideGroup)
		self.rsideGroupCrossB.setGeometry(QtCore.QRect(280, 10, 81, 51))
		self.rsideGroupCrossB.setStyleSheet("border : 0px;")
		self.rsideGroupCrossB.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/cross 2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.rsideGroupCrossB.setIcon(icon)
		self.rsideGroupCrossB.setIconSize(QtCore.QSize(30, 30))
		self.rsideGroupCrossB.setObjectName("rsideGroupCrossB")
		self.rsideGroupCrossB.clicked.connect(self.hideRGroupBox)
		self.rSideGroupText = QtWidgets.QLabel(self.rSideGroup)
		self.rSideGroupText.setGeometry(QtCore.QRect(50, 10, 141, 41))
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(False)
		font.setWeight(50)
		self.rSideGroupText.setFont(font)
		self.rSideGroupText.setStyleSheet("color :rgb(255, 255, 255)")
		self.rSideGroupText.setObjectName("rSideGroupText")
		self.innerGroupBox = QtWidgets.QGroupBox(self.rSideGroup)
		self.innerGroupBox.setGeometry(QtCore.QRect(10, 60, 351, 431))
		self.innerGroupBox.setStyleSheet("#innerGroupBox{border:0px}")
		self.innerGroupBox.setTitle("")
		self.innerGroupBox.setObjectName("innerGroupBox")
		self.block1 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block1.setGeometry(QtCore.QRect(20, 50, 146, 100))
		self.block1.setStyleSheet("background-Color :#1f2327;;\n"
								  "border-radius : 20px;\n"
								  "")
		self.block1.setTitle("")
		self.block1.setObjectName("block1")
		self.widget = QtWidgets.QWidget(self.block1)
		self.widget.setGeometry(QtCore.QRect(10, 20, 16, 60))
		self.widget.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.352632, y1:0.363636, x2:1, y2:1, stop:0 rgba(104, 187, 89, 255), stop:1 rgba(30, 86, 49, 255));\n"
			"border-radius : 5px;\n"
			"")
		self.widget.setObjectName("widget")
		self.block1Title = QtWidgets.QLabel(self.block1)
		self.block1Title.setGeometry(QtCore.QRect(50, 0, 61, 31))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(False)
		font.setWeight(50)
		self.block1Title.setFont(font)
		self.block1Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block1Title.setText("Height")
		self.block1Title.setObjectName("block1Title")
		self.block1value = QtWidgets.QLabel(self.block1)
		self.block1value.setGeometry(QtCore.QRect(50, 40, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block1value.setFont(font)
		self.block1value.setStyleSheet("color : rgb(255, 255, 255)")
		self.block1value.setText("Nill")
		self.block1value.setObjectName("block1value")
		self.block2 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block2.setGeometry(QtCore.QRect(190, 50, 146, 100))
		self.block2.setStyleSheet("Background-color :#1f2327;;\n"
								  "border-radius : 20px;\n"
								  "")
		self.block2.setTitle("")
		self.block2.setObjectName("block2")
		self.widget_2 = QtWidgets.QWidget(self.block2)
		self.widget_2.setGeometry(QtCore.QRect(10, 20, 16, 60))
		self.widget_2.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.052356, y1:0.0568182, x2:0.979, y2:1, stop:0 rgba(163, 223, 232, 255), stop:1 rgba(24, 197, 202, 255));\n"
			"border-radius : 5px;\n"
			"")
		self.widget_2.setObjectName("widget_2")
		self.block2Title = QtWidgets.QLabel(self.block2)
		self.block2Title.setGeometry(QtCore.QRect(50, 10, 55, 16))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block2Title.setFont(font)
		self.block2Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block2Title.setText("Width")
		self.block2Title.setObjectName("block2Title")
		self.block2value = QtWidgets.QLabel(self.block2)
		self.block2value.setGeometry(QtCore.QRect(40, 40, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block2value.setFont(font)
		self.block2value.setStyleSheet("color : rgb(255, 255, 255)")
		self.block2value.setText("Nill")
		self.block2value.setObjectName("block2value")
		self.block4 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block4.setGeometry(QtCore.QRect(190, 169, 146, 100))
		self.block4.setStyleSheet("Background-color :#1f2327;;\n"
								  "border-radius : 20px;\n"
								  "")
		self.block4.setTitle("")
		self.block4.setObjectName("block4")
		self.widget_10 = QtWidgets.QWidget(self.block4)
		self.widget_10.setGeometry(QtCore.QRect(10, 20, 16, 60))
		self.widget_10.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.242316, y1:0.244, x2:1, y2:1, stop:0 rgba(231, 102, 255, 255), stop:0.968421 rgba(159, 73, 158, 255), stop:0.989474 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
			"border-radius : 5px;\n"
			"")
		self.widget_10.setObjectName("widget_10")
		self.block4value = QtWidgets.QLabel(self.block4)
		self.block4value.setGeometry(QtCore.QRect(40, 40, 81, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block4value.setFont(font)
		self.block4value.setStyleSheet("color : rgb(255, 255, 255);")
		self.block4value.setObjectName("block4value")
		self.block4Title = QtWidgets.QLabel(self.block4)
		self.block4Title.setGeometry(QtCore.QRect(50, 10, 51, 16))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block4Title.setFont(font)
		self.block4Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block4Title.setText("Make")
		self.block4Title.setObjectName("block4Title")
		self.block3 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block3.setGeometry(QtCore.QRect(20, 169, 146, 100))
		self.block3.setStyleSheet("Background-color :#1f2327;;\n"
								  "border-radius : 20px;\n"
								  "")
		self.block3.setTitle("")
		self.block3.setObjectName("block3")
		self.widget_4 = QtWidgets.QWidget(self.block3)
		self.widget_4.setGeometry(QtCore.QRect(10, 20, 16, 60))
		self.widget_4.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.397906, y1:0.364, x2:1, y2:1, stop:0 rgba(223, 176, 115, 255), stop:1 rgba(236, 159, 43, 255));\n"
			"border-radius : 5px;\n"
			"")
		self.widget_4.setObjectName("widget_4")
		self.block3Title = QtWidgets.QLabel(self.block3)
		self.block3Title.setGeometry(QtCore.QRect(60, 10, 41, 16))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block3Title.setFont(font)
		self.block3Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block3Title.setText("Size")
		self.block3Title.setObjectName("block3Title")
		self.block3value = QtWidgets.QLabel(self.block3)
		self.block3value.setGeometry(QtCore.QRect(50, 40, 61, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block3value.setFont(font)
		self.block3value.setStyleSheet("color : rgb(255, 255, 255)")
		self.block3value.setText("Nill")
		self.block3value.setObjectName("block3value")
		self.block5 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block5.setGeometry(QtCore.QRect(14, 290, 326, 101))
		self.block5.setStyleSheet("Background-color :#1f2327;;\n"
								  "border-radius : 20px;\n"
								  "")
		self.block5.setTitle("")
		self.block5.setObjectName("block5")
		self.widget_3 = QtWidgets.QWidget(self.block5)
		self.widget_3.setGeometry(QtCore.QRect(21, 20, 16, 60))
		self.widget_3.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.395, y1:0.335227, x2:1, y2:1, stop:0 rgba(230, 119, 119, 255), stop:1 rgba(232, 11, 11, 255));\n"
			"border-radius : 5px;\n"
			"")
		self.widget_3.setObjectName("widget_3")
		self.block5Title = QtWidgets.QLabel(self.block5)
		self.block5Title.setGeometry(QtCore.QRect(110, 4, 131, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block5Title.setFont(font)
		self.block5Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block5Title.setText("Creation Date")
		self.block5Title.setObjectName("block5Title")
		self.block5value = QtWidgets.QLabel(self.block5)
		self.block5value.setGeometry(QtCore.QRect(60, 38, 251, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block5value.setFont(font)
		self.block5value.setStyleSheet("color : rgb(255, 255, 255);")
		self.block5value.setText("Nill")
		self.block5value.setObjectName("block5value")
		self.metatwobutton = QtWidgets.QPushButton(self.innerGroupBox)
		self.metatwobutton.setGeometry(QtCore.QRect(180, 400, 41, 28))
		self.metatwobutton.setStyleSheet("#metatwobutton{border-radius : 20px;\n"
										 "color:rgb(255,255,255);\n"
										 "border : 2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
										 "background-Color :  #121212;}\n"
										 "#metatwobutton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));}")
		self.metatwobutton.setObjectName("metatwobutton")
		self.metatwobutton.setText('2')
		self.metatwobutton.clicked.connect(self.setMetaData2)
		self.metaonebutton = QtWidgets.QPushButton(self.innerGroupBox)
		self.metaonebutton.setGeometry(QtCore.QRect(110, 400, 41, 28))
		self.metaonebutton.setStyleSheet("#metaonebutton{border-radius : 20px;\n"
										 "color:rgb(255,255,255);\n"
										 "border : 2px solid qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));\n"
										 "background-Color :  #121212;}\n"
										 "#metaonebutton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(245, 75, 100, 255), stop:1 rgba(247, 131, 97, 255));}")
		self.metaonebutton.setObjectName("metaonebutton")
		self.metaonebutton.setText('1')
		self.verticalLayoutWidget = QtWidgets.QWidget(self.rSideGroup)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 89, 321, 341))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.verticalLayoutWidget.hide()
		self.innerGroupBox.raise_()
		self.rsideGroupCrossB.raise_()
		self.rSideGroupText.raise_()
		self.mainimagepath = ""

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

	# This method hides the right side Group Box with Animation
	def hideRGroupBox(self):
		formerGeometry = QtCore.QRect(
			self.rSideGroup.geometry())  # storing previous geometry in order to be able to restore it later
		self.hideAnimation = QtCore.QPropertyAnimation(self.rSideGroup, b'geometry')
		self.hideAnimation.setDuration(500)  # choose the value that fits you
		self.hideAnimation.setEasingCurve(QEasingCurve.InOutCubic)
		self.hideAnimation.setStartValue(formerGeometry)
		# computing final geometry
		endTopLeftCorner = QtCore.QPoint(self.rSideGroup.pos() + QtCore.QPoint(self.rSideGroup.width(), 0))
		finalGeometry = QtCore.QRect(endTopLeftCorner, QtCore.QSize(0, self.rSideGroup.height()))
		self.hideAnimation.setEndValue(finalGeometry)
		self.hideAnimation.start()
		self.maximizeMidWIn()

	# This method Shows the right side Group Box with Animation
	def showRGroupBox(self):
		self.showAnimation = QtCore.QPropertyAnimation(self.rSideGroup, b'geometry')
		self.showAnimation.setDuration(500)  # choose the value that fits you
		self.showAnimation.setEasingCurve(QEasingCurve.InOutCubic)
		self.showAnimation.setStartValue(self.rSideGroup.geometry())
		# computing final geometry
		self.showAnimation.setEndValue(QtCore.QRect(900, 80, 361, 501))
		self.showAnimation.start()
		self.minimizeMidWIn()

	## Resizing of midbox and botbox ##################
	def minimizeMidWIn(self):
		# shrinking Mid box with Animation
		shrunkWidth = 660
		point = QtCore.QPoint(self.midBox.pos())
		height = self.midBox.geometry().height()
		width = self.midBox.geometry().width()
		self.animation = QPropertyAnimation(self.midBox, b'geometry')
		self.animation.setEasingCurve(QEasingCurve.InOutCubic)
		self.animation.setDuration(500)
		self.animation.setStartValue(QRect(point, QtCore.QSize(width, height)))
		self.animation.setEndValue(QRect(point, QtCore.QSize(shrunkWidth, height)))
		self.animation.start()
		# Shrinking botBox with Animation
		point2 = QtCore.QPoint(self.botBox.pos())
		shrunkWidth2 = 660
		height2 = self.botBox.geometry().height()
		width2 = self.botBox.geometry().width()
		self.animation2 = QPropertyAnimation(self.botBox, b'geometry')
		self.animation2.setEasingCurve(QEasingCurve.InOutCubic)
		self.animation2.setDuration(500)
		self.animation2.setStartValue(QRect(point2, QtCore.QSize(width2, height2)))
		self.animation2.setEndValue(QRect(point2, QtCore.QSize(shrunkWidth2, height2)))
		self.animation2.start()

	def maximizeMidWIn(self):
		# Stretching Mid box with Animation
		stretchWidth = 901
		point = QtCore.QPoint(self.midBox.pos())
		height = self.midBox.geometry().height()
		width = self.midBox.geometry().width()
		self.animation = QPropertyAnimation(self.midBox, b'geometry')
		self.animation.setEasingCurve(QEasingCurve.InOutCubic)
		self.animation.setDuration(500)
		self.animation.setStartValue(QRect(point, QtCore.QSize(width, height)))
		self.animation.setEndValue(QRect(point, QtCore.QSize(stretchWidth, height)))
		self.animation.start()
		# Stretching botBox with Animation
		point2 = QtCore.QPoint(self.botBox.pos())
		stretchWidth2 = 901
		height2 = self.botBox.geometry().height()
		width2 = self.botBox.geometry().width()
		self.animation2 = QPropertyAnimation(self.botBox, b'geometry')
		self.animation2.setEasingCurve(QEasingCurve.InOutCubic)
		self.animation2.setDuration(500)
		self.animation2.setStartValue(QRect(point2, QtCore.QSize(width2, height2)))
		self.animation2.setEndValue(QRect(point2, QtCore.QSize(stretchWidth2, height2)))
		self.animation2.start()

	# Methods to Open Dialog and then add Image Name to QlistWidget and Add Path to Dictionary##
	imgpathDict = dict()  # Storing Loaded Images Path with ,key as the object of the QlistWidget

	def dialogOpen(self):
		filename = QFileDialog.getOpenFileName()
		print(len(filename[0]))
		if len(filename[0]) != 0:
			imgPath = filename[0]
			imgName = imgPath.split("/")[-1]
			listWidgetItem = QListWidgetItem(imgName)
			if imgPath.endswith('tif'):
				path = 'UI Resources/FIle Formats/tiff.png'
			else:
				path = 'UI Resources/FIle Formats/jpeg.png'
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			listWidgetItem.setIcon(icon)
			self.imgpathDict[str(listWidgetItem)] = imgPath
			self.projectDirList.addItem(listWidgetItem)
			self.mainimagepath = imgPath
			self.updateSystem(1)
		else:
			print('empty')

	def deleteimagefromDir(self):
		itemAddress = self.projectDirList.currentItem()
		if itemAddress is not None:
			item = self.projectDirList.row(itemAddress)
			self.projectDirList.takeItem(item)
			self.imgpathDict.pop(str(itemAddress))
			self.isImageinProjectDir()
			print(self.projectDirList)

	##This method runs whenever ever image change is detectd wether from selection or deletion##
	def selectImageonChange(self):
		toselect = self.projectDirList.currentItem()
		if toselect is not None:
			path = self.imgpathDict[str(toselect)]
			self.mainimagepath = path

			self.updateSystem(1)

	##Method  to  easily update system Views##
	def updateSystem(self, f: int):
		self.setMetaData(f)
		self.setImage(f)
		self.setHistogram()

	## To check wether image exists in Directory or not ##
	def isImageinProjectDir(self):
		if self.projectDirList.currentItem() is None:
			self.updateSystem(0)
		else:
			self.updateSystem(1)

	## Method to Extact Meta Data and Setting it in the GUI Views ##

	def setMetaData(self, flag):
		jpeg_tags = ['Image ImageLength', 'Image ImageWidth', 'EXIF ColorSpace', 'Image Make', 'EXIF DateTimeOriginal']
		tif_tags = ['Image ImageLength', 'Image ImageWidth']
		tagtoberead = []
		block = [self.block1value, self.block2value, self.block3value, self.block4value, self.block5value]
		for b in range(len(block)):
			block[b].setText(jpeg_tags[b])
		if flag == 1:
			f = open(self.mainimagepath, 'rb')
			tags = exifread.process_file(f)
			fileformat = os.path.splitext(self.mainimagepath)[1]
			if fileformat == '.tif':
				tagtoberead = tif_tags
			else:
				tagtoberead = jpeg_tags
			for keys in range(len(tagtoberead)):
				if len(tags) != 0:
					print(str(tags[tagtoberead[keys]]))
					block[keys].setText(str(tags[tagtoberead[keys]]))
				else:
					print('not here')
					block[keys].setText('Nill')
		else:
			for keys in range(len(tagtoberead)):
				block[keys].setText('Nill')

	# setting second part of meta data
	def setMetaData2(self, flag=1):
		jpeg_tags = ['Image Model', 'Image Software', 'Focal Length In 35 mm Film', 'Image Focal Length Value',
					 'Image Shutter Speed Value']
		tif_tags = ['Image ImageLength', 'Image ImageWidth']
		tagtoberead = []
		print('hi')
		block = [self.block1value, self.block2value, self.block3value, self.block4value, self.block5value]
		imlabel = [self.block1Title, self.block2Title, self.block3Title, self.block4Title, self.block5Title]
		for b in range(len(block)):
			imlabel[b].setText(jpeg_tags[b])
		if flag == 1:
			f = open(self.mainimagepath, 'rb')
			tags = exifread.process_file(f)
			fileformat = os.path.splitext(self.mainimagepath)[1]
			if fileformat == '.tif':
				tagtoberead = tif_tags
			else:
				tagtoberead = jpeg_tags
			for keys in range(len(tagtoberead)):
				if len(tags) != 0:
					print(str(tags[tagtoberead[keys]]))
					block[keys].setText(str(tags[tagtoberead[keys]]))
				else:
					print('not here')
					block[keys].setText('Nil')
		else:
			for keys in range(len(tagtoberead)):
				block[keys].setText('Nil')

	# Method to set iamge in Main Image Window
	def setImage(self, flag: int):
		if flag == 1:
			self.mainImage.setPixmap(QtGui.QPixmap(self.mainimagepath))
			self.uploadhintGroup.hide()
		else:
			self.mainImage.setPixmap(QtGui.QPixmap("UI Resources/uploadimg.png"))
			self.uploadhintGroup.show()

	verticalayoutcounter = 0

	# Method to Calculate Histogram of the Image and setting it in the View

	def setHistogram(self):
		# reads an input image
		img = cv2.imread(self.mainimagepath, 0)
		# find frequency of pixels in range 0-255
		histogram = cv2.calcHist([img], [0], None, [256], [0, 256])
		# show the plotting graph of an image
		sc = MplCanvas(self, width=2, height=1, dpi=70)
		sc.axes.plot(histogram)
		# Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
		toolbar = NavigationToolbar(sc, MainWindow)

		# # # Create a placeholder widget to hold our toolbar and canvas.

		if self.verticalayoutcounter > 0:
			for i in reversed(range(self.verticalLayout.count())):
				self.verticalLayout.itemAt(i).widget().setParent(None)
		self.verticalLayout.addWidget(toolbar)
		self.verticalLayout.addWidget(sc)
		self.verticalayoutcounter = self.verticalayoutcounter + 1

	# Method to SHow MetaData##
	def showMeta(self):
		self.verticalLayoutWidget.hide()
		self.innerGroupBox.show()
		self.rSideGroupText.setText('MetaData')
		self.showRGroupBox()

	# Method to SHow HistData##
	def showHist(self):
		self.innerGroupBox.hide()
		self.verticalLayoutWidget.show()
		self.rSideGroupText.setText('Histogram')
		self.showRGroupBox()

	##To Run the Algo##

	def runForensics(self):
		self.commwin.append('Forensics started')
		pool = QThreadPool.globalInstance()
		runnable = Runnable(self.mainimagepath)
		pool.start(runnable)

class Runnable(QRunnable):
	def __init__(self,p):
		super().__init__()
		self.p = p

	def run(self):
		# Your long-running task goes here ...
		img = self.p
		print(img)
		"""Long-running task."""
		print('Task started')
		fim = cl.getChangeofLaplacian(img)
		tf.imwrite('OutputImages\\8bitpyth.tif', fim, photometric='rgb')
		print('Task Finished')

if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = UiMainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
