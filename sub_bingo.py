import pandas as pd


class BingoSimulator:
    random_number_draw = None
    bingo_boards = None
    bingo_check_boards = None

    def __init__(self, random_number_draw, bingo_boards):
        self.random_number_draw = random_number_draw

        bingo_boards = [pd.DataFrame(x) for x in bingo_boards.values()]
        bingo_check_boards = [x.applymap(lambda x: int(0)) for x in bingo_boards]

        self.bingo_boards = bingo_boards
        self.bingo_check_boards = bingo_check_boards

    def run(self):
        win_order_dict = {}
        win_number = 0
        for number in self.random_number_draw:
            for board_i in range(0, len(self.bingo_boards)):

                boards_already_won = [tp[0] for tp in win_order_dict.values()]
                if board_i in boards_already_won:
                    continue

                board = self.bingo_boards[board_i]
                bingo_check_board = self.bingo_check_boards[board_i]

                number_check_df = board.isin([number]).applymap(lambda x: int(x))
                self.bingo_check_boards[board_i] = bingo_check_board + number_check_df

                sum_rows = self.bingo_check_boards[board_i].sum(axis=0)
                sum_cols = self.bingo_check_boards[board_i].sum(axis=1)

                if (5 in sum_rows.values) or (5 in sum_cols.values):
                    win_order_dict[win_number] = (board_i, number)
                    win_number += 1

        return win_order_dict

    def get_unmarked_number_sum(self, board_num):
        winning_board = self.bingo_boards[board_num]
        win_marked_numbers_int = self.bingo_check_boards[board_num]

        win_marked_numbers_int = win_marked_numbers_int.applymap(lambda x: not bool(x))

        unmarked_sum = 0
        for i in range(0, len(winning_board)):
            unmarked_sum += winning_board[i][win_marked_numbers_int[i]].sum()

        return unmarked_sum
