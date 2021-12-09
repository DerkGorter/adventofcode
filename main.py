import os
from sub_daily_tasks import *


def main() -> None:
    """"
    Run the adventofcode.com 2021 submarine
    """
    input_file_path = os.getcwd() + "\\input_files\\"
    parser = InputParser(input_file_path=input_file_path)
    submarine = Submarine()

    day_1_depth_increment_assignment(submarine, parser, file_name="day_1_submarine.txt")
    day_2_dive_position_check(submarine, parser, file_name="day_2_dive.txt")
    day_3_binary_diagnostics(submarine, parser, file_name="day_3_binary_diagnostic.txt")
    day_4_bingo(submarine, parser, file_name="day_4_bingo.txt")
    day_5_hydrothermal_venture(submarine, parser, file_name="day_5_hydrothermal_venture.txt")
    day_6_lanternfish(submarine, parser, file_name="day_6_lanternfish.txt")
    day_7_treachery_of_whales(submarine, parser, file_name="day_7_treachery_of_whales.txt")
    day_8_seven_segment_search(submarine, parser, file_name="day_8_seven_segment_search.txt")


if __name__ == "__main__":
    main()
