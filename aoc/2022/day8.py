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
def trees_seen(los, tree):
    seen = 0
    for i in range(len(los)):
        seen += 1
        if los[i] >= tree:
            break

    return seen


def part1():
    trees = INPUT
    trees = np.array([[int(t) for t in x] for x in trees])
    grid = np.zeros(trees.shape)
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1

    # Iterate through all trees to check
    for i in range(1, trees.shape[0] - 1):
        for j in range(1, trees.shape[1] - 1):
            tree = trees[i][j]
            if (
                max(trees[i, j + 1:]) < tree
                or max(trees[i, :j]) < tree
                or max(trees[:i, j]) < tree
                or max(trees[i + 1:, j]) < tree
            ):
                grid[i, j] = 1

    return int(np.sum(grid))


def part2():
    trees = INPUT
    trees = np.array([[int(t) for t in x] for x in trees])
    grid = np.zeros(trees.shape)

    # Iterate through all trees to check
    for i in range(1, trees.shape[0] - 1):
        for j in range(1, trees.shape[1] - 1):
            tree = trees[i][j]
            score_up = trees_seen(np.flip(trees[:i, j]), tree)
            score_down = trees_seen(trees[i + 1:, j], tree)
            score_right = trees_seen(trees[i, j + 1:], tree)
            score_left = trees_seen(np.flip(trees[i, :j]), tree)
            grid[i][j] = score_up * score_down * score_right * score_left

    return int(np.max(grid))


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

