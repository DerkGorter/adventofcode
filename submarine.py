import numpy as np
import pandas as pd


class Submarine:
    depth_scan_report = None
    position = {'horizontal': 0, 'depth': 0}

    def __init__(self):
        print("init submarine")

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

    def update_position(self, direction: str, distance: int) -> None:
        if direction == 'vertical':
            self.position['depth'] += distance
        elif direction == 'horizontal':
            self.position['horizontal'] += distance
        else:
            raise Exception(f'direction {direction} not implemented')

    def get_position(self) -> str:
        return f"Horizontal position {self.position['horizontal']}; Depth {self.position['depth']}"
