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
pi: float = 3.1415926536
u: float = 0.3
length = 1
g = 9.8
theta_thetad = np.array((pi/2, 3))
time_theta = np.array((0, 0))


def update1():
    global data1, data0, delta, theta_thetad, time_theta
    data0[:-1] = data0[1:]
    data1[:-1] = data1[1:]  # shift data in the array one sample left
    theta_thetad = theta_thetad + \
        np.array((theta_thetad[1], -(g / length) *
                 np.sin(theta_thetad[0]) - u*theta_thetad[1])) * delta
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
