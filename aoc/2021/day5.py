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
    data = INPUT
        
    grid = np.zeros([1000, 1000])
    overlaps = 0

    for line in data:
        p1, p2 = line.split(' -> ')
        p1 = [int(x) for x in p1.split(',')]
        p2 = [int(x) for x in p2.split(',')]

        # Ignore diagonal lines
        if p1[0] != p2[0] and p1[1] != p2[1]:
            continue

        for i in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
            for j in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                if grid[i][j] == 1:
                    overlaps += 1
                grid[i][j] += 1

    return overlaps


def part2():
    data = INPUT

    grid = np.zeros([1000, 1000])
    overlaps = 0

    for line in data:
        p1, p2 = line.split(' -> ')
        p1 = [int(x) for x in p1.split(',')]
        p2 = [int(x) for x in p2.split(',')]

        n_points = max(abs(p1[0] - p2[0]) + 1, abs(p1[1] - p2[1]) + 1)
        sign_x = np.sign(p2[0] - p1[0])
        sign_y = np.sign(p2[1] - p1[1])
        if sign_x == 0:
            sign_x = 1
        if sign_y == 0:
            sign_y = 1
        x_points = list(range(p1[0], p2[0] + sign_x, sign_x))
        y_points = list(range(p1[1], p2[1] + sign_y, sign_y))

        if len(x_points) == 1:
            x_points *= n_points
        if len(y_points) == 1:
            y_points *= n_points

        for i, j in zip(x_points, y_points):
            if grid[j][i] == 1:
                overlaps += 1
            grid[j][i] += 1

    return overlaps


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

