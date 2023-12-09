import numpy as np
from decimal import Decimal, getcontext

from planet import Planet


# 星系
class Galaxy:
    def __init__(self, planetNum: int = 0, stellarNum: int = 0):
        self.step = 20
        self.time = 0
        self.delta_t: np.float64 = 1e4  # delta_t秒
        self._G = 6.67430e-11  # 万有引力常数
        self._stelliteNum = 0
        self._planetNum = planetNum
        self._stellarNum = stellarNum
        self._starNum = self._planetNum + self._stellarNum
        self._anchor_points = {}  # key：卫星，value：母星
        self.planet = Planet()

    @property
    def anchor_points(self):
        return self._anchor_points

    @property
    def starNum(self):
        return self._starNum

    @property
    def G(self):
        return self._G

    def add_stellar(self, starPost, starV, starG):
        self._stellarNum += 1
        self._starNum += 1
        starPost = np.reshape(starPost, (1, -1))  # 将starPost转换为1x3的二维数组
        starV = np.reshape(starV, (1, -1))  # 将starV转换为1x3的二维数组
        starG = np.reshape(starG, (1, -1))  # 将starG转换为1x1的二维数组
        value = np.concatenate((starPost, starV, starG), axis=1)
        self.planet.values = np.append(self.planet.values, value, axis=0)

    def add_planet(self, starPost, starV, starG):
        self._planetNum += 1
        self._starNum += 1
        starPost = np.reshape(starPost, (1, -1))  # 将starPost转换为1x3的二维数组
        starV = np.reshape(starV, (1, -1))  # 将starV转换为1x3的二维数组
        starG = np.reshape(starG, (1, -1))  # 将starG转换为1x1的二维数组
        value = np.concatenate((starPost, starV, starG), axis=1)
        self.planet.values = np.append(self.planet.values, value, axis=0)

    def add_stellite(self, masterPost, r, v, g):
        self._stelliteNum += 1
        self._planetNum -= 1  # 这里必须减1
        self.add_planet(masterPost + np.array((r, 0, 0)), v, g)

    def makeStellar1(self):
        self.add_stellar(
            (-1e10, 0.0, 0.0), (0.3471168881e4, 0.527249454e4, 0.0), 1.5e28
        )
        self.add_stellar((1e10, 0.0, 0.0), (0.3471168881e4, 0.527249454e4, 0.0), 1.5e28)
        self.add_stellar(
            (0.0, 0.0, 0.0), (-0.6942337762e4, -1.06544989808e4, 0.0), 1.5e28
        )

    def makeStellar2(self):
        self.add_stellar(
            (0.716248295712871e10, 0.384288553041130e10, 0.0),
            (1.245268230895990e4, 2.444311951776573e4, 0.0),
            1e31,
        )
        self.add_stellar(
            (0.086172594591232e10, 1.342795868576616e10, 0.0),
            (-0.675224323690062e4, -0.962879613630031e4, 0.0),
            1e31,
        )
        self.add_stellar(
            (0.538777980807643e10, 0.481049882655556e10, 0.0),
            (-0.57004390705925e4, -1.481432338146543e4, 0.0),
            1e31,
        )

    def makeStellar3(self):
        self.add_stellar((-1.1889693067e10, 0.0, 0.0), (0.0, 0.8042120498e4, 0.0), 1e30)
        self.add_stellar((3.8201881837e10, 0.0, 0.0), (0.0, 0.0212794833e4, 0.0), 1e30)
        self.add_stellar((-2.631218877e10, 0.0, 0.0), (0.0, -0.8254915331e4, 0.0), 1e30)

    def solarSystem(self):
        self.add_stellar((0, 0, 0), (0, 0, 0), 2e30)  # 太阳
        self.add_planet((58343153000.18, 0, 0), (0, 47870, 0), 5.97e24)  # 水星
        self.add_planet((107710436000.65, 0, 0), (0, 35020, 0), 4.87e24)  # 金星
        self.add_planet((149597828000.68, 0, 0), (0, 29783, 0), 5.97e24)  # 地球
        self.add_planet((227388699000.59, 0, 0), (0, 24070, 0), 6.39e23)  # 火星
        self.add_planet((816624856528.0308, 0, 0), (0, 12755.234, 0), 1.8982e27)  # 木星
        self.add_planet((1433147198000.73, 0, 0), (0, 9680, 0), 5.68e26)  # 土星
        self.add_planet((2875270267000.18, 0, 0), (0, 6810, 0), 8.68e25)  # 天王星
        self.add_planet((4495414751000.75, 0, 0), (0, 5430, 0), 1.02e26)  # 海王星
        self.add_stellite(
            self.planet.Pos[3], 384400000, (0, 1020 + 29783, 0), 7.34e22
        )  # 月球
        self.add_stellite(
            self.planet.Pos[5], 421800000, (0, 17330 + 12755.234, 0), 8.94e22
        )  # 伊欧
        self.add_stellite(
            self.planet.Pos[5], 671100000, (0, 13740 + 12755.234, 0), 4.8e22
        )  # 伊欧
        self.add_stellite(
            self.planet.Pos[5], 1070400000, (0, 10880 + 12755.234, 0), 1.48e23
        )  # 伊欧
        self.add_stellite(
            self.planet.Pos[5], 1882700000, (0, 8200 + 12755.234, 0), 1.08e23
        )  # 伊欧
        self._anchor_points[9] = 3
        self._anchor_points[10] = 5
        self._anchor_points[11] = 5
        self._anchor_points[12] = 5
        self._anchor_points[13] = 5
        return self._anchor_points

    def solarSystem_fake(self):
        self.add_stellar((0, 0, 0), (0, 0, 0), 1.989e30)  # 太阳
        self.add_stellar((1.496e11, 0, 0), (0, 29783, 0), 5.972e24)  # 地球
        self.add_stellite(self.planet.Pos[1], 384400, (0, 1020, 0), 7.34e22)  # 月球

    def rand_star(self):
        for i in range(self._planetNum):
            pos = (
                (np.random.rand() - 0.5) * 1e5,
                (np.random.rand() - 0.5) * 1e5,
                (np.random.rand() - 0.5) * 1e5,
            )
            v = (
                (np.random.rand() - 0.5) * 1e-5,
                (np.random.rand() - 0.5) * 1e-5,
                (np.random.rand() - 0.5) * 1e-5,
            )
            g = np.random.rand() * 1e10
            self.add_stellar(pos, v, g)

    def init_star(self):  # 生成恒星并随机生成行星
        self.makeStellar1()
        for i in range(self._planetNum):
            pos = (
                (np.random.rand() - 0.5) * 1e4,
                (np.random.rand() - 0.5) * 1e4,
                (np.random.rand() - 0.5) * 1e4,
            )
            v = (
                (np.random.rand() - 0.5) * 1e-1,
                (np.random.rand() - 0.5) * 1e-1,
                (np.random.rand() - 0.5) * 1e-1,
            )
            g = np.random.rand() * 1e-1
            self.add_stellar(pos, v, g)
