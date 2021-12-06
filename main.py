import os

from submarine import Submarine
from input_parser import InputParser


def main():
    input_file_path = os.getcwd() + "\\input_files\\"
    parser = InputParser(input_file_path=input_file_path)
    int_depth_list = parser.parse_int_list_from_txt("day_1_submarine.txt")

    submarine = Submarine()
    submarine.get_depth_scan_results(int_depth_list)
    sliding_window_size = 3
    depth_increments = submarine.determine_number_of_depth_increments(sliding_window_size)

    print("Depth increments ", depth_increments, f" [sliding window size {sliding_window_size}]")


if __name__ == "__main__":
    main()
