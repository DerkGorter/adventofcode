from grid_utils.line import Line
from grid_utils.point import Point


def convert_movement_instruction(instruction: str) -> tuple:
    if 'up' in instruction:
        x = int(instruction.replace('up ', ''))
        return 'aim', -x
    elif 'down' in instruction:
        x = int(instruction.replace('down ', ''))
        return 'aim', x
    elif 'forward' in instruction:
        x = int(instruction.replace('forward ', ''))
        return 'horizontal', x


def convert_line_segemnt_str_to_line(line_segment_str: str) -> Line:
    points = line_segment_str.split(' -> ')

    a = [int(x) for x in points[0].split(',')]
    b = [int(x) for x in points[1].split(',')]

    point_a = Point(a[0], a[1])
    point_b = Point(b[0], b[1])

    return Line(point_a, point_b)
