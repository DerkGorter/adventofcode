import pandas as pd
import numpy as np


class Grid:
    _min_x_grid = None
    _min_y_grid = None
    _max_x_grid = None
    _max_y_grid = None
    _grid_df = None
    _grid_matrix = None

    def __init__(self, min_x, max_x, min_y, max_y, initial_value: int):
        self._min_x_grid = min_x
        self._min_y_grid = min_y
        self._max_x_grid = max_x
        self._max_y_grid = max_y
        self._grid_df = pd.DataFrame(index=range(min_x, max_x + 1), columns=range(min_y, max_y + 1))
        self._grid_df = self._grid_df.applymap(lambda x: int(initial_value))
        self._grid_matrix = np.zeros(shape=(max_x - min_x + 1, max_y - min_y + 1))

    def __getitem__(self, slice_tuple):
        x_slice, y_slice = slice_tuple
        return self._grid_matrix[x_slice, y_slice]

    def __setitem__(self, slice_tuple, value):
        x_slice, y_slice = slice_tuple
        self._grid_matrix[x_slice, y_slice] = value

    def transpose(self):
        self._grid_matrix.transpose()

    def plot_lines(self, lines):
        for line in lines:
            self.plot_line(line)

    def plot_line(self, line):
        point_a = line.point_a
        point_b = line.point_b

        x_a = point_a.x
        x_b = point_b.x
        y_a = point_a.y
        y_b = point_b.y

        x_min = x_a if x_a < x_b else x_b
        x_max = x_a if x_a > x_b else x_b
        y_min = y_a if y_a < y_b else y_b
        y_max = y_a if y_a > y_b else y_b

        if line.is_vertical() or line.is_horizontal():
            current_values = self[x_min:x_max+1, y_min:y_max+1]
            new_values = [value + 1 for value in current_values]
            self[x_min:x_max+1, y_min:y_max+1] = new_values
        else:
            # check if one of the points is in the top left corner
            if (x_a, y_a) == (x_min, y_min) or (x_b, y_b) == (x_min, y_min):
                flip_left_right = False
            else:
                flip_left_right = True

            selection = self[x_min:x_max+1, y_min:y_max+1]

            if flip_left_right:
                selection = np.fliplr(selection)

            diagonal = selection.diagonal()
            diagonal_new = [value + 1 for value in diagonal]
            np.fill_diagonal(selection, diagonal_new)

            if flip_left_right:
                selection = np.fliplr(selection)
            self[x_min:x_max+1, y_min:y_max+1] = selection

    def determine_danger_zones(self):
        return sum(sum(self._grid_matrix > 1))

    @staticmethod
    def determine_grid_size_from_lines(lines):
        x_coordinates = []
        y_coordinates = []
        for line in lines:
            for point in line.get_points():
                x_coordinates.append(point.x)
                y_coordinates.append(point.y)

        min_x = min(x_coordinates)
        max_x = max(x_coordinates)
        min_y = min(y_coordinates)
        max_y = max(y_coordinates)

        return min_x, max_x, min_y, max_y
