#!/usr/bin/python
# -----------------------------------------------------------------------------
# Name:        pyQt5_Sudoku_Calculator.py
#
# Purpose:     This module is used to learn Qt5 ui widgets.(by creat a Sudoku_Calculator)
#
# Author:      Yuancheng Liu <liu_yuan_cheng@Hotmail.com>
#
# Created:     2019/03/27
# algrithom: https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku
# -----------------------------------------------------------------------------

import os, sys
import time
from PyQt5 import(QtGui, QtCore)
# import QT UI lib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import(
    # Qt main widget:
    QApplication, QMainWindow, QWidget,
    # Qt Layout:
    QGridLayout,
    # Qt components:
    QFileDialog, QPushButton, QMessageBox, QAction, qApp)
from PyQt5.QtGui import QFont, QPainter,  QFont, QPen

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class SudokuCalculator(QMainWindow):
    """ pyQt5_Sudoku_Calculator """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.editingBt = None # the button user editing now.
        self.numberList = [[0 for j in range(9)] for i in range(9)]
        self.lockRslt = False # flag to lock the result

    # -----------------------------------------------------------------------------
    def initUI(self):
        """ Init the UI"""
        self.setGeometry(300, 300, 300, 350)
        self.setWindowTitle("pyQt5_Sudoku_Calculator_v0.1")
        # Add the menu area
        menubar = self.menuBar()
        cal = menubar.addMenu('Action')
        # 
        impEmAct = QAction('Get result', self)
        impEmAct.triggered.connect(self.calculateSu)
        cal.addAction(impEmAct)
        # 
        clearAll = QAction('Clear All', self)
        clearAll.triggered.connect(self.clearAll)
        cal.addAction(clearAll)
        #
        loadSu = QAction('Load Sudoku', self)
        loadSu.triggered.connect(self.loadFromFile)
        cal.addAction(loadSu)
        # Button list used for display the numbers.
        self.gridBtList = [[None for j in range(9)] for i in range(9)]
        # Display area:
        self.bgWidgets = QWidget(self)  # Init the background widget.
        grid = QGridLayout()
        positions = [(i, j) for i in range(9) for j in range(9)]
        for pos in positions:
            x, y = pos
            button = QPushButton(' ', self.bgWidgets)
            button.setMaximumSize(30, 30)
            # use tool tip to identify the button position.
            button.setToolTip(','.join([str(x), str(y)]))
            button.clicked.connect(self.buttonClicked)
            grid.addWidget(button, x, y)
            self.gridBtList[int(x)][int(y)] = button
        self.bgWidgets.setLayout(grid)
        self.bgWidgets.show()
        self.setCentralWidget(self.bgWidgets)
        self.show()

# -----------------------------------------------------------------------------
    def buttonClicked(self):
        """ When the user clicked the Sudoku grid area to set a number."""
        if self.lockRslt:
            print("The result has been locked, can not edit anymore.")
            return
        # Change previous button color to normal:
        if self.editingBt is not None:
            x, y = str(self.editingBt .toolTip()).split(',')
            if self.numberList[int(x)][int(y)] == 0:
                # reset to background color if the grid has not been set.
                self.editingBt.setStyleSheet("background-color: #E1E1E1")
        # High light the editing button.
        sender = self.sender()
        # use the tool tip to get the button poisition.
        x, y = str(sender.toolTip()).split(',')
        self.editingBt = self.gridBtList[int(x)][int(y)]
        self.editingBt.setStyleSheet("background-color: blue")

# -----------------------------------------------------------------------------
    def calculateSu(self):
        now = time.time()
        result = self.solveSudoku(self.numberList)
        period = time.time() - now
        print("The give sudoku solveing result is: %s" %str(result))
        if result:
            # Show the result:
            for idx, row in enumerate(self.gridBtList):
                for idy, button in enumerate(row):
                    button.setText(str(self.numberList[idx][idy]))
            QMessageBox.about(self, "Calculation result", "Get the result in:<%s> sec." %str(period))
            self.lockRslt = True
        else:
            QMessageBox.about(self, "Calculation result", "[x] The given sudoku got no solution!")
            self.lockRslt = False

# -----------------------------------------------------------------------------
    def clearAll(self):
        """ re-init all the parameters."""
        for row in self.gridBtList:
            for button in row:
                button.setText(' ')
                button.setStyleSheet("background-color: #E1E1E1")
        self.numberList = [[0 for j in range(9)] for i in range(9)]
        self.editingBt = None
        self.lockRslt = False

# -----------------------------------------------------------------------------
    def drawLines(self, event, qp):
        """Draw the grid lines."""
        qp.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        qp.drawLine(0, 132, 350, 132)
        qp.drawLine(0, 239, 350, 239)
        qp.drawLine(115, 0, 115, 350)
        qp.drawLine(222, 0, 222, 350)

# -----------------------------------------------------------------------------
    def findNextCellToFill(self, grid, i, j):
        """ find the next grid position whick can fill in."""
        for x in range(i, 9):
            for y in range(j, 9):
                if grid[x][y] == 0: return x, y
        for x in range(0, 9):
            for y in range(0, 9):
                if grid[x][y] == 0: return x, y
        return -1, -1

# -----------------------------------------------------------------------------
    def isValid(self, grid, i, j, e):
        """ Check whether the fill in numbers in the grid are valid"""
        rowOk = all([e != grid[i][x] for x in range(9)])
        if rowOk:
            columnOk = all([e != grid[x][j] for x in range(9)])
            if columnOk:
                # finding the top left x,y co-ordinates of the section containing the i,j cell
                secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
                for x in range(secTopX, secTopX+3):
                    for y in range(secTopY, secTopY+3):
                        if grid[x][y] == e:
                            return False
                return True
        return False

# -----------------------------------------------------------------------------
    def keyPressEvent(self, event):
        """ Handle all the user number input."""
        keyNum = int(event.key()-48) # Convert the key AsicII to number.
        x, y = str(self.editingBt.toolTip()).split(',')
        if 0 < keyNum < 10:
            self.editingBt.setText(str(keyNum))
            self.numberList[int(x)][int(y)] = keyNum
            self.editingBt.setStyleSheet("background-color: gray")
        else:
            self.editingBt.setText(' ')
            self.numberList[int(x)][int(y)] = 0
            self.editingBt.setStyleSheet("background-color: #E1E1E1")

# -----------------------------------------------------------------------------
    def loadFromFile(self):
        """ Load unfished Sudoku from file"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
        if fname[0]:
            with open(fname[0], 'r') as f:
                for idx in range(9):
                    dataStr = f.readline()
                    numList = dataStr.split(',')
                    if len(numList) != 9: 
                        print("The input file is invalid.")
                        self.clearAll()
                    for idy, num in enumerate(numList):
                        self.numberList[idx][idy] = int(num)
                        if int(num) !=0:
                            self.gridBtList[idx][idy].setText(str(num))
                            self.gridBtList[idx][idy].setStyleSheet("background-color: gray")
        else:
            print("Input file not exists")

# -----------------------------------------------------------------------------
    def paintEvent(self, event):
        """Draw the grid for the number display area"""
        qp = QPainter()
        qp.begin(self)
        self.drawLines(event, qp)
        qp.end()

# -----------------------------------------------------------------------------
    def solveSudoku(self, grid, i=0, j=0):
        i,j = self.findNextCellToFill(grid, i, j)
        if i == -1: return True
        for e in range(1,10):
            if self.isValid(grid,i,j,e):
                grid[i][j] = e
                if self.solveSudoku(grid, i, j): return True
                # Undo the current cell for backtracking
                grid[i][j] = 0
        return False
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SudokuCalculator()
    sys.exit(app.exec_())
