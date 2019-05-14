#!/usr/bin/python
# -----------------------------------------------------------------------------
# Name:        pyQtSudoku_Solver.py
#
# Purpose:     This module is used to learn Qt5 ui widgets.(by creat a )
#
# Author:      Yuancheng Liu
#
# Created:     2019/03/27
# Copyright:   YC
# License:     YC
# -----------------------------------------------------------------------------

import sys
from random import randint
from collections.abc import Iterable

# import QT UI lib
from PyQt5.QtCore import (Qt, QObject, QDate, QTime, QDateTime, 
                          QBasicTimer, QDate, QMimeData, pyqtSignal)

from PyQt5.QtWidgets import(
    # Qt main widget:
    QApplication, QMainWindow, QWidget, QDesktopWidget, QFrame,
    # Qt Layout:
    QHBoxLayout, QVBoxLayout, QGridLayout, QSplitter,
    # Qt components:
    QToolTip, QPushButton, QMessageBox, QMenu, QAction, QLabel, QComboBox,
    QLCDNumber, QSlider, QLineEdit, QCheckBox, QProgressBar, QCalendarWidget,
    # Qt dialogs:
    QInputDialog, QColorDialog, QFontDialog, QFileDialog,
    qApp)

from PyQt5.QtGui import (QIcon, QFont, QPixmap, QDrag)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath)


nowStr = QDate.currentDate()
dateTimeStr = QDateTime.currentDateTime()
timeStr = QTime.currentTime()


class TestUI(QMainWindow):
    """ Test UI used to test the QT function. 
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    # -----------------------------------------------------------------------------
    def initUI(self):
        self.setTitle()
        self.setGeometry(300, 300, 300, 350)
        # Add the menu area
        menubar = self.menuBar()
        clear = menubar.addMenu('Clear All')
        cal = menubar.addMenu('Calculate')

        self.bgWidgets = QWidget(self)  # Init the background widget.
        grid = QGridLayout()
        positions = [(i, j) for i in range(9) for j in range(9)]
        for pos in positions:
            x, y = pos
            button = QPushButton(str(randint(0, 9)), self.bgWidgets)
            button.setMaximumSize(30, 30)
            button.clicked.connect(self.buttonClicked)
            grid.addWidget(button, x, y)
        self.bgWidgets.setLayout(grid)
        self.bgWidgets.show()
        self.setCentralWidget(self.bgWidgets)
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        sender.setStyleSheet("background-color: gray")

    def keyPressEvent(self, event):
        print(int(event.key()-48))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(event, qp)
        qp.end()

    def drawLines(self, event, qp):
        pen = QPen(Qt.gray, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 132, 350, 132)
        qp.drawLine(0, 239, 350, 239)
        qp.drawLine(115, 0, 115, 350)
        qp.drawLine(222, 0, 222, 350)

    # -----------------------------------------------------------------------------
    def setTitle(self):
        """ Set the title bar of the window.
        """
        self.setWindowTitle("Soduku Calculaor by YC")
        self.setWindowIcon(QIcon('icon.jpg'))
        self.menubar = self.menuBar()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TestUI()
    sys.exit(app.exec_())