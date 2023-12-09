import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from GalaxyWidget import GalaxyWidget
from galaxy import Galaxy
from orbit import Orbit

if __name__ == "__main__":
    app = pg.mkQApp()  # 创建QGuiApplication
    galaxy = Galaxy()
    galaxy.solarSystem()
    orbit = Orbit(galaxy, low=100, up=1000, delta_t=1e3)
    pgwid = GalaxyWidget(orbit)
    pgwid.show()
    pgwid.run_app(app)
