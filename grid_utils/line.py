from grid_utils.point import Point


class Line:
    _point_a = None
    _point_b = None

    def __init__(self, point_a: Point, point_b: Point):
        self._point_a = point_a
        self._point_b = point_b

    @property
    def point_a(self):
        return self._point_a

    @point_a.setter
    def point_a(self, value):
        pass

    @property
    def point_b(self):
        return self._point_b

    @point_b.setter
    def point_b(self, value):
        pass

    def is_vertical(self):
        return self.point_a.y == self.point_b.y

    def is_horizontal(self):
        return self.point_a.x == self.point_b.x

    @staticmethod
    def select_horizontal_lines(lines):
        return [line for line in lines if line.is_horizontal()]

    @staticmethod
    def select_vertical_lines(lines):
        return [line for line in lines if line.is_vertical()]

    @staticmethod
    def select_horizontal_and_vertical_lines(lines):
        return [*Line.select_horizontal_lines(lines), *Line.select_vertical_lines(lines)]

    def get_points(self):
        return [self.point_a, self.point_b]
