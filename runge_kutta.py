import numpy as np
from galaxy import Galaxy


class RungeKutta:
    """
    m * d^2y/d^2t = f(t, y, z)

    t:自变量（时间）planteNum
    y:因变量（位置）
    z:导数（速度）
    """

    def __init__(self, galaxy: Galaxy, step: int = 10, delta_t: float = 1e2):
        self.step = step  # 绘制窗口期
        self.galaxy = galaxy
        self.delta_t = delta_t

    def _force(self, t, y, z, i):
        zn = np.zeros(3)
        for j in range(self.galaxy._starNum):
            if not i == j:  # 如果不是自身
                vector = self.galaxy.planet.Pos[j] - y  # 引力的方向
                zn += (
                    self.galaxy.G
                    * self.galaxy.planet.G[j]
                    * self.galaxy.planet.G[i]
                    * vector
                    / np.linalg.norm(vector) ** 3
                )
        return zn / self.galaxy.planet.G[i]

    # 更新星系
    def update(self):
        for _ in range(self.step):
            # 遍历所有星体
            for i in range(self.galaxy._starNum):
                x = 0
                y = self.galaxy.planet.Pos[i]
                z = self.galaxy.planet.V[i]
                h = self.delta_t

                k1 = z
                k2 = z + h / 2 * self._force(x, y, z, i)
                k3 = z + h / 2 * self._force(
                    x + h / 2, y + h / 2 * k1, z + h / 2 * k1, i
                )
                k4 = z + h * self._force(x + h / 2, y + h / 2 * k2, z + h / 2 * k2, i)
                l1 = self._force(x, y, z, i)
                l2 = self._force(x + h / 2, y + h / 2 * k1, z + h / 2 * l1, i)
                l3 = self._force(x + h / 2, y + h / 2 * k2, z + h / 2 * l2, i)
                l4 = self._force(x + h, y + h * k3, z + h * l3, i)
                y += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)  # 更新函数值
                z += h / 6 * (l1 + 2 * l2 + 2 * l3 + l4)  # 更新导数值
                """t += h"""  # 更新自变量
            self.galaxy.time += h
