import pandas as pd


class BingoSimulator:
    _random_number_draw = None
    _bingo_boards = None
    _bingo_check_boards = None
    _boards_with_bingo = []
    _win_order_dict = {}

    def __init__(self, random_number_draw: list, bingo_boards: dict) -> None:
        self._random_number_draw = random_number_draw
        self._bingo_boards = [pd.DataFrame(x) for x in bingo_boards.values()]
        self._bingo_check_boards = [x.applymap(lambda x: int(0)) for x in self._bingo_boards]

    def run(self) -> None:
        # win number to keep track of when a bingo board wins
        win_number = 0

        # call out numbers from the random number draw
        for number in self._random_number_draw:

            # mark the called out number on each board
            for board_i in range(0, len(self._bingo_boards)):

                # skip boards that have bingo
                if self.board_has_bingo(board_i):
                    continue

                # get current board and the corresponding marked numbers
                board = self._bingo_boards[board_i]
                bingo_check_board = self._bingo_check_boards[board_i]

                # check if the called out number is on the bingo board, and mark the number
                number_check = board.isin([number]).applymap(lambda x: int(x))
                self._bingo_check_boards[board_i] = bingo_check_board + number_check

                # determine the column and row sum of the markings
                sum_rows = self._bingo_check_boards[board_i].sum(axis=0)
                sum_cols = self._bingo_check_boards[board_i].sum(axis=1)

                # if a row sum or column sum equals five, the board has bingo
                if (5 in sum_rows.values) or (5 in sum_cols.values):
                    self._win_order_dict[win_number] = (board_i, number)
                    self._boards_with_bingo.append(board_i)
                    win_number += 1

    def board_has_bingo(self, board_i: int) -> bool:
        return board_i in self._boards_with_bingo

    def get_win_order(self) -> dict:
        return self._win_order_dict

    def get_bingo_board(self, board_num: int) -> pd.DataFrame:
        return self._bingo_boards[board_num]

    def get_unmarked_number_sum(self, board_num: int) -> int:
        bingo_board = self._bingo_boards[board_num]
        marked_numbers_int = self._bingo_check_boards[board_num]

        marked_numbers_int = marked_numbers_int.applymap(lambda x: not bool(x))

        unmarked_sum = 0
        for i in range(0, len(bingo_board)):
            unmarked_sum += bingo_board[i][marked_numbers_int[i]].sum()

        return unmarked_sum
