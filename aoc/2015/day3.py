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
    if len(lines) == 2 and not lines[1]:
        INPUT = lines[0]
    else:
        INPUT = lines[:-1]
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
    line = INPUT

    houses = set()
    pos = (0, 0)
    houses.add(pos)

    for c in line:
        new_pos = [pos[0], pos[1]]
        if c == '>':
            new_pos[0] += 1
        elif c == '<':
            new_pos[0] -= 1
        elif c == 'v':
            new_pos[1] += 1
        else:
            new_pos[1] -= 1

        pos = tuple(new_pos)
        houses.add(pos)

    return len(houses)


def part2():
    line = INPUT

    houses = set()
    pos = [(0, 0), (0, 0)]
    santa = 0
    houses.add(pos[0])

    for c in line:
        new_pos = [pos[santa][0], pos[santa][1]]
        if c == '>':
            new_pos[0] += 1
        elif c == '<':
            new_pos[0] -= 1
        elif c == 'v':
            new_pos[1] += 1
        else:
            new_pos[1] -= 1

        pos[santa] = tuple(new_pos)
        houses.add(pos[santa])
        santa = (santa + 1) % 2

    return len(houses)


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

