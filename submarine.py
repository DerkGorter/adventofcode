import numpy as np
import pandas as pd

from sub_diagnostics import SubmarineDiagnosticsHelper
from sub_bingo import BingoSimulator
from grid_utils.line import Line
from grid_utils.grid import Grid
from lanternfish import LanternfishSchool


class Submarine:
    _depth_scan_report = None
    _diagnostics_helper = SubmarineDiagnosticsHelper()
    _position = {'horizontal': 0, 'depth': 0, 'aim': 0}
    _hydrothermal_lines = None

    def __init__(self):
        print("init submarine")

    def reset_position(self):
        self._position = {'horizontal': 0, 'depth': 0, 'aim': 0}

    def get_position(self) -> str:
        return f"Horizontal position {self.horizontal_position()}; Depth {self.vertical_position()}"

    def horizontal_position(self):
        return self._position['horizontal']

    def vertical_position(self):
        return self._position['depth']

    def aim(self):
        return self._position['aim']

    def get_depth_scan_results(self, scan_report: list) -> None:
        self._depth_scan_report = scan_report

    def determine_number_of_depth_increments(self, sliding_window_size: int = 1) -> int:
        report_length = len(self._depth_scan_report)

        # initialize pandas dataframe with of correct index lenght
        index = range(0, report_length + sliding_window_size - 1)
        df = pd.DataFrame(index=index)

        # for the size of the sliding window add columns to the df where the depth measurements are shifted
        for i in range(0, sliding_window_size):
            df[str(i)] = np.nan
            df.iloc[0+i:report_length+i, i] = self._depth_scan_report

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
        self._position[update_type] += value

        if update_type == 'horizontal':
            self._position['depth'] += value * self._position['aim']

    def read_diagnostics_report(self, report):
        self._diagnostics_helper.read_diagnostics_report(report)

    def process_diagnostics(self):
        return self._diagnostics_helper.process_diagnostics()

    @staticmethod
    def bingo_simulation(random_number_draw, bingo_boards: dict) -> tuple:
        bingo_sim = BingoSimulator(random_number_draw, bingo_boards)
        bingo_sim.run()
        win_order_dict = bingo_sim.get_win_order()

        winning_board_num, final_number_win = win_order_dict[0]
        winning_board = bingo_sim.get_bingo_board(winning_board_num)
        win_unmarked_sum = bingo_sim.get_unmarked_number_sum(winning_board_num)

        losing_board_num, final_number_lose = win_order_dict[len(win_order_dict) - 1]
        losing_board = bingo_sim.get_bingo_board(losing_board_num)
        loss_unmarked_sum = bingo_sim.get_unmarked_number_sum(losing_board_num)

        return (winning_board, final_number_win, win_unmarked_sum), (losing_board, final_number_lose, loss_unmarked_sum)

    def scan_hydrothermal_lines(self, hydrothermal_lines):
        self._hydrothermal_lines = hydrothermal_lines

    def determine_hydrothermal_danger_zones(self):
        lines_hz = Line.select_horizontal_and_vertical_lines(self._hydrothermal_lines)
        min_x, max_x, min_y, max_y = Grid.determine_grid_size_from_lines(lines_hz)
        grid = Grid(min_x, max_x, min_y, max_y, initial_value=0)
        grid.plot_lines(lines_hz)
        number_of_danger_zones_hz = grid.determine_danger_zones()

        min_x, max_x, min_y, max_y = Grid.determine_grid_size_from_lines(self._hydrothermal_lines)
        grid2 = Grid(min_x, max_x, min_y, max_y, initial_value=0)
        grid2.plot_lines(self._hydrothermal_lines)
        number_of_danger_zones = grid2.determine_danger_zones()

        return number_of_danger_zones_hz, number_of_danger_zones

    @staticmethod
    def lanternfish_simulation(fish_states, days):

        lantern_fish_school = LanternfishSchool(np.array(fish_states))
        lantern_fish_school.run_school_simulation(days)
        total_fish = lantern_fish_school.get_total_fish_amount()

        return total_fish

    @staticmethod
    def determine_lowest_fuel_costs_to_align_crab_positions(crab_positions, fuel_costs_non_linear=False):
        alignment_options = np.array(list(range(min(crab_positions), max(crab_positions)+1)))
        alignment_matrix = np.array([alignment_options for i in range(0, len(crab_positions))]).transpose()

        costs = abs(alignment_matrix - crab_positions)

        if fuel_costs_non_linear:
            linear_fuel_values = np.unique(costs)

            # reverse the order to avoid overwriting higher linear costs
            for x in linear_fuel_values[::-1]:
                costs[costs == x] = sum((range(0, x+1)))

        lowest_cost = min(costs.sum(axis=1))

        return lowest_cost
