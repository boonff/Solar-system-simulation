import numpy as np
from galaxy import Galaxy


class Euler:
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

    def _force(self, t, i):
        z = np.zeros(3)
        for j in range(self.galaxy._starNum):
            if not i == j:  # 如果不是自身
                vector = self.galaxy.planet.Pos[j] - self.galaxy.planet.Pos[i]  # 引力的方向
                z += (
                    self.galaxy.G
                    * self.galaxy.planet.G[j]
                    * self.galaxy.planet.G[i]
                    * vector
                    / np.linalg.norm(vector) ** 3
                )
        return z / self.galaxy.planet.G[i]

    # 更新星系
    def update(self):
        for _ in range(self.step):
            # 遍历所有星体
            for i in range(self.galaxy._starNum):
                y = self.galaxy.planet.Pos[i]
                z = self.galaxy.planet.V[i]

                y += z * self.delta_t
                z += self._force(self.galaxy.time, i) * self.delta_t
                # t += self.delta_t
            self.galaxy.time += self.delta_t
