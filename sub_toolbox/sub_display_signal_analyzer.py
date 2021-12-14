class DisplaySignalAnalyzer:
    _unique_pattern_count = None
    _decoded_output = []
    _signal_data_raw = None
    _signal_data = None
    _test_signals_list = []
    _output_display_signals = []
    _signal_mappers = []

    def __init__(self, signal_data_raw=None):
        self._signal_data_raw = signal_data_raw

    def read_signals(self, signal_data_raw):
        self._signal_data_raw = signal_data_raw

    def get_unique_pattern_count(self):
        return self._unique_pattern_count

    def get_decoded_output(self):
        return self._decoded_output

    def prepare_signal_data(self) -> None:
        [self.clean_raw_signal_entry(signal) for signal in self._signal_data_raw]

    def clean_raw_signal_entry(self, signal) -> None:
        cleaned_signal = [entry.split(' ') for entry in signal.split('|')]
        cleaned_test_signal = [cs for cs in cleaned_signal[0] if cs != '']
        cleaned_out_signal = [cs for cs in cleaned_signal[1] if cs != '']
        self._test_signals_list.append(cleaned_test_signal)
        self._output_display_signals.append(cleaned_out_signal)

    def count_unique_patterns_in_output_signals(self) -> None:
        self._unique_pattern_count = \
            sum([self.count_unique_patterns_in_output_signal(signal) for signal in self._output_display_signals])

    @staticmethod
    def count_unique_patterns_in_output_signal(signal) -> int:
        return sum([len(single_digit_signal) in [2, 3, 4, 7] for single_digit_signal in signal])

    def get_decoded_output_sum(self):
        return sum(self._decoded_output)

    def decode_four_digit_output_values(self) -> None:
        self.determine_signal_mappings()
        self.decode_output_signals()

    def determine_signal_mappings(self):
        for test_signals in self._test_signals_list:
            self.get_signal_mapper_for_signal(test_signals)

    def get_signal_mapper_for_signal(self, test_signals):
        mapping = {}

        one_signal = None
        four_signal = None
        seven_signal = None

        sorted_signals_hold = []

        for test_signal in test_signals:
            sorted_signal = self.sorted_signal(test_signal)

            signal_length = len(sorted_signal)

            if signal_length == 2:
                mapping[sorted_signal] = 1
                one_signal = test_signal
            elif signal_length == 3:
                mapping[sorted_signal] = 7
                seven_signal = test_signal
            elif signal_length == 4:
                mapping[sorted_signal] = 4
                four_signal = test_signal
            elif signal_length == 7:
                mapping[sorted_signal] = 8
            else:
                sorted_signals_hold.append(sorted_signal)

        two_five_differentiator = [c for c in four_signal if c not in one_signal]

        for sorted_test_signal in sorted_signals_hold:
            signal_length = len(sorted_test_signal)

            if signal_length == 6:
                if all([c in sorted_test_signal for c in four_signal]):
                    mapping[sorted_test_signal] = 9
                elif all([c in sorted_test_signal for c in seven_signal]):
                    mapping[sorted_test_signal] = 0
                else:
                    mapping[sorted_test_signal] = 6

            if signal_length == 5:
                if all([c in sorted_test_signal for c in seven_signal]):
                    mapping[sorted_test_signal] = 3
                elif all([c in sorted_test_signal for c in two_five_differentiator]):
                    mapping[sorted_test_signal] = 5
                else:
                    mapping[sorted_test_signal] = 2

        self._signal_mappers.append(mapping)

    @staticmethod
    def sorted_signal(signal):
        return "".join(sorted(signal))

    def decode_output_signals(self):
        for i in range(0, len(self._output_display_signals)):
            mapper = self._signal_mappers[i]
            display_signals = self._output_display_signals[i]
            decoded_signals = [str(mapper[self.sorted_signal(signal)]) for signal in display_signals]
            self._decoded_output.append(int(''.join(decoded_signals)))
