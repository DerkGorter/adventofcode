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
