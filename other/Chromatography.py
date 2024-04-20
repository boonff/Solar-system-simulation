import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import numpy as np


class ColorMapPlot:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        # 创建一个PlotItem
        self.plot_item = pg.PlotItem()
        self.plot_item.setTitle("Color Map")
        self.lineNum = 100
        self.data_list = [[[] for _ in range(2)] for _ in range(self.lineNum)]
        for i in range(self.lineNum):
            for j in range(2):
                self.data_list[i][j] = np.zeros(3)

        # 创建一个ImageItem
        self.curve_list = []

        # 设置窗口
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle("Color Map")
        self.p1 = self.win.addPlot()

        self.setData()
        self.setPlot()

    def hex_reb(self, hex_color):
        hex_color = int(hex_color)
        return ((hex_color >> 16) & 0xFF, (hex_color >> 8) & 0xFF, hex_color & 0xFF)

    # 设置曲线
    def setData(self):
        for i in range(self.lineNum):
            self.data_list[i][0][:] = np.array([i, i, i])
            self.data_list[i][1][:] = np.array([0, 0, 1000])

    def setPlot(self):
        for i in range(self.lineNum):
            color = pg.hsvColor(i / self.lineNum)
            curve = self.p1.plot(self.data_list[i][0], self.data_list[i][1], pen=None)
            curve.setPen(color, width=5)

            self.curve_list.append(curve)

    def update(self):
        pass

    def run_app(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(100)  # 设置更新间隔时间
        self.app.exec()


if __name__ == "__main__":
    color_map_plot = ColorMapPlot()
    color_map_plot.run_app()
