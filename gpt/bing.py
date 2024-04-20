import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
import psutil


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU使用率监控")
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.plot_widget = QtWidgets.QWidget()
        self.plot_layout = QtWidgets.QGridLayout()
        self.plot_widget.setLayout(self.plot_layout)
        self.plot_plt = pg.PlotWidget()
        self.plot_plt.showGrid(x=True, y=True)
        self.plot_layout.addWidget(self.plot_plt)
        self.main_layout.addWidget(self.plot_widget, 1, 0, 3, 3)

        self.data_list = []
        self.timer_start()

    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_cpu_info)
        self.timer.start(1000)

    def get_cpu_info(self):
        cpu = "%0.2f" % psutil.cpu_percent(interval=1)
        self.data_list.append(float(cpu))
        self.plot_plt.plot().setData(self.data_list, pen="g")


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
