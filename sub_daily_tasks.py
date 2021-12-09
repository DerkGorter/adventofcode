from submarine import Submarine
from input.input_parser import InputParser


def day_1_depth_increment_assignment(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    int_depth_list = parser.parse_int_list_from_txt(file_name)
    submarine.get_depth_scan_results(int_depth_list)
    sliding_window_size = 3
    depth_increments = submarine.determine_number_of_depth_increments(sliding_window_size)
    print("Depth increments ", depth_increments, f" [sliding window size {sliding_window_size}]")


def day_2_dive_position_check(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    instructions = parser.parse_movement_instructions(file_name)

    for update_type, value in instructions:
        submarine.update_position(update_type, value)

    horizontal_position, vertical_position = submarine.get_position()

    print(f"Horizontal position {horizontal_position}; Depth {vertical_position}")
    print('Day 2 daily taks answer ' + str(submarine.horizontal_position() * submarine.vertical_position()))


def day_3_binary_diagnostics(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    diagnostics_report = parser.read_txt_file(file_name)

    submarine.read_diagnostics_report(diagnostics_report)
    gamma, epsilon, oxygen, co2 = submarine.process_diagnostics()

    print(f"Power consumption {int(gamma, 2) * int(epsilon, 2)}")
    print(f"Life support rating {int(oxygen, 2) * int(co2, 2)}")


def day_4_bingo(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    random_draw, boards = parser.read_bingo_input(file_name)
    win_info, loss_info = submarine.bingo_simulation(random_draw, boards)

    winning_board, final_number_win, win_unmarked_sum = win_info
    print("winning_board:\n", winning_board, "\n\n final number: ", final_number_win, "\n unmarked sum: ",
          win_unmarked_sum)
    print("puzzle part one answer ", str(win_unmarked_sum * final_number_win))

    losing_board, final_number_lose, loss_unmarked_sum = loss_info
    print("losing_board:\n", losing_board, "\n\n final number: ", final_number_lose, "\n unmarked sum: ",
          loss_unmarked_sum)
    print("puzzle part two answer ", str(loss_unmarked_sum * final_number_lose))


def day_5_hydrothermal_venture(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    hydrothermal_lines = parser.parse_line_segments(file_name)
    submarine.scan_hydrothermal_lines(hydrothermal_lines)

    horizontal_and_vertical_danger_zones= submarine.determine_hydrothermal_danger_zones(only_hz=True)
    total_danger_zones = submarine.determine_hydrothermal_danger_zones(only_hz=False)

    print(f"danger zones horizontal/vertical: {horizontal_and_vertical_danger_zones}")
    print(f" total danger zones: {total_danger_zones}")


def day_6_lanternfish(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    lanternfish_initial_states = parser.parse_int_list_from_single_string(file_name)
    days = 256
    number_of_fish = submarine.lanternfish_simulation(lanternfish_initial_states, days=days)
    print(f"after {days} days there are {number_of_fish} lanternfish")


def day_7_treachery_of_whales(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    crab_positions = parser.parse_int_list_from_single_string(file_name)

    fuel_cost = submarine.determine_lowest_fuel_costs_to_align_crab_positions(crab_positions)
    fuel_cost_non_linear = submarine.determine_lowest_fuel_costs_to_align_crab_positions(
        crab_positions,
        fuel_costs_non_linear=True)

    print('crab alignment fuel costs ', fuel_cost)
    print('crab alignment non linear fuel costs', fuel_cost_non_linear)


def day_8_seven_segment_search(submarine: Submarine, parser: InputParser, file_name: str) -> None:
    print("dingen")
