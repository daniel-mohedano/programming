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
def part1():
    moves = INPUT

    visited_positions = [[0, 0]]
    head = np.array([0, 0])
    tail = np.array([0, 0])

    dir_vecs = {'L': np.array([-1, 0]), 'R': np.array([1, 0]),
                'U': np.array([0, 1]), 'D': np.array([0, -1])}

    for move in moves:
        direction, count = move.split(" ")
        count = int(count)
        update = dir_vecs[direction]

        for _ in range(count):
            # Repeat move n times
            head += update

            # Check if tail needs repositioning
            if max(abs(head - tail)) > 1:
                # Check repositioning vector
                sign_vec = np.sign(head - tail)
                tail += sign_vec

                if list(tail) not in visited_positions:
                    visited_positions.append(list(tail))

    return len(visited_positions)


def part2():
    moves = INPUT

    visited_positions = [[0, 0]]
    knots = [np.array([0, 0]) for i in range(10)]

    dir_vecs = {'L': np.array([-1, 0]), 'R': np.array([1, 0]),
                'U': np.array([0, 1]), 'D': np.array([0, -1])}

    for move in moves:
        direction, count = move.split(" ")
        count = int(count)
        update = dir_vecs[direction]

        for _ in range(count):
            # Repeat move n times
            knots[0] += update

            # Check if tails need repositioning
            for i in range(9):
                head = knots[i]
                tail = knots[i + 1]
                if max(abs(head - tail)) > 1:
                    # Check repositioning vector
                    sign_vec = np.sign(head - tail)
                    tail += sign_vec

                    if i == 8 and list(tail) not in visited_positions:
                        visited_positions.append(list(tail))

    return len(visited_positions)


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

