import sys
import pandas as pd
import numpy as np
from datetime import datetime, time

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,  \
    QPushButton, QLabel
from PyQt6.QtGui import QFont

import pyqtgraph as pg
from pyqtgraph import mkPen


class TimeAxisItem(pg.DateAxisItem):
    def tickStrings(self, values, scale, spacing):
        return [QtCore.QDateTime.fromMSecsSinceEpoch(int(value)).toString('HH:mm') for value in values]
    
class Plots(QWidget):
    def __init__(self, xlimits=None, ylimits=None):
        super().__init__()
            
        now = datetime.utcnow().timestamp()
        start = now - 5
        end = now + 180
        xlow = start
        xhigh = end
        ylow = 41000
        yhigh = 44000

        self.w = pg.GraphicsLayoutWidget()
        self.w.setBackground('ivory')

        # Create three subplots
        self.p1 = self.w.addPlot(title="Plot 1")
        self.p2 = self.w.addPlot(title="Plot 2")
        self.p3 = self.w.addPlot(title="Plot 3")

        # Set the subplots in a vertical arrangement
        self.w.nextRow()  # Move to the next row
        self.w.addItem(self.p1)
        self.w.nextRow()  # Move to the next row
        self.w.addItem(self.p2)
        self.w.nextRow()  # Move to the next row
        self.w.addItem(self.p3)

        # Set the x-axis to be shared with plot1
        self.p2.setXLink(self.p1)
        self.p3.setXLink(self.p1)
        # self.p2.setYLink(self.p1)
        # self.p3.setYLink(self.p1)

        for p in [self.p1, self.p2, self.p3]:
            p.setXRange(xlow, xhigh)
            p.setYRange(ylow, yhigh)
            p.getAxis('left').setPen(mkPen('k', width=2))
            p.setAxisItems({'bottom': TimeAxisItem()})
            p.getAxis('left').setStyle(tickFont = QFont("Arial", 10), autoExpandTextSpace=True)
            p.getAxis('bottom').setPen(mkPen('k', width=2))
            p.getAxis('bottom').setStyle(tickFont = QFont("Arial", 10), autoExpandTextSpace=True)

        layout = QVBoxLayout()
        layout.addWidget(self.w)
        self.setLayout(layout)
        
    
def plots_main():
    app = QApplication(sys.argv)
    plots = Plots()
    plots.show()
    sys.exit(app.exec())    
        
    
if __name__ == '__main__':
    plots_main()