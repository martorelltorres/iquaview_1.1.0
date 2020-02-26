# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Iqua Robotics SL

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import signal
import logging
import argparse
from time import time

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
iquaview_root_path = srcpath + '/../../'
sys.path.append(iquaview_root_path)

from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplashScreen, QProgressBar
from qgis.core import QgsApplication
from iquaview.src.mainwindow import MainWindow

signal.signal(signal.SIGINT, signal.SIG_DFL)

LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--debug',
                    default=2,
                    type=int,
                    help='Verbosity level for log messages')
args, unknownargs = parser.parse_known_args()


def logger_init(level):
    """
    Initialize the logger for this thread.
    Sets the log level to ERROR (0), WARNING (1), INFO (2), or DEBUG (3),
    depending on the argument `level`.
    """
    levellist = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    handler = logging.StreamHandler()
    fmt = ('%(asctime)s [%(levelname)s] %(name)s %(lineno) -5d: %(message)s')
    handler.setFormatter(logging.Formatter(fmt,
                                           "%Y-%m-%d %H:%M:%S"))

    handler.setLevel(levellist[level])
    logger = logging.root
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def main(args=None):

    # supply path to qgis install location
    QgsApplication.setPrefixPath("/usr", True)

    # create a reference to the QgsApplication
    # setting the second argument to True enables the IquaView GUI,
    # which we need to do since this is a custom application
    qgs = QgsApplication([], True)

    # init splash screen
    splash_pix = QPixmap(':/resources/iquaview.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())

    light_blue = QColor(165,197,192)
    dark_blue = QColor(11,52,70)
    # adding progress bar
    progress_bar = QProgressBar(splash)
    p = progress_bar.palette()
    p.setColor(QPalette.Highlight, light_blue)
    p.setColor(QPalette.HighlightedText, dark_blue)
    progress_bar.setPalette(p)
    progress_bar.setMaximum(10)
    progress_bar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)

    splash.show()
    splash.showMessage("Initializing interface...", Qt.AlignBottom | Qt.AlignCenter, light_blue)

    # progress bar...
    for i in range(1, 11):
        progress_bar.setValue(i)
        t = time()
        if i == 5:
            splash.showMessage("Loading providers...", Qt.AlignBottom | Qt.AlignCenter, light_blue)
            # load providers
            qgs.initQgis()
            LOGGER.info(qgs.showSettings())
        if i == 10:
            # exec iquaview window
            window = MainWindow()
            window.setWindowIcon(QIcon(":/resources/iquaview_vector.svg"))
            splash.showMessage("IQUAview ready!", Qt.AlignBottom | Qt.AlignCenter, light_blue)


        while time() < t + 0.1:
            qgs.processEvents()

    window.showMaximized()
    splash.finish(window)

    qgs.exec_()
    window.deleteLater()
    # when app terminates, call exitQgis() to remove the provider and layer registries from memory
    qgs.exitQgis()


if __name__ == "__main__":
    logger_init(args.debug)
    main()
