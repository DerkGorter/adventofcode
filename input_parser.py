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

    def parse_instructions(self, file_name):
        str_instructions = self.read_txt_file(file_name)
        return [self.convert_instruction(s) for s in str_instructions]

    @staticmethod
    def convert_instruction(instruction: str):
        if 'up' in instruction:
            x = int(instruction.replace('up ', ''))
            return 'aim', -x
        elif 'down' in instruction:
            x = int(instruction.replace('down ', ''))
            return 'aim', x
        elif 'forward' in instruction:
            x = int(instruction.replace('forward ', ''))
            return 'horizontal', x

    def read_bingo_input(self, file_name):
        raw_input = self.read_txt_file(file_name)
        random_number_draw_str = raw_input[0].split(sep=',')
        random_number_draw_int = [int(x) for x in random_number_draw_str]

        raw_boards = raw_input[1:len(raw_input)]

        boards = {}
        board = []
        b = 0
        for i in range(1, len(raw_boards)):
            str_values = raw_boards[i]

            if str_values != '':
                values = str_values.split(sep='  ')
                values = ' '.join(values)
                int_values = [int(x) for x in values.split(sep=' ')]
                board.append(int_values)
            else:
                boards[b] = board
                board = []
                b += 1
        boards[b] = board

        return random_number_draw_int, boards
