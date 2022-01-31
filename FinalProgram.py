# -*- coding: utf-8 -*-
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
import exifread
import cv2
import matplotlib as plt

plt.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)


class UiMainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		flag = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
		MainWindow.setWindowFlags(flag)
		MainWindow.setFixedSize(1272, 752)
		MainWindow.setStyleSheet("#MainWindow{border :200px solid black;}")
		MainWindow.setIconSize(QtCore.QSize(27, 27))
		MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.mainwind = QtWidgets.QGroupBox(self.centralwidget)
		self.mainwind.setGeometry(QtCore.QRect(0, 0, 1271, 751))
		self.mainwind.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.mainwind.setStyleSheet(
			"#mainwind{background-Color : rgb(36, 34, 34);\n""color : rgb(255, 255, 255);\n" "border-radius : 20px;\n" "}")
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
			"#minButton{background-Color : rgb(36, 34, 34);border:0px solid black} #minButton:hover{background-Color : #57A773;}")
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
			"#closeButton{border-radius: 20px;background-Color : rgb(36, 34, 34)} #closeButton:hover{background-Color :#A71D31;border-radius: 20px} ")
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
			"#maximButton{background-Color : rgb(36, 34, 34);border:0px solid black} #maximButton:hover{background-Color :#F4A259}")
		self.maximButton.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/Square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.maximButton.setIcon(icon2)
		self.maximButton.setIconSize(QtCore.QSize(25, 25))
		self.maximButton.setObjectName("maximButton")
		self.logoLabel = QtWidgets.QLabel(self.mainwind)
		self.logoLabel.setGeometry(QtCore.QRect(10, 40, 211, 131))
		self.logoLabel.setText("")
		self.logoLabel.setPixmap(QtGui.QPixmap("UI Resources/logo/logo.png"))
		self.logoLabel.setScaledContents(True)
		self.logoLabel.setObjectName("logoLabel")
		self.botBox = QtWidgets.QGroupBox(self.mainwind)
		self.botBox.setGeometry(QtCore.QRect(220, 550, 901, 141))
		self.botBox.setStyleSheet(
			"background-Color : rgb(79, 76, 76);\n""color : rgb(255, 255, 255);\n""border-radius : 20px;")
		self.botBox.setTitle("")
		self.botBox.setObjectName("botBox")
		self.runWinText = QtWidgets.QLabel(self.botBox)
		self.runWinText.setGeometry(QtCore.QRect(20, 10, 861, 111))
		self.runWinText.setText("")
		self.runWinText.setObjectName("runWinText")
		self.midBox = QtWidgets.QGroupBox(self.mainwind)
		self.midBox.setGeometry(QtCore.QRect(220, 140, 901, 391))
		self.midBox.setStyleSheet(
			"background-Color : rgb(79, 76, 76);\n""color : rgb(255, 255, 255);\n""border-radius : 20px;")
		self.midBox.setTitle("")
		self.midBox.setObjectName("midBox")
		self.metaDataButton = QtWidgets.QPushButton(self.midBox)
		self.metaDataButton.setGeometry(QtCore.QRect(0, 20, 41, 31))
		self.metaDataButton.setText("MT")
		self.metaDataButton.setObjectName("metaDataButton")
		self.metaDataButton.clicked.connect(self.showMeta)
		self.histogramButton = QtWidgets.QPushButton(self.midBox)
		self.histogramButton.setGeometry(QtCore.QRect(0, 60, 41, 31))
		self.histogramButton.setText("Hist")
		self.histogramButton.setObjectName("histogramButton")
		self.histogramButton.clicked.connect(self.showHist)
		self.mainImage = QtWidgets.QLabel(self.midBox)
		self.mainImage.setGeometry(QtCore.QRect(250, 30, 381, 271))
		self.mainImage.setText("")
		self.mainImage.setPixmap(QtGui.QPixmap("UI Resources/uploadimg.png"))
		self.mainImage.setScaledContents(True)
		self.mainImage.setObjectName("mainImage")
		self.uploadhintGroup = QtWidgets.QGroupBox(self.midBox)
		self.uploadhintGroup.setGeometry(QtCore.QRect(250, 340, 401, 41))
		self.uploadhintGroup.setStyleSheet("background-color:rgb(49, 49, 49)")
		self.uploadhintGroup.setTitle("")
		self.uploadhintGroup.setObjectName("uploadhintGroup")
		self.label_2 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_2.setGeometry(QtCore.QRect(160, 10, 171, 21))
		self.label_2.setText("Please Upload the Image First ")
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_3.setGeometry(QtCore.QRect(120, 10, 31, 24))
		self.label_3.setText("")
		self.label_3.setPixmap(QtGui.QPixmap("UI Resources/plus Icon/plus 1.png"))
		self.label_3.setScaledContents(True)
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(self.uploadhintGroup)
		self.label_4.setGeometry(QtCore.QRect(80, 10, 41, 21))
		self.label_4.setText("Press")
		self.label_4.setObjectName("label_4")
		self.uploadButton = QtWidgets.QPushButton(self.mainwind)
		self.uploadButton.setGeometry(QtCore.QRect(40, 150, 141, 51))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.uploadButton.setFont(font)
		self.uploadButton.setAutoFillBackground(False)
		self.uploadButton.setStyleSheet(
			"background-color : rgb(55, 53, 53);\n""color : rgb(255, 255, 255);\n""border-radius : 20px;")
		self.uploadButton.setText("")
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap("UI Resources/plus Icon/plus 1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.uploadButton.setIcon(icon3)
		self.uploadButton.setIconSize(QtCore.QSize(40, 40))
		self.uploadButton.setObjectName("uploadButton")
		self.uploadButton.clicked.connect(self.dialogOpen)
		self.projectBox = QtWidgets.QGroupBox(self.mainwind)
		self.projectBox.setGeometry(QtCore.QRect(30, 240, 161, 451))
		self.projectBox.setStyleSheet(
			"background-Color : rgb(61, 61, 61);color : rgb(255, 255, 255);border-radius : 0px;")
		self.projectBox.setTitle("")
		self.projectBox.setObjectName("projectBox")
		self.projectDirList = QtWidgets.QListWidget(self.projectBox)
		self.projectDirList.setGeometry(QtCore.QRect(10, 10, 141, 411))
		self.projectDirList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.projectDirList.setObjectName("projectDirList")
		self.projectDirList.currentItemChanged.connect(self.selectImageonChange)
		self.deleteImgButton = QtWidgets.QPushButton(self.projectBox)
		self.deleteImgButton.setGeometry(QtCore.QRect(130, 420, 31, 31))
		self.deleteImgButton.setText("")
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap("UI Resources/Trash Can/trashcan1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.deleteImgButton.setIcon(icon4)
		self.deleteImgButton.setIconSize(QtCore.QSize(27, 27))
		self.deleteImgButton.setObjectName("deleteImgButton")
		self.deleteImgButton.clicked.connect(self.deleteimagefromDir)
		self.deleteImgButton.setStyleSheet(
			"background-Color : rgb(61, 61, 61);color : rgb(255, 255, 255);border-radius : 0px;")
		self.toolbar.raise_()
		self.logoLabel.raise_()
		self.minButton.raise_()
		self.closeButton.raise_()
		self.maximButton.raise_()
		self.botBox.raise_()
		self.midBox.raise_()
		self.uploadButton.raise_()
		self.projectBox.raise_()
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
		self.rSideGroup.setGeometry(QtCore.QRect(1241, 80, 0, 461))
		self.rSideGroup.setStyleSheet("border:0px")
		self.rSideGroup.setTitle("")
		self.rSideGroup.setObjectName("rSideGroup")
		self.rsideGroupCrossB = QtWidgets.QPushButton(self.rSideGroup)
		self.rsideGroupCrossB.setGeometry(QtCore.QRect(280, 10, 81, 51))
		self.rsideGroupCrossB.setStyleSheet("border : 0px;")
		self.rsideGroupCrossB.setText("")
		self.rsideGroupCrossB.clicked.connect(self.hideRGroupBox)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("UI Resources/Toolbar Icons/cross 2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.rsideGroupCrossB.setIcon(icon)
		self.rsideGroupCrossB.setIconSize(QtCore.QSize(30, 30))
		self.rsideGroupCrossB.setObjectName("rsideGroupCrossB")
		self.rSideGroupText = QtWidgets.QLabel(self.rSideGroup)
		self.rSideGroupText.setGeometry(QtCore.QRect(50, 10, 141, 41))
		font = QtGui.QFont()
		font.setPointSize(16)
		self.rSideGroupText.setFont(font)
		self.rSideGroupText.setStyleSheet("color :rgb(255, 255, 255)")
		self.rSideGroupText.setObjectName("rSideGroupText")
		self.innerGroupBox = QtWidgets.QGroupBox(self.rSideGroup)
		self.innerGroupBox.setGeometry(QtCore.QRect(10, 60, 351, 411))
		self.innerGroupBox.setTitle("")
		self.innerGroupBox.setObjectName("innerGroupBox")
		self.verticalLayoutWidget = QtWidgets.QWidget(self.rSideGroup)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 89, 321, 341))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.verticalLayoutWidget.hide()
		self.block1 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block1.setGeometry(QtCore.QRect(20, 50, 146, 100))
		self.block1.setStyleSheet("Background-color :rgb(53, 51, 51);\n"
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
		self.block2.setStyleSheet("Background-color :rgb(53, 51, 51);\n"
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
		self.block2value.setGeometry(QtCore.QRect(50, 40, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block2value.setFont(font)
		self.block2value.setStyleSheet("color : rgb(255, 255, 255)")
		self.block2value.setText("Nill")
		self.block2value.setObjectName("block2value")
		self.block4 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block4.setGeometry(QtCore.QRect(190, 180, 146, 100))
		self.block4.setStyleSheet("Background-color :rgb(53, 51, 51);\n"
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
		self.block4value.setGeometry(QtCore.QRect(50, 40, 81, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block4value.setFont(font)
		self.block4value.setStyleSheet("color : rgb(255, 255, 255);")
		self.block4value.setObjectName("block4value")
		self.block4value.setText("Nill")
		self.block4Title = QtWidgets.QLabel(self.block4)
		self.block4Title.setGeometry(QtCore.QRect(50, 10, 51, 16))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block4Title.setFont(font)
		self.block4Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block4Title.setText("Make")
		self.block4Title.setObjectName("block4Title")
		self.block3 = QtWidgets.QGroupBox(self.innerGroupBox)
		self.block3.setGeometry(QtCore.QRect(20, 180, 146, 100))
		self.block3.setStyleSheet("Background-color :rgb(53, 51, 51);\n"
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
		self.block5.setGeometry(QtCore.QRect(10, 290, 341, 101))
		self.block5.setStyleSheet("Background-color :rgb(53, 51, 51);\n"
		                          "border-radius : 20px;\n"
		                          "")
		self.block5.setTitle("")
		self.block5.setObjectName("block5")
		self.widget_3 = QtWidgets.QWidget(self.block5)
		self.widget_3.setGeometry(QtCore.QRect(10, 20, 16, 60))
		self.widget_3.setStyleSheet(
			"Background-color :qlineargradient(spread:pad, x1:0.395, y1:0.335227, x2:1, y2:1, stop:0 rgba(230, 119, 119, 255), stop:1 rgba(232, 11, 11, 255));\n"
			"border-radius : 5px;\n"
			"")
		self.widget_3.setObjectName("widget_3")
		self.block5Title = QtWidgets.QLabel(self.block5)
		self.block5Title.setGeometry(QtCore.QRect(110, 10, 131, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.block5Title.setFont(font)
		self.block5Title.setStyleSheet("color :rgb(255, 255, 255)")
		self.block5Title.setText("Creation Date")
		self.block5Title.setObjectName("block5Title")
		self.block5value = QtWidgets.QLabel(self.block5)
		self.block5value.setGeometry(QtCore.QRect(50, 38, 271, 31))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.block5value.setFont(font)
		self.block5value.setStyleSheet("color : rgb(255, 255, 255);")
		self.block5value.setText("Nill")
		self.block5value.setObjectName("block5value")
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
		self.hideAnimation.setDuration(500)  # chose the value that fits you
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
		self.showAnimation.setDuration(500)  # chose the value that fits you
		self.showAnimation.setEasingCurve(QEasingCurve.InOutCubic)
		self.showAnimation.setStartValue(self.rSideGroup.geometry())
		# computing final geometry
		self.showAnimation.setEndValue(QtCore.QRect(880, 80, 361, 461))
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

	## Methods to Open Dialog and then add Image Name to QlistWidget and Add Path to Dictionary##
	imgpathDict = dict()  # Storing Loaded Images Path with ,key as the object of the QlistWidget

	def dialogOpen(self):
		filename = QFileDialog.getOpenFileName()
		print(len(filename[0]))
		if len(filename[0]) != 0:
			imgPath = filename[0]
			imgName = imgPath.split("/")[-1]
			listWidgetItem = QListWidgetItem(imgName)
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

	##This method runs whenever ever image change is detectd wether from selection or deletion
	def selectImageonChange(self):
		toselect = self.projectDirList.currentItem()
		if toselect is not None:
			path = self.imgpathDict[str(toselect)]
			self.mainimagepath = path
			self.updateSystem(1)

	##Method  to  easil update system Views##
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
		exif_keys = ['Image ImageLength', 'Image ImageWidth', 'EXIF ColorSpace', 'Image Make', 'EXIF DateTimeOriginal']
		block = [self.block1value, self.block2value, self.block3value, self.block4value, self.block5value]
		if flag == 1:
			f = open(self.mainimagepath, 'rb')
			tags = exifread.process_file(f)
			print(tags)
			for keys in range(len(exif_keys)):
				if len(tags) != 0:
					print(str(tags[exif_keys[keys]]))
					block[keys].setText(str(tags[exif_keys[keys]]))
				else:
					print('not here')
					block[keys].setText('Nill')
		else:
			for keys in range(len(exif_keys)):
				block[keys].setText('Nill')

	## Method to set iamge in Main Image Window
	def setImage(self, flag: int):
		if flag == 1:
			self.mainImage.setPixmap(QtGui.QPixmap(self.mainimagepath))
			self.uploadhintGroup.hide()
		else:
			self.mainImage.setPixmap(QtGui.QPixmap("UI Resources/uploadimg.png"))
			self.uploadhintGroup.show()

	verticalayoutcounter = 0

	## Method to Calculate Histogram of the Image and setting it in the View

	def setHistogram(self):
		# reads an input image
		img = cv2.imread(self.mainimagepath, 0)
		# find frequency of pixels in range 0-255
		histr = cv2.calcHist([img], [0], None, [256], [0, 256])
		# show the plotting graph of an image
		sc = MplCanvas(self, width=3, height=2, dpi=50)
		sc.axes.plot(histr)
		if self.verticalayoutcounter > 0:
			for i in reversed(range(self.verticalLayout.count())):
				self.verticalLayout.itemAt(i).widget().setParent(None)
		self.verticalLayout.addWidget(sc)
		self.verticalayoutcounter = self.verticalayoutcounter + 1

	def showMeta(self):
		self.verticalLayoutWidget.hide()
		self.innerGroupBox.show()
		self.rSideGroupText.setText('MetaData')
		self.showRGroupBox()

	def showHist(self):
		self.innerGroupBox.hide()
		self.verticalLayoutWidget.show()
		self.rSideGroupText.setText('Histogram')
		self.showRGroupBox()


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = UiMainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
