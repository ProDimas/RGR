from conj_dirs_powell_method import ConjDirsPowellSolver
import numpy as np
from math import sqrt
from operator import attrgetter
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

n = 16
f = lambda x: 3 * (x[0] - n) ** 2 - x[0] * x[1] + 4 * x[1] ** 2
x0 = np.array([-1.2 * n - 4] * 2)
S1 = np.array([1, 0])
S2 = np.array([0, 1])
e = 0.01
decimals = 6

c = ConjDirsPowellSolver(x0, f, S1, S2, e, decimals).solve()

def tf_sqrt(x, z):
    return sqrt(abs(z - 3 * n ** 2 - (47 * x ** 2) / 16 + 6 * x * n))

def tf1(x, z):
    return x / 8 - tf_sqrt(x, z) / 2
tf1 = np.vectorize(tf1, excluded=['z'])

def tf2(x, z):
    return x / 8 + tf_sqrt(x, z) / 2
tf2 = np.vectorize(tf2, excluded=['z'])

def tf_args(z):
    val1 = sqrt(z + (3 * n ** 2) / 47)
    val2 = (12 * n) / sqrt(47)
    val3 = 4 / sqrt(47)
    return np.linspace(val3 * (-val1 + val2), val3 * (val1 + val2), 500)

zs = [-(3 * n ** 2) / 47 + np.power(2, i) for i in [5] + list(range(8, 13))]

fig, ax = plt.subplots(figsize=(10, 10))

for z in zs:
    args = tf_args(z)
    ax.plot(args, tf1(args, z=z), color='b')
    ax.plot(args, tf2(args, z=z), color='b')

f_x_points = list(map(attrgetter('f_x'), c.get_points()))[:-1]
for z in f_x_points:
    args = tf_args(z)
    ax.plot(args, tf1(args, z=z), color='darkviolet')
    ax.plot(args, tf2(args, z=z), color='darkviolet')

points = np.array(list(map(attrgetter('x'), c.get_points())))

zs = sorted(zs + f_x_points)
labels = np.array(zs).round(2)
x1_min = points[-1, 0]
for i, l in enumerate(labels[:6]):
    ax.annotate(str(l), (x1_min - 2, tf2(x1_min, zs[i]) + 0.3))

def get_left_lim(z):
    val1 = sqrt(z + (3 * 16 ** 2) / 47)
    val2 = (12 * 16) / sqrt(47)
    val3 = 4 / sqrt(47)
    return val3 * (-val1 + val2)

for i in range(6, 8):
    x = get_left_lim(zs[i])
    ax.annotate(str(labels[i]), (x + 2, tf2(x, zs[i]) + 8))

for i in range(8, len(labels)):
    x = get_left_lim(zs[i])
    offset = -2 if i == 8 else 0
    ax.annotate(str(labels[i]), (x + 6, tf2(x, zs[i]) + 25 + offset))

ax.plot(points[:, 0], points[:, 1], color='r')
ax.plot(points[[1, 3], 0], points[[1, 3], 1], linestyle='--', color='black')

rounded_points = points.round(4)
for i in range(points.shape[0] - 1):
    ax.scatter(points[i, 0], points[i, 1], c='g', s=20)
    label = f'x({i})=' + ' '.join(str(rounded_points[i]).split())
    ax.annotate(label, (points[i, 0] + 0.2, points[i, 1] - 1))
ax.scatter(points[-1, 0], points[-1, 1], c='g', s=20)
label = f'x(4)=' + ' '.join(str(rounded_points[-1]).split())
ax.annotate(label, (points[-1, 0] + 0.5, points[-1, 1] + 0.4))

lims = (-25, 25)
ax.set_xlim(*lims)
ax.set_ylim(*lims)
locs = list(range(lims[0], lims[1] + 1, 5))
ax.xaxis.set_major_locator(FixedLocator(locs))
ax.yaxis.set_major_locator(FixedLocator(locs))
ax.set_xlabel('x1')
ax.set_ylabel('x2')

fig.tight_layout()
plt.show()