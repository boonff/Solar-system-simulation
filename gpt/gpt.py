import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

app = QApplication([])

# 创建一个GraphicsView
view = pg.GraphicsView()

# 创建一个GraphicsScene
scene = pg.GraphicsScene()

# 将GraphicsScene设置为GraphicsView的场景
view.setScene(scene)

# 创建一个PlotItem
plot_item = pg.PlotItem()

# 在PlotItem中添加一个TickSliderItem
tick_slider = pg.TickSliderItem(orientation="bottom")
plot_item.addItem(tick_slider)

# 将PlotItem添加到GraphicsScene中
scene.addItem(plot_item)

# 显示窗口
view.show()

app.exec_()
