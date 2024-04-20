from typing import Self
import numpy as np
from point import Point
from sven_algorithm import SvenSolver
from golden_section_method import GoldenSectionSolver
from dsk_powell_method import DSKPowellSolver

def eu(vector):
    return np.sqrt(np.sum(vector ** 2))
    
class ConjDirsPowellSolver:
    def __init__(self, x0, f, S1, S2, step_e, decimals):
        self.__decimals = decimals
        self.__raw_f = f
        self.__f = lambda x: Point._make([x.round(decimals), f(x.round(decimals))])
        self.__points = [self.__f(x0)]
        self.__S1 = S1
        self.__S2 = S2
        self.__step_e = step_e
        self.__log = ''
        self.__log_delimiter = '-' * 30 + '\n'
    
    def solve(self) -> Self:
        self.__log += 'Conjugate directions Powell algorithm iterations:\n'
        x = self.__points[-1].x
        self.__log += f'x_0 = [{x[0]} {x[1]}]; f(x_0) = {self.__points[-1].f_x}\n'
        self.__log += self.__log_delimiter
        directions = [self.__S2, self.__S1, self.__S2]
        step_size_mets = [GoldenSectionSolver] * 2 + [DSKPowellSolver]
        i = 1
        for S, met in zip(directions, step_size_mets):
            self.__log += f'Iteration {i}\n'
            self.__log += f'S = {S}\n'
            lstep, f_x = self.__next_x(x, S, met)
            x = (x + lstep * S).round(self.__decimals)
            self.__log += f'Movement:\n'
            self.__log += f'(step) l_{i - 1} = {lstep}\n'
            self.__log += f'x_{i} = [{x[0]} {x[1]}]; f(x_{i}) = {f_x}\n'
            self.__points.append(Point(x, f_x))
            i += 1
            self.__log += self.__log_delimiter
        
        self.__log += f'Iteration {i}\n'
        S = self.__points[3].x - self.__points[1].x
        self.__log += f'S = x_3 - x_1 = {S}\n'
        lstep, f_x = self.__next_x(x, S, DSKPowellSolver)
        x = (x + lstep * S).round(self.__decimals)
        self.__log += f'Movement:\n'
        self.__log += f'(step) l_{i - 1} = {lstep}\n'
        self.__log += f'x_{i} = [{x[0]} {x[1]}]; f(x_{i}) = {f_x}\n'
        self.__points.append(Point(x, f_x))
        return self
    
    def __next_x(self, x_base, S, met):
        l0 = 0
        x_of_l = lambda l: (x_base + l * S).round(self.__decimals)
        f_of_l = lambda l: Point._make([round(l, self.__decimals),
                                        round(
                                            self.__raw_f(x_of_l(round(l, self.__decimals))), self.__decimals
                                            )])
        self.__log += self.__log_delimiter
        dl = round(0.1 * eu(x_base) / eu(S), self.__decimals)
        self.__log += f'l0 = {l0}; dl = {dl}\n'
        interval_solver = SvenSolver(l0, dl, f_of_l).solve()
        interval = interval_solver.get_interval()
        self.__log += interval_solver.log()
        self.__log += self.__log_delimiter
        met_solver = met(interval, f_of_l, self.__step_e, self.__decimals).solve()
        self.__log += met_solver.log()
        return met_solver.get_minimum()

    def get_minimum(self):
        return self.__points[-1]
    
    def get_points(self):
        return self.__points
    
    def log(self):
        return self.__log