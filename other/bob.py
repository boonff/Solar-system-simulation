import numpy as np
from matplotlib import pyplot as plot
import time

delta: float = 1e-5
pi: float = 3.1415926536
u: float = 0.3

length = 1
g = 9.8
theta_thetad = np.array((pi/2, 2))
time_theta = np.array((0, 0))


def foo():
    return np.array((theta_thetad[1], -(g / length)*np.sin(theta_thetad[0]) - u*theta_thetad[1]))


t = time.time()
while(True):
    theta_thetad = theta_thetad + foo() * delta
    time_theta = time_theta + np.array((1, theta_thetad[0])) * delta
    if time.time() > t + 0.3:
        t = time.time()
        plot.ion()
        plot.xlim(-5, 100)
        plot.ylim(-5, 5)
        plot.scatter(time_theta[0], time_theta[1], 5)
        plot.pause(0.1)
        plot.ioff()
