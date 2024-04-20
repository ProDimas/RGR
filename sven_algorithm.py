from typing import Self
from operator import attrgetter

class SvenSolver:
    def __init__(self, l0, dl, f):
        self.__f = f
        self.__l0 = f(l0)
        self.__dl = dl
        self.__log = ''
        pass

    def solve(self) -> Self:
        left = self.__f(self.__l0.x - self.__dl)
        right = self.__f(self.__l0.x + self.__dl)
        prev = self.__l0
        if left.f_x >= prev.f_x >= right.f_x:
            cur = right
        elif left.f_x <= prev.f_x <= right.f_x:
            self.__dl = -self.__dl
            cur = left
        elif left.f_x >= prev.f_x <= right.f_x:
            self.__interval = (left, prev, right)
            self.__make_log(self.__interval)
            return self
        else:
            raise Exception('function must be unimodal')
        
        k = 1
        next = self.__f(cur.x + self.__dl * (2 ** k))
        while next.f_x < cur.f_x:
            prev = cur
            cur = next
            k += 1
            next = self.__f(cur.x + self.__dl * (2 ** k))
        
        mid = self.__f(next.x - self.__dl * (2 ** (k - 1)))
        if next.f_x == cur.f_x:
            self.__interval = tuple(sorted([cur, mid, next], key=attrgetter('x')))
        else:
            self.__interval = self.__exclude_interval(*sorted([prev, cur, mid, next], key=attrgetter('x')))

        self.__make_log(self.__interval)
        return self

    def __exclude_interval(self, a, b, c, d):
        if b.f_x > c.f_x:
            return (b, c, d)
        elif b.f_x < c.f_x:
            return (a, b, c)
        else:
            return (b, self.__f((b.x + c.x) / 2), c)

    def get_interval(self) -> tuple[float, float, float]:
        return self.__interval
    
    def __make_log(self, interval):
        self.__log += 'Sven algorithm result:\n' + 'Interval:\n'
        l1, l2, l3 = interval
        self.__log += f'l1 = {l1.x}; f(l1) = {l1.f_x}\n'
        self.__log += f'l2 = {l2.x}; f(l2) = {l2.f_x}\n'
        self.__log += f'l3 = {l3.x}; f(l3) = {l3.f_x}\n'
    
    def log(self):
        return self.__log