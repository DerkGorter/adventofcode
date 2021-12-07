import numpy as np
import pandas as pd

from sub_diagnostics import SubmarineDiagnosticsHelper
from sub_bingo import BingoSimulator


class Submarine:
    depth_scan_report = None
    diagnostics_helper = SubmarineDiagnosticsHelper()
    position = {'horizontal': 0, 'depth': 0, 'aim': 0}

    def __init__(self):
        print("init submarine")

    def horizontal_position(self):
        return self.position['horizontal']

    def vertical_position(self):
        return self.position['depth']

    def aim(self):
        return self.position['aim']

    def get_depth_scan_results(self, scan_report: list) -> None:
        self.depth_scan_report = scan_report

    def determine_number_of_depth_increments(self, sliding_window_size: int = 1) -> int:
        report_length = len(self.depth_scan_report)

        # initialize pandas dataframe with of correct index lenght
        index = range(0, report_length + sliding_window_size - 1)
        df = pd.DataFrame(index=index)

        # for the size of the sliding window add columns to the df where the depth measurements are shifted
        for i in range(0, sliding_window_size):
            df[str(i)] = np.nan
            df.iloc[0+i:report_length+i, i] = self.depth_scan_report

        # drop rows that have less measurements than the sliding window size
        df = df.drop(np.array(range(0, sliding_window_size - 1)))
        df = df.drop(np.array(range(report_length, report_length + sliding_window_size - 1)))

        # compute sliding window sums
        window_sums = np.array(df.sum(axis=1))

        # compare the sums and thes sums shifted by one position to find the differences
        window_sums_shift = np.array([np.nan, *window_sums])
        window_sums = np.array([*window_sums, np.nan])
        differences = window_sums - window_sums_shift

        # find the number of increments
        number_of_increments = sum([int(d > 0) for d in differences if not np.isnan(d)])

        return number_of_increments

    def update_position(self, update_type: str, value: int) -> None:
        self.position[update_type] += value

        if update_type == 'horizontal':
            self.position['depth'] += value * self.position['aim']

    def get_position(self) -> str:
        return f"Horizontal position {self.horizontal_position()}; Depth {self.vertical_position()}"

    def read_diagnostics_report(self, report):
        self.diagnostics_helper.read_diagnostics_report(report)

    def process_diagnostics(self):
        return self.diagnostics_helper.process_diagnostics()

    @staticmethod
    def bingo_simulation(random_number_draw, bingo_boards):
        bingo_sim = BingoSimulator(random_number_draw, bingo_boards)
        win_order_dict = bingo_sim.run()

        winning_board_num, final_number_win = win_order_dict[0]
        winning_board = bingo_sim.bingo_boards[winning_board_num]
        win_unmarked_sum = bingo_sim.get_unmarked_number_sum(winning_board_num)

        losing_board_num, final_number_lose = win_order_dict[len(win_order_dict) - 1]
        losing_board = bingo_sim.bingo_boards[losing_board_num]
        loss_unmarked_sum = bingo_sim.get_unmarked_number_sum(losing_board_num)

        return (winning_board, final_number_win, win_unmarked_sum), (losing_board, final_number_lose, loss_unmarked_sum)

