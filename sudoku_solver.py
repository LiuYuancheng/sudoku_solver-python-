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
# algrithom: https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku
# -----------------------------------------------------------------------------

import sys
from random import randint
from collections.abc import Iterable


from PyQt5 import(QtGui, QtCore)
# import QT UI lib
from PyQt5.QtCore import (Qt , QObject, QDate, QTime, QDateTime, 
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
    QDialog, QInputDialog, QColorDialog, QFontDialog, QFileDialog,
    qApp)

from PyQt5.QtGui import (QIcon, QFont, QPixmap, QDrag)
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen, QBrush, QPainterPath)


nowStr = QDate.currentDate()
dateTimeStr = QDateTime.currentDateTime()
timeStr = QTime.currentTime()


class keyboardPopup(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        lblName = QLabel(self.name, self)
        self.show()


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
        self.gridBtList = [[None]*9]*9
        self.numberList = [[0]*9]*9
        self.kb = None
        print(self.gridBtList)
        self.bgWidgets = QWidget(self)  # Init the background widget.
        grid = QGridLayout()
        positions = [(i, j) for i in range(9) for j in range(9)]
        for pos in positions:
            x, y = pos
            button = QPushButton(str(randint(0, 9)), self.bgWidgets)
            button.setMaximumSize(30, 30)
            button.setToolTip(','.join([str(x), str(y)]))
            button.clicked.connect(self.buttonClicked)

            grid.addWidget(button, x, y)
        self.bgWidgets.setLayout(grid)
        self.bgWidgets.show()
        self.setCentralWidget(self.bgWidgets)
        
        self.show()


    def mousePressEvent(self, event):
        
        if self.kb:
            self.kb.close()


    def buttonClicked(self):
        sender = self.sender()
        # use the tool tip to get the button poisition.
        print(sender.toolTip())
        sender.setStyleSheet("background-color: gray")
        self.buildExamplePopup(sender)
        if QtGui.qApp.mouseButtons() & QtCore.Qt.RightButton:
            print("Sense the right click.")

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


    # -----------------------------------------------------------------------------
    def buildExamplePopup(self, item):
        self.kb = QDialog()
        self.kb.setWindowFlags(Qt.FramelessWindowHint)
        bList = []
        for i in range(3):
            for j in range(3):
                b = QPushButton(str((i+1)*(j+1)),self.kb)
                bList.append(b)
                b.setMaximumSize(20, 20)
                b.move(i*20,j*20)

        self.kb.setWindowTitle(" ")
        self.kb.setWindowModality(Qt.ApplicationModal)
        self.kb.setGeometry(100, 100, 60, 60)
        self.kb.exec_()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TestUI()
    sys.exit(app.exec_())