import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Scrolling Plots Mode 1')

p1 = win.addPlot()
p1.setYRange(-10, 10, padding=0)
p1.setXRange(-10, 10, padding=0)
data0 = np.zeros(5000)
data1 = np.zeros(5000)
curve1 = p1.plot(data0, data1)

# bob
delta: float = 1e-3
u: float = 0.3
g = 9.8
velocity_d = 0
velocity = 0
high = 10


def update1():
    global data1, data0, delta, theta_thetad, time_theta
    data0[:-1] = data0[1:]
    data1[:-1] = data1[1:]  # shift data in the array one sample left
    velocity_d = -g * delta
    velocity = 0
    time_theta = time_theta + np.array((1, theta_thetad[0])) * delta

    # (see also: np.roll)
    data0[-1] = theta_thetad[0]
    data1[-1] = theta_thetad[1]
    curve1.setData(data0, data1)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update1)
timer.start(0)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.exec_()