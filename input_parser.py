import sub_utils


class InputParser:
    input_file_path = None

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path

    def read_txt_file(self, file_name):
        file = self.input_file_path + file_name

        with open(file) as f:
            lines = f.readlines()

        lines = [l.strip() for l in lines]
        return lines

    def parse_int_list_from_txt(self, file_name):
        str_list = self.read_txt_file(file_name)
        int_list = [int(s) for s in str_list]
        return int_list

    def parse_movement_instructions(self, file_name):
        str_instructions = self.read_txt_file(file_name)
        return [sub_utils.convert_movement_instruction(s) for s in str_instructions]

    def read_bingo_input(self, file_name):
        raw_input = self.read_txt_file(file_name)

        # read the random number draw from the first line
        random_number_draw_str = raw_input[0].split(sep=',')
        random_number_draw_int = [int(x) for x in random_number_draw_str]

        # select bingo board lines and initialize output container
        raw_boards = raw_input[1:len(raw_input)]
        boards = {}

        # read bingo boards separated by empty lines
        board = []
        b = 0
        for i in range(1, len(raw_boards)):
            str_values = raw_boards[i]
            if str_values != '':
                int_values = self.separate_bingo_board_into_int_array(str_values)
                board.append(int_values)
            else:
                boards[b] = board
                board = []
                b += 1
        # add last board, since the input file does not have an empty line at the end
        boards[b] = board

        return random_number_draw_int, boards

    @staticmethod
    def separate_bingo_board_into_int_array(str_values):
        # The bingo board contains two seperators, a space and a double space
        # first replace the double space with one space, then split and cast to int
        values = str_values.split(sep='  ')
        values = ' '.join(values)
        int_values = [int(x) for x in values.split(sep=' ')]
        return int_values

    def parse_line_segments(self, file_name):
        raw_line_segments = self.read_txt_file(file_name)
        return [sub_utils.convert_line_segemnt_str_to_line(x) for x in raw_line_segments]
