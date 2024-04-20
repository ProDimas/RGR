from typing import Self
from operator import attrgetter

class DSKPowellSolver:
    def __init__(self, interval, f, e, decimals):
        self.__interval = interval
        self.__f = f
        self.__e = e
        self.__decimals = decimals
        self.__log = ''
    
    def solve(self) -> Self:
        self.__log += 'DSK-Powell algorithm iterations and result:\n'
        self.__min = self.__dsk(*self.__interval)
        left, mid, right = self.__interval
        i = 1
        self.__iteration_log(i, left, mid, right, self.__min)
        while not self.__end_criteria(mid, self.__min):
            i += 1
            min = sorted([left, mid, right, self.__min], key=attrgetter('f_x'))[0]
            points = sorted([left, mid, right, self.__min], key=attrgetter('x'))
            min_index = list(map(attrgetter('x'), points)).index(min.x)
            left, mid, right = points[min_index - 1:min_index + 2]
            a1 = self.__fraction_for_a(mid, left)
            a2 = 1 / (right.x - mid.x) * (self.__fraction_for_a(right, left) - a1)
            self.__min = self.__f((left.x + mid.x) / 2 - a1 / (2 * a2))
            self.__iteration_log(i, left, mid, right, self.__min)

        return self
    
    def __iteration_log(self, i, l1, l2, l3, lstar):
        self.__log += f'Iteration {i}:\n'
        self.__log += f'l1 = {l1.x}; f(l1) = {l1.f_x}\n'
        self.__log += f'l2 = {l2.x}; f(l2) = {l2.f_x}\n'
        self.__log += f'l3 = {l3.x}; f(l3) = {l3.f_x}\n'
        self.__log += f'l* = {lstar.x}; f(l*) = {lstar.f_x}\n'

    def __dsk(self, left, mid, right):
        delta = right.x - mid.x
        star = self.__f(mid.x + delta * (left.f_x - right.f_x) / (2 * (left.f_x - 2 * mid.f_x + right.f_x)))
        return star
    
    def __fraction_for_a(self, a, b):
        return (a.f_x - b.f_x) / (a.x - b.x)

    def __end_criteria(self, prev_min, new_min):
        f_cond = round(abs(prev_min.f_x - new_min.f_x), self.__decimals)
        x_cond = round(abs(prev_min.x - new_min.x), self.__decimals)
        self.__log += f'|f(l2) - f(l*)| = {f_cond} {'<=' if f_cond <= self.__e else '>'} e = {self.__e}\n'
        self.__log += f'|l2 - l*| = {x_cond} {'<=' if x_cond <= self.__e else '>'} e = {self.__e}\n'
        return (f_cond <= self.__e) and (x_cond <= self.__e)

    def get_minimum(self):
        return self.__min
    
    def log(self):
        return self.__log