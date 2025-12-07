import numpy as np
import requests
import argparse
from pathlib import Path
import time


# ADVENT OF CODE VARIABLES
AOC_YEAR = int(Path(__file__).resolve().parents[0].stem)
AOC_DAY = int(Path(__file__).resolve().stem.replace('day', ''))
TEST_MODE = False
INPUT = None
TEST_INPUT = """"""

# AUX_FUNCTIONS
def aoc_input():
    global INPUT
    if TEST_MODE:
        text = TEST_INPUT
    else:        
        with open(Path(__file__).resolve().parents[1] / 'TOKEN', 'r') as f:
            token = f.read().replace('\n', '')

        r = requests.get(f'https://adventofcode.com/{AOC_YEAR}/day/{AOC_DAY}/input',
                         cookies={'session': token},
                         headers={'User-Agent': 'danmohedano'})
        if r.status_code != 200:
            print(f'Invalid response status code, got {r.status_code}. Check session token.')
            return False

        text = r.text

    lines = text.split('\n')
    INPUT = lines[:-1] if len(lines) > 1 else lines[0]
    return True


def main():
    # Obtain desired input
    if not aoc_input():
        return

    # Execute solution for part 1
    t1 = time.perf_counter()
    sol1 = part1()
    t1 = time.perf_counter() - t1
    print(f'AOC {AOC_YEAR} Day {AOC_DAY} Part 1: {sol1}')
    print(f'Execution time: {t1:.6f}')

    # Execute solution for part 2
    t2 = time.perf_counter()
    sol2 = part2()
    t2 = time.perf_counter() - t2
    print(f'AOC {AOC_YEAR} Day {AOC_DAY} Part 2: {sol2}')
    print(f'Execution time: {t2:.6f}')


# SOLUTIONS
def _check_bingo(table, row, col):
    flag_col, flag_row = True, True

    # Check all rows of col
    for i in range(table.shape[0]):
        if table[i][col] == 0:
            flag_col = False

    # Check all columns in row
    for j in range(table.shape[1]):
        if table[row][j] == 0:
            flag_row = False

    return flag_col or flag_row


def _sum_unmarked(table, table_marks):
    sum = 0
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            if table_marks[i][j] == 0:
                sum += table[i][j]

    return sum


def part1():
    data = INPUT
        
    # Random numbers
    order = [int(n) for n in data[0].split(',')]
    
    # Load boards
    boards = []
    board_dicts = []
    board_marks = []

    for b_i in range(2, len(data), 6):
        board = np.zeros([5, 5])
        board_mark = np.zeros([5, 5])
        board_dict = {}

        for row_i, row in enumerate(data[b_i:b_i + 6]):
            for col_i, ele in enumerate(row.replace('\n', '').split()):
                board[row_i][col_i] = int(ele)
                board_dict[int(ele)] = (row_i, col_i)

        boards.append(board)
        board_dicts.append(board_dict)
        board_marks.append(board_mark)

    # Iterate through numbers
    for n in order:
        # Iterate through boards
        for b, b_dict, b_mark in zip(boards, board_dicts, board_marks):
            # If number in bingo card
            if n in b_dict:
                pos_x, pos_y = b_dict[n]
                b_mark[pos_x][pos_y] = 1
                if _check_bingo(b_mark, pos_x, pos_y):
                    return int(_sum_unmarked(b, b_mark) * n)

    return None


def part2():
    data = INPUT
        
    # Random numbers
    order = [int(n) for n in data[0].split(',')]
    
    # Load boards
    boards = []
    board_dicts = []
    board_marks = []

    for b_i in range(2, len(data), 6):
        board = np.zeros([5, 5])
        board_mark = np.zeros([5, 5])
        board_dict = {}

        for row_i, row in enumerate(data[b_i:b_i + 6]):
            for col_i, ele in enumerate(row.replace('\n', '').split()):
                board[row_i][col_i] = int(ele)
                board_dict[int(ele)] = (row_i, col_i)

        boards.append(board)
        board_dicts.append(board_dict)
        board_marks.append(board_mark)

    # Iterate through numbers
    won_boards = []
    total_boards = len(boards)
    for n in order:
        # Iterate through boards
        for b_i, (b, b_dict, b_mark) in enumerate(zip(boards, board_dicts, board_marks)):
            # If number in bingo card
            if n in b_dict:
                pos_x, pos_y = b_dict[n]
                b_mark[pos_x][pos_y] = 1
                if _check_bingo(b_mark, pos_x, pos_y) and b_i not in won_boards:
                    won_boards.append(b_i)

                if len(won_boards) == total_boards:
                    return int(n * _sum_unmarked(b, b_mark))

    return None


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

