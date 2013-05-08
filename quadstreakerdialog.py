# -*- coding: utf-8 -*-
"""
/***************************************************************************
 quadstreakerDialog
                                 A QGIS plugin
 some sticks and stones for quality control
                             -------------------
        begin                : 2013-04-08
        copyright            : (C) 2013 by quadstreaker/pugetworks
        email                : info@pugetworks.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_quadstreaker import Ui_quadstreaker, QuadStreakerPushButton
from qgis.core import *
from qgis.gui import *
# create the dialog for zoom to point


class quadstreakerDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self,None,QtCore.Qt.WindowStaysOnTopHint)
        # Set up the user interface from Designer.
        self.ui = Ui_quadstreaker()
        self.ui.setupUi(self)
        self.setFixedSize(263,585) # dimensions in ui_quadstreaker.py

    #
    #
    #  dialog globals
    #
    #
    def clearGlobals(self):
        self.ui.valLayerType.setText("")
        self.ui.valNumObjects.setText("")

    def setGlobalLayerType(self, text):
        self.ui.valLayerType.setText(text)

    def setGlobalNumObjects(self, text):
        self.ui.valNumObjects.setText(text)
    

