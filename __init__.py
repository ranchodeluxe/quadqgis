# -*- coding: utf-8 -*-
"""
/***************************************************************************
 quadstreaker
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "QuadStreaker QuadQC"


def description():
    return "some sticks and stones for quality control"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "quadstreaker/pugetworks"

def email():
    return "info@pugetworks.com"

def classFactory(iface):
    # load quadstreaker class from file quadstreaker
    from quadstreaker import quadstreaker
    return quadstreaker(iface)
