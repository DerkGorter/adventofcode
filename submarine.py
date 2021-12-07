import numpy as np
import pandas as pd


class Submarine:
    depth_scan_report = None
    diagnostics_report = None
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
        self.diagnostics_report = report

    def process_diagnostics(self):
        gamma_rate = self.diagnostics_gamma_rate(self.diagnostics_report)
        epsilon_rate = self.invert_binary_number(gamma_rate)
        oxygen_generator_rating = self.diagnostics_life_support(self.diagnostics_report, support_type="oxygen")
        co2_scrubber_rating = self.diagnostics_life_support(self.diagnostics_report, support_type="co2")

        return gamma_rate, epsilon_rate, oxygen_generator_rating, co2_scrubber_rating

    @staticmethod
    def diagnostics_gamma_rate(diagnostics_report):
        diagnostics_df = Submarine.diagnostics_report_to_df(diagnostics_report)
        sums = np.array(diagnostics_df.sum())
        binary_as_array = sums > (len(diagnostics_df) / 2)
        return Submarine.binary_array_to_string(binary_as_array)

    @staticmethod
    def binary_array_to_string(binary_as_array):
        int_str_list = [str(int(x)) for x in binary_as_array]
        return ''.join(int_str_list)

    @staticmethod
    def diagnostics_life_support(diagnostics_report, support_type):
        diagnostics_df = Submarine.diagnostics_report_to_df(diagnostics_report)
        selection = diagnostics_df.copy()

        binary_number_total = len(diagnostics_df)

        i = 0
        bit_num = 0
        while len(selection) > 1 and i < binary_number_total:
            bit_values = selection.iloc[:, bit_num]
            remaining_number = len(selection)
            bit_sum = sum(bit_values)

            if support_type == "oxygen":
                selection_bit = int(bit_sum >= (remaining_number / 2))
            elif support_type == "co2":
                selection_bit = int(bit_sum < (remaining_number / 2))
            else:
                raise Exception(f'support type {support_type} not implemented')

            selection = selection[selection.iloc[:, bit_num] == selection_bit]

            bit_num += 1
            i += 1

        if len(selection) > 1:
            raise Exception('more than one binary number left')

        binary_as_array = np.array(selection.iloc[0])
        binary_as_str = Submarine.binary_array_to_string(binary_as_array)
        return binary_as_str

    @staticmethod
    def diagnostics_report_to_df(diagnostics_report):
        report = [list(x) for x in diagnostics_report]
        return pd.DataFrame(report).applymap(lambda x: int(x))

    @staticmethod
    def invert_binary_number(binary_number: str):
        temp = binary_number.replace('0', '_')
        temp = temp.replace('1', '0')
        return temp.replace('_', '1')
