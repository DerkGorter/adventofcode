import os

from submarine import Submarine
from input_parser import InputParser


def main():
    input_file_path = os.getcwd() + "\\input_files\\"
    parser = InputParser(input_file_path=input_file_path)
    submarine = Submarine()

    day_1_depth_increment_assignment(submarine, parser, file_name="day_1_submarine.txt")
    day_2_dive_position_check(submarine, parser, file_name="day_2_dive.txt")


def day_1_depth_increment_assignment(submarine, parser, file_name):
    int_depth_list = parser.parse_int_list_from_txt(file_name)
    submarine.get_depth_scan_results(int_depth_list)
    sliding_window_size = 3
    depth_increments = submarine.determine_number_of_depth_increments(sliding_window_size)
    print("Depth increments ", depth_increments, f" [sliding window size {sliding_window_size}]")


def day_2_dive_position_check(submarine, parser, file_name):
    instructions = parser.parse_instructions(file_name)

    for direction, distance in instructions:
        submarine.update_position(direction, distance)

    print(submarine.get_position())
    print('puzzle answer ' + str(submarine.horizontal_position() * submarine.vertical_position()))


if __name__ == "__main__":
    main()
