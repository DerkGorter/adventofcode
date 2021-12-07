import os

from submarine import Submarine
from input_parser import InputParser


def main():
    input_file_path = os.getcwd() + "\\input_files\\"
    parser = InputParser(input_file_path=input_file_path)
    submarine = Submarine()

    day_1_depth_increment_assignment(submarine, parser, file_name="day_1_submarine.txt")
    day_2_dive_position_check(submarine, parser, file_name="day_2_dive.txt")
    day_3_binary_diagnostics(submarine, parser, file_name="day_3_binary_diagnostic.txt")
    day_4_bingo(submarine, parser, file_name="day_4_bingo.txt")


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


def day_3_binary_diagnostics(submarine, parser, file_name):
    diagnostics_report = parser.read_txt_file(file_name)

    submarine.read_diagnostics_report(diagnostics_report)
    gamma, epsilon, oxygen, co2 = submarine.process_diagnostics()

    print(f"Power consumption {int(gamma, 2) * int(epsilon, 2)}")
    print(f"Life support rating {int(oxygen, 2) * int(co2, 2)}")


def day_4_bingo(submarine, parser, file_name):
    random_draw, boards = parser.read_bingo_input(file_name)
    win_info, loss_info = submarine.bingo_simulation(random_draw, boards)

    winning_board, final_number_win, win_unmarked_sum = win_info
    print("winning_board:\n", winning_board, "\n\n final number: ", final_number_win, "\n unmarked sum: ", win_unmarked_sum)
    print("puzzle part one answer ", str(win_unmarked_sum * final_number_win))

    losing_board, final_number_lose, loss_unmarked_sum = loss_info
    print("losing_board:\n", losing_board, "\n\n final number: ", final_number_lose, "\n unmarked sum: ", loss_unmarked_sum)
    print("puzzle part two answer ", str(loss_unmarked_sum * final_number_lose))


if __name__ == "__main__":
    main()
