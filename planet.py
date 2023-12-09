import numpy as np


class Planet:
    def __init__(self):
        self.values = np.zeros((0, 7), np.float64)

    @property
    def Pos(self):
        return self.values[:, :3]

    @Pos.setter
    def Pos(self, new_pos):
        if new_pos.shape[1] == 3:
            self.values[:, :3] = new_pos
        else:
            raise ValueError("Invalid shape for Pos")

    @property
    def V(self):
        return self.values[:, 3:6]

    @V.setter
    def V(self, new_v):
        if new_v.shape[1] == 3:
            self.values[:, 3:6] = new_v
        else:
            raise ValueError("Invalid shape for V")

    @property
    def G(self):
        return self.values[:, -1]

    @G.setter
    def G(self, new_g):
        self.values[:, -1] = new_g
