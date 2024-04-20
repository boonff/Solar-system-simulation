import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


# 星体


class Planet:
    def __init__(self, pos: tuple = (0, 0, 0), velocity: tuple = (0, 0, 0), gravity: float = 9.8):
        self.pos: np = np.array(pos)
        self.velocity: np = np.array(velocity)
        self.gravity: float = gravity
        self.velocity_d: np = np.array((0, 0, 0))

    def compult_veclocity_d(self, planet):
        vector = (planet.pos - self.pos)
        #if np.linalg.norm(vector) < 1e-2:
            #self.velocity = 0
        return planet.gravity * self.gravity * vector / np.linalg.norm(vector)**3


win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Scrolling Plots Mode 1')
p1 = win.addPlot()
p1.setYRange(-1000, 1000, padding=0)
p1.setXRange(-1000, 1000, padding=0)
#星体数量
planet_num = 6
data_list = [[[]for _ in range(3)] for _ in range(planet_num)]
for i in range(planet_num):
    for j in range(2):
        data_list[i][j] = np.ones(1000)
curve_list = [[]for _ in range(planet_num)]
for i in range(planet_num):
    if i == 0:
        curve_list[i] = p1.plot(
            data_list[i][0], data_list[i][1], pen='w')
    else:
        curve_list[i] = p1.plot(
            data_list[i][0], data_list[i][1], pen=int(0xFFFFFF * i / (planet_num - 1 + 1e-7)))

planet_tuple = [[]for _ in range(planet_num)]

def makeStart1(a):
    planet_tuple[0] = Planet((-10000.0, 0.0, 0.0), (0.3471168881, 0.527249454, 0.0), 1e2)
    planet_tuple[1] = Planet((10000.0, 0.0, 0.0), (0.3471168881, 0.527249454, 0.0), 1e2)
    planet_tuple[2] = Planet((0.0, 0.0, 0.0), (-0.6942337762, -1.06544989808, 0.0), 1e2)

def makeStart2(a):
    planet_tuple[0] = Planet((0.716248295712871*1e4, 0.384288553041130*1e4, 0.0), (1.245268230895990, 2.444311951776573, 0.0), 1e4)
    planet_tuple[1] = Planet((0.086172594591232*1e4, 1.342795868576616*1e4, 0.0), (-0.675224323690062, -0.962879613630031, 0.0), 1e4)
    planet_tuple[2] = Planet((0.538777980807643*1e4, 0.481049882655556*1e4, 0.0), (-0.57004390705925, -1.481432338146543, 0.0), 1e4)

def makeStart3(a):
    planet_tuple[0] = Planet((-1.1889693067*1e4, 0.0, 0.0), (0.0, 0.8042120498, 0.0), 1e4)
    planet_tuple[1] = Planet((3.8201881837*1e4, 0.0, 0.0), (0.0, 0.0212794833, 0.0), 1e4)
    planet_tuple[2] = Planet((-2.631218877*1e4, 0.0, 0.0), (0.0, -0.8254915331, 0.0), 1e4)

def rand_planet(n):
    for i in range(n):
        pos = ((np.random.rand()-0.5) * 1e5, (np.random.rand()-0.5) * 1e5, (np.random.rand()-0.5) * 1e5)
        velocity = ((np.random.rand()-0.5)*1e-5, (np.random.rand()-0.5)*1e-5, (np.random.rand()-0.5)*1e-5)
        g = np.random.rand() * 1e10
    
        data_list[i][0][:] = data_list[i][0][:] * pos[0]
        data_list[i][1][:] = data_list[i][1][:] * pos[1]
        planet_tuple[i] = Planet(pos, velocity, g)

#生成恒星并随机生成行星（恒星数，行星数）
def init_planet(a, b):
        makeStart1(a)
        for i in range(a, a + b):
            pos = ((np.random.rand()-0.5) * 1e4, (np.random.rand()-0.5) * 1e4, (np.random.rand()-0.5) * 1e4)
            velocity = ((np.random.rand()-0.5) * 1e-1, (np.random.rand()-0.5) * 1e-1, (np.random.rand()-0.5) * 1e-1)
            g = np.random.rand() * 1e-1
            data_list[i][0][:] = data_list[i][0][:] * pos[0]
            data_list[i][1][:] = data_list[i][1][:] * pos[1]
            planet_tuple[i] = Planet(pos, velocity, g)

init_planet(3, 3)

#更新间隔
delta: float = 1e1

def update():
    global data_list, delta, planet_tuple, curve_list
    for i in range(planet_num):
        for j in range(3):
            data_list[i][j][:-1] = data_list[i][j][1:]
    for planet in planet_tuple:
        velocity_d = np.array((0, 0, 0))
        for except_planet in planet_tuple:
            if except_planet != planet:
                velocity_d = velocity_d + planet.compult_veclocity_d(except_planet)
                planet.velocity_d = velocity_d

        for planet in planet_tuple:
            planet.velocity = planet.velocity + planet.velocity_d * delta
            planet.pos = planet.pos + planet.velocity * delta

    # (see also: np.roll)
    for i in range(planet_num):
        for j in range(2):
            data_list[i][j][-1] = planet_tuple[i].pos[j]
    for i in range(planet_num):
        curve_list[i].setData(
            data_list[i][0], data_list[i][1])


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.exec_()
