class Point:
    _x = None
    _y = None

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        pass

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        pass

