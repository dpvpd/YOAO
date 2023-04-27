import math
class Vector2:
    def __init__(self, x, y):
        self.value = (x,y)
    
    def __repr__(self):
        return 'Vector({},{})'.format(self.value[0], self.value[1])
    
    def __call__(self):
        return self.value
    
    def getSize(self):
        x,y = self.value
        return ((x**2)+(y**2))**.5

    def getAngle(self, __x):
        x,y = self.value
        dx, dy = __x.value
        return math.asin(((x*dy)-(y*dx))/(self.getSize()*__x.getSize()))

    def cos(self, x):
        return math.cos(self.getAngle(x))
    def sin(self, x):
        return math.sin(self.getAngle(x))
    
    def __add__(self, __x):
        x, y = self.value
        dx, dy = __x.value
        return Vector2(x+dx, y+dy)
    
    def __sub__(self, __x):
        x, y = self.value
        dx, dy = __x.value
        return Vector2(x-dx, y-dy)
    
    def __mul__(self, __x):
        x, y = self.value
        if type(__x) in [type(int()), type(float())]:
            return Vector2(x*__x, y*__x)
        else:
            #원래 이게 외적이어야하고
            dx, dy = __x.value
            return (x*dx)+(y*dy)
    
    def __dot__(self, __x):
        #이게 내적이어야하지만
        #2차원벡터에선 외적이 없으므로 그냥 외적 위치에 내적 넣음
        print('@ 연산은 지원되지 않습니다. ')
        pass
