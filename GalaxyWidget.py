import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from PyQt5.QtWidgets import QSlider, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt
import numpy as np

from galaxy import Galaxy
from euler import Euler
from runge_kutta import RungeKutta
from orbit import Orbit


class GalaxyWidget(pg.GraphicsLayoutWidget):
    def __init__(self, orbit: Orbit):
        super().__init__()
        self.orbit = orbit
        self.follow = 0
        self.plot = self.addPlot()  # 创建绘图区域
        self.plot.scene().sigMouseClicked.connect(self._select_star)  # 获取鼠标点击的接口
        self._setWin()
        self.__curve_list = []  # 曲线列
        self._setCurve()
        self._setScatter()
        self._setSilder()

    def _update_delta_t(self, item: pg.TickSliderItem):
        delta_t = item.tickValue(0) * 1e4
        print(delta_t)
        self.orbit.update_delta_t(delta_t)

    def _select_star(self, event):
        pos = event.pos()
        print(f"Mouse clicked at position: {pos.x()}, {pos.y()}")
        for i in range(self.orbit.orbitNum):
            vector = pos - self.orbit.StarPos[i, :2]
            normal = np.linalg.norm(vector)

            if normal < 1e8:
                self.follow = i
                print("follow: " + str(self.follow))

    def _setWin(self):  # 设置窗口
        self.plot.setAspectLocked()  # 锁定坐标轴
        self.plot.setYRange(-1e10, 1e10, padding=0)
        self.plot.setXRange(-1e10, 1e10, padding=0)
        self.setBackground("k")  # 设置背景颜色在

    def _setScatter(self):
        self.scatter_plot = pg.ScatterPlotItem()  # 显示点
        self.plot.addItem(self.scatter_plot)

    def _setCurve(self):  # 设置曲线属性
        for i in range(self.orbit.orbitNum):
            color = pg.hsvColor(i / self.orbit.orbitNum)
            curve = self.plot.plot(pen=pg.mkPen(color, width=1))  # 创建曲线对象
            self.__curve_list.append(curve)

    def _setSilder(self):
        tickSlider = pg.TickSliderItem(
            orientation="bottom", allowAdd=False, allowRemove=False
        )  # 创建 TickSliderItem
        tickSlider.addTick(0)  # 添加标记
        tickSlider.sigTicksChanged.connect(self._update_delta_t)
        self.addItem(tickSlider, row=1, col=0)  # 添加到布局中

    def _update(self):
        time, data_curves, data_points = self.orbit.update()
        # 更新窗口标题为时间
        current_value = time / 60 / 60 / 24
        self.setWindowTitle(f"运行时间： {str(round(current_value, 5)) + '天'}")
        for i in range(self.orbit.orbitNum):  # 更新曲线
            self.__curve_list[i].setData(data_curves[i][0], data_curves[i][1])
        self.scatter_plot.setData(pos=data_points)  # 更新点
        # 跟随星体
        pos1 = np.array(
            [data_curves[self.follow][0][1], data_curves[self.follow][1][1]]
        )
        pos2 = np.array(
            [data_curves[self.follow][0][2], data_curves[self.follow][1][2]]
        )
        vector = pos1 - pos2
        view_box = self.plot.getViewBox()
        x_range, y_range = view_box.viewRange()
        self.plot.setXRange(x_range[0] + vector[0], x_range[1] + vector[0], padding=0)
        self.plot.setYRange(y_range[0] + vector[1], y_range[1] + vector[1], padding=0)
        print(f"X轴范围：{x_range}, Y轴范围：{y_range}")

    def run_app(self, app):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self._update)
        timer.start(0)
        app.exec()


if __name__ == "__main__":
    app = pg.mkQApp()  # 创建QGuiApplication
    galaxy = Galaxy()
    galaxy.solarSystem()
    orbit = Orbit(galaxy, low=100, up=1000, delta_t=1e3)
    pgWid = GalaxyWidget(orbit)
    pgWid.show()
    pgWid.run_app(app)
