from conj_dirs_powell_method import ConjDirsPowellSolver
import numpy as np

n = 16
f = lambda x: 3 * (x[0] - n) ** 2 - x[0] * x[1] + 4 * x[1] ** 2
x0 = np.array([-1.2 * n - 4] * 2)
S1 = np.array([1, 0])
S2 = np.array([0, 1])
e = 0.01
decimals = 6

c = ConjDirsPowellSolver(x0, f, S1, S2, e, decimals).solve()
print(c.log())