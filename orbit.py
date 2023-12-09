import numpy as np

from galaxy import Galaxy
from euler import Euler
from runge_kutta import RungeKutta

"""
功能包括初始化轨道曲线，使用更新器更新星系和更新轨道曲线
可以在本类选择更新器
"""


class Orbit:
    def __init__(
        self, galaxy: Galaxy, low=100, up=1000, delta_t=1e2
    ):  # （星系，最小轨道长度，最大轨道长度）
        self._galaxy = galaxy
        self._orbitNum = galaxy.starNum
        self._delta_t = delta_t
        self._anchor_points = self._galaxy.anchor_points  # 生成星系
        self._euler = Euler(self._galaxy, step=20, delta_t=delta_t)  # 欧拉更新器
        self._runge_kuuta = RungeKutta(self._galaxy, step=5, delta_t=delta_t)  # 龙格库塔更新器

        self._data_points = np.zeros((self._galaxy._starNum, 2))  # 点列表
        self._data_curves = [
            [[] for _ in range(2)] for _ in range(self._galaxy._starNum)
        ]
        self._init_data_curves(low, up)

    @property
    def orbitNum(self):
        return self._orbitNum

    @property
    def delta_t(self):
        return self._delta_t

    @property
    def StarPos(self):
        return self._galaxy.planet.Pos

    def _curve_size(self, low, up):  # 计算每条曲线的长度
        vs = np.sum(self._galaxy.planet.V, axis=1)
        v_max = np.max(vs)
        curs = np.zeros(self._galaxy._starNum)
        for i in range(self._galaxy._starNum):
            v = max(vs[i], 1000)
            curs[i] = v_max / v

        d = np.average(curs)  # 缩放
        curs = curs * ((up - low) / d)  # 平移
        curs = curs - (min(curs) - low)

        for i in range(self._galaxy._starNum):  # 截取区间中的值
            curs[i] = max(low, min(up, curs[i]))
        return curs

    def _set_start(self):  # 设置曲线的所有点到星体的起点
        for i in range(self._galaxy._starNum):
            self._data_curves[i][0][:] = self._galaxy.planet.Pos[i][0]
            self._data_curves[i][1][:] = self._galaxy.planet.Pos[i][1]

    def _init_data_curves(self, low, up):  # 初始化曲线列表
        curs = self._curve_size(low, up)
        for i in range(self._galaxy._starNum):
            for j in range(2):
                self._data_curves[i][j] = np.zeros(int(curs[i]))  # 每条曲线的点数
        self._set_start()

    def update(self):
        self._euler.update()  # 更新星系

        for i in range(self._galaxy._starNum):  # 更新__data_curves
            self._data_curves[i][0][0] = self._galaxy.planet.Pos[i][0]
            self._data_curves[i][1][0] = self._galaxy.planet.Pos[i][1]
            if i in self._anchor_points.keys():  # 计算卫星曲线的相对位置
                pos1 = np.array(
                    [
                        self._data_curves[self._anchor_points[i]][0][0],
                        self._data_curves[self._anchor_points[i]][1][0],
                    ]
                )
                pos2 = np.array(
                    [
                        self._data_curves[self._anchor_points[i]][0][1],
                        self._data_curves[self._anchor_points[i]][1][1],
                    ]
                )
                vector = pos1 - pos2
                self._data_curves[i][0][1:] += vector[0]
                self._data_curves[i][1][1:] += vector[1]
        for i in range(self._galaxy._starNum):  # 使曲线前进
            self._data_curves[i][0][1:] = self._data_curves[i][0][:-1]
            self._data_curves[i][1][1:] = self._data_curves[i][1][:-1]
        for i in range(self._galaxy._starNum):  # 更新点列表
            self._data_points[i, 0] = self._galaxy.planet.Pos[i, 0]
            self._data_points[i, 1] = self._galaxy.planet.Pos[i, 1]
        return self._galaxy.time, self._data_curves, self._data_points

    def update_delta_t(self, delta_t):
        self._delta_t = delta_t
        self._euler.delta_t = delta_t
        self._runge_kuuta.delta_t = delta_t
