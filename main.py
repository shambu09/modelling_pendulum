import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from celluloid import Camera


class Euler:

    def __init__(self, t, L=1, b=0, m=1):
        self.t_series = t
        self.t = t[1]
        self.t0 = t[0]
        self.angle = np.pi / 2
        self.angle_vel = 0
        self.g = 9.81
        self.b = b
        self.m = m
        self.L = L
        self.c1 = self.b / (self.m * self.L ** 2)
        self.c2 = self.g / self.L
        self.thetas = []

    def spit_angle(self):
        self.angle = self.angle + self.spit_angular_vel() * (self.t - self.t0)
        return self.angle

    def spit_angular_vel(self):
        self.angle_vel = self.angle_vel + (
            self.c1 * self.angle_vel - self.c2 * np.sin(self.angle)) * (self.t - self.t0)
        return self.angle_vel

    def fit(self):
        for i in range(self.t_series.shape[0] - 1):
            self.t = self.t_series[i + 1]
            self.t0 = self.t_series[i]
            theta = self.spit_angle()
            ang_vel = self.spit_angular_vel()
            self.thetas.append((theta, ang_vel))
        self.thetas.append(self.thetas[-1])
        self.thetas = np.array(self.thetas)
        return self.thetas


class rect:

    def __init__(self, x=0, y=0, x1=0, y1=0):
        self.u_l = np.array([x, y], dtype=np.float)
        self.l_r = np.array([x1, y1], dtype=np.float)
        self.l_l = np.array([x, y1], dtype=np.float)
        self.u_r = np.array([x1, y], dtype=np.float)
        self.x = [x, x1, x1, x]
        self.y = [y, y, y1, y1]

    def blit(self, ax, color):
        ax.fill(self.x, self.y, color=color)

    def update(self, x, y, x1, y1):
        self.x = [x, x1, x1, x]
        self.y = [y, y, y1, y1]


if __name__ == "__main__":
    delta_t = 0.02
    t_max = 10.0
    t = np.linspace(0, t_max, int(t_max / delta_t))

    e = Euler(t)
    r = rect(-0.05, 1, 0.05, 0.9)
    pend = rect()

    temp = e.fit()[:, 0]
    y = -np.cos(temp)
    x = np.sin(temp)

    fig = plt.figure()
    camera = Camera(fig)
    ax = plt.axes(xlim=(-4, 4), ylim=(-4, 4))
    ax.set_xticks([])
    ax.set_yticks([])

    for i in range(500):
        x_ = x[i]
        y_ = y[i]
        ax.plot([0, x_], [0.95, y_])
        pend.update(x_ - 0.025, y_ + 0.025, x_ + 0.025, y_ - 0.025)
        r.blit(ax, "red")
        pend.blit(ax, "green")
        camera.snap()

    anime = camera.animate()
    anime.save('pendulum.mp4',
               writer='ffmpeg', fps=30)
