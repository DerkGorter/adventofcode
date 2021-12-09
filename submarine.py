import numpy as np
import pandas as pd

from sub_toolbox.sub_diagnostics import SubmarineDiagnosticsHelper
from sub_games.sub_bingo import BingoSimulator
from sub_toolbox.grid_utils.line import Line
from sub_toolbox.grid_utils.grid import Grid
from ocean_life_forms.lanternfish_school import LanternfishSchool


class Submarine:
    """"
    Submarine class, to help save Christmas, by finding the lost sleigh keys in the ocean:

    Submarine the Elves keep ready for situations like this. It's covered in Christmas lights (because of course it is),
    and it even has an experimental antenna that should be able to track the keys if you can boost its signal strength
    high enough; there's a little meter that indicates the antenna's signal strength by displaying 0-50 stars.
    """
    _depth_scan_report = None
    _hydrothermal_lines = None
    _diagnostics_helper = SubmarineDiagnosticsHelper()
    _position = {'horizontal': 0, 'depth': 0, 'aim': 0}

    def __init__(self):
        print("Submarine submerged!")

    def reset_position(self) -> None:
        """"
        Reset the position of the submarine,
        by setting the values of the _position dictionary to zero
         """
        self._position = {'horizontal': 0, 'depth': 0, 'aim': 0}

    def get_position(self) -> tuple:
        """"Return the Submarine position as a tuple of (horizontal:int, depth: int)"""
        return self.horizontal_position(), self.vertical_position()

    def horizontal_position(self) -> int:
        """"Return the horizontal position of the submarine"""
        return self._position['horizontal']

    def vertical_position(self):
        """"Return the vertical position of the submarine"""
        return self._position['depth']

    def aim(self):
        """"Return the aim of the submarine"""
        return self._position['aim']

    def update_position(self, update_type: str, value: int) -> None:
        """"
        Update the position of the submarine
        :param update_type: a string specifying the type of update that must be performed
        :param value: integer value of the update to be performed

        When the update is of type 'horizontal' also perform a depth update of value * aim
        """
        self._position[update_type] += value

        if update_type == 'horizontal':
            self._position['depth'] += value * self._position['aim']

    def get_depth_scan_results(self, scan_report: list) -> None:
        """"
        Store the depth scan report in the Submarine class
        :param scan_report: A depth scan report as a list of int
        """
        self._depth_scan_report = scan_report

    def determine_number_of_depth_increments(self, sliding_window_size: int = 1) -> int:
        """"
        Calculate the number of increments in a list of ints
        :param sliding_window_size: set the size of the sliding window by passing an int

        Create a pandas DataFrame with index corresponding to depth scan report and the sliding window size.
        Add columns that match the sliding window size, drop irrelevant rows and count increments by checking row sums
        See example:     a  b               a = original scan report,   b = shifted report
                        [1  x] -> drop
                        [2  1] -> 3
                        [1  2] -> 3
                        [3  1] -> 4    <-- there is one increment in this example
                        [1  3] -> 3
                        [x  1] -> drop
        """
        depth_scan_report_length = len(self._depth_scan_report)

        # initialize pandas DataFrame with of correct index length
        index = range(0, depth_scan_report_length + sliding_window_size - 1)
        df = pd.DataFrame(index=index)

        # for the size of the sliding window add columns to the df where the depth measurements are shifted
        for i in range(0, sliding_window_size):
            df[str(i)] = np.nan
            df.iloc[0+i:depth_scan_report_length+i, i] = self._depth_scan_report

        # drop rows that have less measurements than the sliding window size
        df = df.drop(np.array(range(0, sliding_window_size - 1)))
        df = df.drop(np.array(range(depth_scan_report_length, depth_scan_report_length + sliding_window_size - 1)))

        # compute sliding window sums
        window_sums = np.array(df.sum(axis=1))

        # compare the sums and the sums shifted by one position to find the differences
        window_sums_shift = np.array([np.nan, *window_sums])
        window_sums = np.array([*window_sums, np.nan])
        differences = window_sums - window_sums_shift

        # find the number of increments
        number_of_increments = sum([int(d > 0) for d in differences if not np.isnan(d)])

        return number_of_increments

    def read_diagnostics_report(self, report: list) -> None:
        """"
        Pass a submarine diagnostics report to the _diagnostics_helper
        :param report: a list of binary numbers represented as strings
        """
        self._diagnostics_helper.read_diagnostics_report(report)

    def process_diagnostics(self) -> tuple:
        """"Process the diagnostics report with the _diagnostics_helper"""
        return self._diagnostics_helper.process_diagnostics()

    @staticmethod
    def bingo_simulation(random_number_draw: list, bingo_boards: dict) -> tuple:
        """"
        Run a bingo simulation to find the winning and losing board, including the final called number for both the
        winning and losing board. Also determines the sum of unmarked numbers for the winning and losing board.
        :param random_number_draw: a list of ints that represent the order of randomly drawn numbers
        :param bingo_boards: a dictionary of bingo boards {int: pd.DataFrame}
        """
        # Initialize the bingo simulator and run the simulation
        bingo_sim = BingoSimulator(random_number_draw, bingo_boards)
        bingo_sim.run()
        win_order_dict = bingo_sim.get_win_order()

        # from the simulation results, extract the winning board info
        winning_board_num, final_number_win = win_order_dict[0]
        winning_board = bingo_sim.get_bingo_board(winning_board_num)
        win_unmarked_sum = bingo_sim.get_unmarked_number_sum(winning_board_num)

        # from the simulation results, extract the losing board info
        losing_board_num, final_number_lose = win_order_dict[len(win_order_dict) - 1]
        losing_board = bingo_sim.get_bingo_board(losing_board_num)
        loss_unmarked_sum = bingo_sim.get_unmarked_number_sum(losing_board_num)

        return (winning_board, final_number_win, win_unmarked_sum), (losing_board, final_number_lose, loss_unmarked_sum)

    def scan_hydrothermal_lines(self, hydrothermal_lines: list) -> None:
        """"
        Add the hydrothermal line scan results as a private member to the submarine class
        :param hydrothermal_lines: a list of Line objects
        """
        self._hydrothermal_lines = hydrothermal_lines

    def determine_hydrothermal_danger_zones(self, only_hz: bool) -> tuple:
        """"
        Determine hydrothermal danger zones. these are the points where the _hydrothermal_lines intersect
        The danger zones will be determined for a selection of only the horizontal and vertical lines or all lines
        :param only_hz: bool to specify if only the horizontal and vertical lines should be considered
        """
        # Select the horizontal and vertical lines
        lines = self._hydrothermal_lines
        if only_hz:
            lines = Line.select_horizontal_and_vertical_lines(self._hydrothermal_lines)

        # Determine the outer points of the grid to plot lines on
        min_x, max_x, min_y, max_y = Grid.determine_grid_size_from_lines(lines)

        # Initialize a new grid and plot the selected lines
        grid = Grid(min_x, max_x, min_y, max_y, initial_value=0)
        grid.plot_lines(lines)

        # get the number of danger zones
        number_of_danger_zones = grid.determine_danger_zones()

        return number_of_danger_zones

    @staticmethod
    def lanternfish_simulation(fish_states: list, days: int) -> int:
        """"
        Simulate a lanternfish school. The lantern fish can have state 0 to 8 which is a countdown until the
        lanternfish spawns a new Lanternfish with state 8. The original fish resets to state 6.
        :param fish_states: a list of int with the initial states
        :param days: int number of days to run the simulation
        """
        lantern_fish_school = LanternfishSchool(np.array(fish_states))
        lantern_fish_school.run_school_simulation(days)
        total_fish = lantern_fish_school.get_total_fish_amount()

        return total_fish

    @staticmethod
    def determine_lowest_fuel_costs_to_align_crab_positions(crab_positions, fuel_costs_non_linear=False) -> int:
        """"
        Crabs in small submarines can help by aligning at the same horizontal position, this method
        determines the least amount of fuel costs for the crab submarines
        :param crab_positions: list of ints of initial crab positions
        :param fuel_costs_non_linear: bool indicating if fuel consumption is linear
        """
        # determine at what horizontal positions the crab submarines can align and create a martix with the
        # options for each crab submarine
        alignment_options = np.array(list(range(min(crab_positions), max(crab_positions)+1)))
        alignment_matrix = np.array([alignment_options for i in range(0, len(crab_positions))]).transpose()

        # determine the costs when fuel consumption is linear by subtracting the positions from the options
        costs = abs(alignment_matrix - crab_positions)

        # for non linear fuel consumption perform additional fuel calculation
        if fuel_costs_non_linear:
            linear_fuel_values = np.unique(costs)

            # reverse the order to avoid overwriting higher linear costs
            for x in linear_fuel_values[::-1]:
                costs[costs == x] = sum((range(0, x+1)))

        # determine the lowest costs
        lowest_cost = min(costs.sum(axis=1))

        return lowest_cost
