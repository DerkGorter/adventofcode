from sub_toolbox import sub_utils
from unittest import TestCase
from submarine import Submarine

submarine = Submarine()


class SubmarineTesting(TestCase):
    def test_determine_number_of_depth_increments(self):
        test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        expected_result = 7

        submarine.get_depth_scan_results(test_input)
        test_result = submarine.determine_number_of_depth_increments(sliding_window_size=1)

        self.assertEqual(test_result, expected_result)

    def test_determine_number_of_depth_increments_sliding_window(self):
        test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        expected_result = 5

        submarine.get_depth_scan_results(test_input)
        test_result = submarine.determine_number_of_depth_increments(sliding_window_size=3)

        self.assertEqual(test_result, expected_result)

    def test_movement(self):
        test_input = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
        expected_result = (15, 60)

        submarine.reset_position()

        for instruction in test_input:
            update_type, value = sub_utils.convert_movement_instruction(instruction)
            submarine.update_position(update_type, value)

        test_result = submarine.get_position()
        self.assertEqual(test_result, expected_result)

    def test_diagnostics(self):
        test_input = ['00100',
                      '11110',
                      '10110',
                      '10111',
                      '10101',
                      '01111',
                      '00111',
                      '11100',
                      '10000',
                      '11001',
                      '00010',
                      '01010']

        expected_gamma = '10110'
        expected_epsilon = '01001'
        expected_oxygen = '10111'
        expected_co2 = '01010'
        expected_result = (expected_gamma, expected_epsilon, expected_oxygen, expected_co2)

        submarine.read_diagnostics_report(test_input)
        test_result = submarine.process_diagnostics()

        self.assertEqual(test_result, expected_result)

    def test_bingo_sim(self):
        input_random_number_draw = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8,
                                    19, 3, 26, 1]
        expected_result = (4512, 1924)

        input_boards = {0: [[22, 13, 17, 11, 0],
                            [8, 2, 23, 4, 24],
                            [21, 9, 14, 16, 7],
                            [6, 10, 3, 18, 5],
                            [1, 12, 20, 15, 19], ],

                        1: [[3, 15, 0, 2, 22],
                            [9, 18, 13, 17, 5],
                            [19, 8, 7, 25, 23],
                            [20, 11, 10, 24, 4],
                            [14, 21, 16, 12, 6]],

                        2: [[14, 21, 17, 24, 4],
                            [10, 16, 15, 9, 19],
                            [18, 8, 23, 26, 20],
                            [22, 11, 13, 6, 5],
                            [2, 0, 12, 3, 7]]}

        win_info, loss_info = submarine.bingo_simulation(input_random_number_draw, input_boards)

        _, final_number_win, win_unmarked_sum = win_info
        _, final_number_lose, loss_unmarked_sum = loss_info

        test_result = (final_number_win * win_unmarked_sum, final_number_lose * loss_unmarked_sum)

        self.assertEqual(test_result, expected_result)

    def test_hydrothermal_lines(self):
        test_input = ['0,9 -> 5,9',
                        '8,0 -> 0,8',
                        '9,4 -> 3,4',
                        '2,2 -> 2,1',
                        '7,0 -> 7,4',
                        '6,4 -> 2,0',
                        '0,9 -> 2,9',
                        '3,4 -> 1,4',
                        '0,0 -> 8,8',
                        '5,5 -> 8,2']
        expected_result = (5, 12)

        lines = [sub_utils.convert_line_segemnt_str_to_line(x) for x in test_input]

        submarine.scan_hydrothermal_lines(lines)
        test_result_hz = submarine.determine_hydrothermal_danger_zones(only_hz=True)
        test_result_all = submarine.determine_hydrothermal_danger_zones(only_hz=False)

        self.assertEqual((test_result_hz, test_result_all), expected_result)

    def test_laternfish_sim(self):
        test_input = [3, 4, 3, 1, 2]
        expected_result = 26
        test_result = submarine.lanternfish_simulation(test_input, 18)
        self.assertEqual(test_result, expected_result)

    def test_day_7_treachery_of_whales(self):
        test_input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        expected_result = (37, 168)
        test_result_1 = submarine.determine_lowest_fuel_costs_to_align_crab_positions(test_input)
        test_result_2 = submarine.determine_lowest_fuel_costs_to_align_crab_positions(test_input, fuel_costs_non_linear=True)
        self.assertEqual((test_result_1, test_result_2), expected_result)

    def test_day_8_seven_segment_search(self):
        test_input = ['be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe',
                        'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc',
                        'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg',
                        'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb',
                        'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea',
                        'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb',
                        'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe',
                        'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef',
                        'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb',
                        'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce']

        submarine.parse__display_signals_to_signal_analyzer(test_input)
        submarine.run_display_signal_analysis()
        result = submarine._signal_analyzer.get_unique_pattern_count()

        out_signals = [t.split('|')[1] for t in test_input]
        test_result = submarine.count_digits_with_unique_signal_length(out_signals)

        self.assertEqual(test_result, 26)
