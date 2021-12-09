import numpy as np
import pandas as pd


class SubmarineDiagnosticsHelper:
    diagnostics_report = None

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
        diagnostics_df = SubmarineDiagnosticsHelper.diagnostics_report_to_df(diagnostics_report)
        sums = np.array(diagnostics_df.sum())
        binary_as_array = sums > (len(diagnostics_df) / 2)
        return SubmarineDiagnosticsHelper.binary_array_to_string(binary_as_array)

    @staticmethod
    def binary_array_to_string(binary_as_array):
        int_str_list = [str(int(x)) for x in binary_as_array]
        return ''.join(int_str_list)

    @staticmethod
    def diagnostics_life_support(diagnostics_report, support_type):
        diagnostics_df = SubmarineDiagnosticsHelper.diagnostics_report_to_df(diagnostics_report)
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
        binary_as_str = SubmarineDiagnosticsHelper.binary_array_to_string(binary_as_array)
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
