from typing import Self

class GoldenSectionSolver:
    LEFT_CONST: float = 0.382

    RIGHT_CONST: float = 0.618

    def __init__(self, interval, f, e, decimals):
        self.__interval = (interval[0], interval[-1])
        self.__f = f
        self.__e = e
        self.__decimals = decimals
        self.__log = ''
    
    def solve(self) -> Self:
        a, b = self.__interval
        l = b.x - a.x
        if l <= self.__e:
            self.__make_log(self.__interval)
            return self
        
        left = self.__f(a.x + self.LEFT_CONST * l)
        right = self.__f(a.x + self.RIGHT_CONST * l)
        while l > self.__e:
            if left.f_x <= right.f_x:
                b = right
                right = left
                l = b.x - a.x
                left = self.__f(a.x + self.LEFT_CONST * l)
            else:
                a = left
                left = right
                l = b.x - a.x
                right = self.__f(a.x + self.RIGHT_CONST * l)
        
        self.__interval = (a, b)
        self.__make_log(self.__interval)
        return self
    
    def get_minimum(self):
        a, b = self.__interval
        if a.f_x < b.f_x:
            return a
        else:
            return b
        
    def __make_log(self, interval):
        a, b = interval
        self.__log += 'Golden section algorithm result:\n'
        self.__log += f'a = {a.x}; f(a) = {a.f_x}\n'
        self.__log += f'b = {b.x}; f(b) = {b.f_x}\n'
        self.__log += f'L = {round(b.x - a.x, self.__decimals)} <= e = {self.__e}\n'
    
    def log(self):
        return self.__log