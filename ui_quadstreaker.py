# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_quadstreaker.ui'
#
# Created: Wed Apr 24 15:12:09 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from ui_custom import QuadStreakerPushButton

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_quadstreaker(object):
    def setupUi(self, quadstreaker):
        quadstreaker.setObjectName(_fromUtf8("quadstreaker"))
        quadstreaker.resize(263, 585)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(quadstreaker.sizePolicy().hasHeightForWidth())
        quadstreaker.setSizePolicy(sizePolicy)
        quadstreaker.setMinimumSize(QtCore.QSize(0, 0))
        self.labelSplit = QtGui.QLabel(quadstreaker)
        self.labelSplit.setGeometry(QtCore.QRect(100, 205, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelSplit.setFont(font)
        self.labelSplit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelSplit.setObjectName(_fromUtf8("labelSplit"))
        self.btnSplit = QuadStreakerPushButton(quadstreaker)
        self.btnSplit.setGeometry(QtCore.QRect(10, 210, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnSplit.setFont(font)
        self.btnSplit.setObjectName(_fromUtf8("btnSplit"))
        self.btnMergeSuperCity = QuadStreakerPushButton(quadstreaker)
        self.btnMergeSuperCity.setGeometry(QtCore.QRect(10, 160, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnMergeSuperCity.setFont(font)
        self.btnMergeSuperCity.setObjectName(_fromUtf8("btnMergeSuperCity"))
        self.labelMergeSuperCity = QtGui.QLabel(quadstreaker)
        self.labelMergeSuperCity.setGeometry(QtCore.QRect(100, 170, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelMergeSuperCity.setFont(font)
        self.labelMergeSuperCity.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMergeSuperCity.setObjectName(_fromUtf8("labelMergeSuperCity"))
        self.labelCreateCity = QtGui.QLabel(quadstreaker)
        self.labelCreateCity.setGeometry(QtCore.QRect(100, 310, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelCreateCity.setFont(font)
        self.labelCreateCity.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelCreateCity.setObjectName(_fromUtf8("labelCreateCity"))
        self.btnCreateCity = QuadStreakerPushButton(quadstreaker)
        self.btnCreateCity.setGeometry(QtCore.QRect(10, 300, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnCreateCity.setFont(font)
        self.btnCreateCity.setObjectName(_fromUtf8("btnCreateCity"))
        self.btnMove = QuadStreakerPushButton(quadstreaker)
        self.btnMove.setGeometry(QtCore.QRect(10, 530, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnMove.setFont(font)
        self.btnMove.setObjectName(_fromUtf8("btnMove"))
        self.labelMove = QtGui.QLabel(quadstreaker)
        self.labelMove.setGeometry(QtCore.QRect(100, 515, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelMove.setFont(font)
        self.labelMove.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMove.setObjectName(_fromUtf8("labelMove"))
        self.btnAdd2Water = QuadStreakerPushButton(quadstreaker)
        self.btnAdd2Water.setGeometry(QtCore.QRect(10, 420, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnAdd2Water.setFont(font)
        self.btnAdd2Water.setObjectName(_fromUtf8("btnAdd2Water"))
        self.labelAdd2Water = QtGui.QLabel(quadstreaker)
        self.labelAdd2Water.setGeometry(QtCore.QRect(100, 430, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelAdd2Water.setFont(font)
        self.labelAdd2Water.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelAdd2Water.setObjectName(_fromUtf8("labelAdd2Water"))
        self.valLayerType = QtGui.QLabel(quadstreaker)
        self.valLayerType.setGeometry(QtCore.QRect(20, 20, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.valLayerType.setFont(font)
        self.valLayerType.setText(_fromUtf8(""))
        self.valLayerType.setObjectName(_fromUtf8("valLayerType"))
        self.valNumObjects = QtGui.QLabel(quadstreaker)
        self.valNumObjects.setGeometry(QtCore.QRect(140, 40, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.valNumObjects.setFont(font)
        self.valNumObjects.setText(_fromUtf8(""))
        self.valNumObjects.setObjectName(_fromUtf8("valNumObjects"))
        self.keyNumObjects = QtGui.QLabel(quadstreaker)
        self.keyNumObjects.setGeometry(QtCore.QRect(10, 40, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.keyNumObjects.setFont(font)
        self.keyNumObjects.setObjectName(_fromUtf8("keyNumObjects"))
        self.keyLayerName = QtGui.QLabel(quadstreaker)
        self.keyLayerName.setGeometry(QtCore.QRect(10, 0, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.keyLayerName.setFont(font)
        self.keyLayerName.setObjectName(_fromUtf8("keyLayerName"))
        self.txtSplit = QtGui.QTextEdit(quadstreaker)
        self.txtSplit.setGeometry(QtCore.QRect(100, 240, 101, 21))
        self.txtSplit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtSplit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtSplit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.txtSplit.setObjectName(_fromUtf8("txtSplit"))
        self.txtMove = QtGui.QTextEdit(quadstreaker)
        self.txtMove.setGeometry(QtCore.QRect(100, 550, 101, 21))
        self.txtMove.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtMove.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtMove.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.txtMove.setObjectName(_fromUtf8("txtMove"))
        self.btnAdd = QuadStreakerPushButton(quadstreaker)
        self.btnAdd.setGeometry(QtCore.QRect(10, 470, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btnAdd.setFont(font)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.labelAdd = QtGui.QLabel(quadstreaker)
        self.labelAdd.setGeometry(QtCore.QRect(100, 470, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelAdd.setFont(font)
        self.labelAdd.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelAdd.setObjectName(_fromUtf8("labelAdd"))
        self.btnUpdateGeom = QuadStreakerPushButton(quadstreaker)
        self.btnUpdateGeom.setGeometry(QtCore.QRect(10, 90, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnUpdateGeom.setFont(font)
        self.btnUpdateGeom.setObjectName(_fromUtf8("btnUpdateGeom"))
        self.labelUpdateGeom = QtGui.QLabel(quadstreaker)
        self.labelUpdateGeom.setGeometry(QtCore.QRect(100, 100, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelUpdateGeom.setFont(font)
        self.labelUpdateGeom.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelUpdateGeom.setObjectName(_fromUtf8("labelUpdateGeom"))
        self.btnCreateHood = QuadStreakerPushButton(quadstreaker)
        self.btnCreateHood.setGeometry(QtCore.QRect(10, 350, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnCreateHood.setFont(font)
        self.btnCreateHood.setObjectName(_fromUtf8("btnCreateHood"))
        self.labelCreateHood = QtGui.QLabel(quadstreaker)
        self.labelCreateHood.setGeometry(QtCore.QRect(100, 335, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.labelCreateHood.setFont(font)
        self.labelCreateHood.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelCreateHood.setObjectName(_fromUtf8("labelCreateHood"))
        self.lnALL = QtGui.QFrame(quadstreaker)
        self.lnALL.setGeometry(QtCore.QRect(10, 70, 241, 20))
        self.lnALL.setFrameShape(QtGui.QFrame.HLine)
        self.lnALL.setFrameShadow(QtGui.QFrame.Sunken)
        self.lnALL.setObjectName(_fromUtf8("lnALL"))
        self.labelALL = QtGui.QLabel(quadstreaker)
        self.labelALL.setGeometry(QtCore.QRect(70, 70, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelALL.setFont(font)
        self.labelALL.setAutoFillBackground(True)
        self.labelALL.setAlignment(QtCore.Qt.AlignCenter)
        self.labelALL.setObjectName(_fromUtf8("labelALL"))
        self.lnANY = QtGui.QFrame(quadstreaker)
        self.lnANY.setGeometry(QtCore.QRect(10, 400, 241, 20))
        self.lnANY.setFrameShape(QtGui.QFrame.HLine)
        self.lnANY.setFrameShadow(QtGui.QFrame.Sunken)
        self.lnANY.setObjectName(_fromUtf8("lnANY"))
        self.label = QtGui.QLabel(quadstreaker)
        self.label.setGeometry(QtCore.QRect(100, 400, 41, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.lnSUPERCITY = QtGui.QFrame(quadstreaker)
        self.lnSUPERCITY.setGeometry(QtCore.QRect(10, 130, 241, 20))
        self.lnSUPERCITY.setFrameShape(QtGui.QFrame.HLine)
        self.lnSUPERCITY.setFrameShadow(QtGui.QFrame.Sunken)
        self.lnSUPERCITY.setObjectName(_fromUtf8("lnSUPERCITY"))
        self.labelSUPERCITY = QtGui.QLabel(quadstreaker)
        self.labelSUPERCITY.setGeometry(QtCore.QRect(70, 130, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelSUPERCITY.setFont(font)
        self.labelSUPERCITY.setAutoFillBackground(True)
        self.labelSUPERCITY.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSUPERCITY.setObjectName(_fromUtf8("labelSUPERCITY"))
        self.lnCITY = QtGui.QFrame(quadstreaker)
        self.lnCITY.setGeometry(QtCore.QRect(10, 270, 241, 20))
        self.lnCITY.setFrameShape(QtGui.QFrame.HLine)
        self.lnCITY.setFrameShadow(QtGui.QFrame.Sunken)
        self.lnCITY.setObjectName(_fromUtf8("lnCITY"))
        self.labelCITY = QtGui.QLabel(quadstreaker)
        self.labelCITY.setGeometry(QtCore.QRect(70, 270, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelCITY.setFont(font)
        self.labelCITY.setAutoFillBackground(True)
        self.labelCITY.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCITY.setObjectName(_fromUtf8("labelCITY"))
        self.txtCreateHood = QtGui.QTextEdit(quadstreaker)
        self.txtCreateHood.setGeometry(QtCore.QRect(100, 370, 101, 21))
        self.txtCreateHood.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtCreateHood.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtCreateHood.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.txtCreateHood.setObjectName(_fromUtf8("txtCreateHood"))

        self.retranslateUi(quadstreaker)
        QtCore.QMetaObject.connectSlotsByName(quadstreaker)

    def retranslateUi(self, quadstreaker):
        quadstreaker.setWindowTitle(QtGui.QApplication.translate("quadstreaker", "quadstreaker", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSplit.setText(QtGui.QApplication.translate("quadstreaker", "Selected SuperQuads\n"
"and name as:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSplit.setText(QtGui.QApplication.translate("quadstreaker", "Split", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMergeSuperCity.setText(QtGui.QApplication.translate("quadstreaker", "Merge", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMergeSuperCity.setText(QtGui.QApplication.translate("quadstreaker", "Selected SuperCities", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCreateCity.setText(QtGui.QApplication.translate("quadstreaker", "From selected SuperCity", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCreateCity.setText(QtGui.QApplication.translate("quadstreaker", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMove.setText(QtGui.QApplication.translate("quadstreaker", "Move Into", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMove.setText(QtGui.QApplication.translate("quadstreaker", "Quad/SuperQuad into\n"
"parent ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd2Water.setText(QtGui.QApplication.translate("quadstreaker", "Add2Water", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAdd2Water.setText(QtGui.QApplication.translate("quadstreaker", "Selected Feature(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.keyNumObjects.setText(QtGui.QApplication.translate("quadstreaker", "# Objects Selected:", None, QtGui.QApplication.UnicodeUTF8))
        self.keyLayerName.setText(QtGui.QApplication.translate("quadstreaker", "Selected Layer Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("quadstreaker", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAdd.setText(QtGui.QApplication.translate("quadstreaker", "Add Quad/SuperQuad\n"
"click button then map", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdateGeom.setText(QtGui.QApplication.translate("quadstreaker", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUpdateGeom.setText(QtGui.QApplication.translate("quadstreaker", "Update Geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCreateHood.setText(QtGui.QApplication.translate("quadstreaker", "New Hood", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCreateHood.setText(QtGui.QApplication.translate("quadstreaker", "From selected shapefile\n"
"feature, name as:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelALL.setText(QtGui.QApplication.translate("quadstreaker", "All Types", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("quadstreaker", "Misc", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSUPERCITY.setText(QtGui.QApplication.translate("quadstreaker", "SuperCity", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCITY.setText(QtGui.QApplication.translate("quadstreaker", "City", None, QtGui.QApplication.UnicodeUTF8))
