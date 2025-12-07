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
def _infer_digit(a, cf, bd, digit):
    length = len(digit)
    if length == 2:
        return "1"
    elif length == 3:
        return "7"
    elif length == 4:
        return "4"
    elif length == 7:
        return "8"

    if length == 6:
        # 0, 6, 9
        if bd[0] not in digit or bd[1] not in digit:
            return "0"
        elif cf[0] not in digit or cf[1] not in digit:
            return "6"
        else:
            return "9"
    else:
        # 2, 3, 5
        if bd[0] in digit and bd[1] in digit:
            return "5"
        elif cf[0] in digit and cf[1] in digit:
            return "3"
        else:
            return "2"

            
def part1():
    data = INPUT
    """
    0 - 6 : abcefg
    1 - 2 : cf (unique)
    2 - 5 : acdeg
    3 - 5 : acdfg
    4 - 4 : bcdf (unique)
    5 - 5 : abdfg
    6 - 6 : abdefg
    7 - 3 : acf (unique)
    8 - 7 : abcdefg (unique)
    9 - 6 : abcdfg
    """
    appearances = 0
    for line in data:
        patterns, output = line.split(' | ')
        for n in output.split(' '):
            if len(n) in [2, 4, 3, 7]:
                appearances += 1

    return appearances


def part2():
    data = INPUT
    """
    0 - 6 : abcefg
    1 - 2 : cf (unique)
    2 - 5 : acdeg
    3 - 5 : acdfg
    4 - 4 : bcdf (unique)
    5 - 5 : abdfg
    6 - 6 : abdefg
    7 - 3 : acf (unique)
    8 - 7 : abcdefg (unique)
    9 - 6 : abcdfg
    """
    sum_outputs = 0
    for line in data:
        patterns, output = line.split(' | ')
        output_value = []

        patterns_dict = {i: [] for i in [2, 3, 4, 5, 6, 7]}

        for p in patterns.split(' '):
            patterns_dict[len(p)].append(p)

        a = [x for x in patterns_dict[3][0] if x not in patterns_dict[2][0]]
        cf = [x for x in patterns_dict[2][0]]
        bd = [x for x in patterns_dict[4][0] if x not in patterns_dict[2][0]]

        for out in output.split(' '):
            output_value.append(_infer_digit(a, cf, bd, out))

        sum_outputs += int(''.join(output_value))

    return sum_outputs


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

