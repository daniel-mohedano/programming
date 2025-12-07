import numpy as np
import requests
import argparse
from pathlib import Path
import time
import functools


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
def day13_compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left == right: 
            return 0
        else:
            return -1
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))): 
            res = day13_compare(left[i], right[i])
            if res == 0:
                continue
            else: 
                return res

        if len(left) < len(right):
            return 1
        elif len(left) == len(right):
            return 0
        else:
            return -1
    else:
        if isinstance(left, int): 
            return day13_compare([left], right)
        else:
            return day13_compare(left, [right])


def part1():
    lines = INPUT
    correct_order = 0

    for i in range((len(lines) + 1) // 3):
        left = eval(lines[3 * i].replace('\n', ''))
        right = eval(lines[3 * i + 1].replace('\n', ''))

        if day13_compare(left, right) == 1:
            correct_order += (i + 1)

    return correct_order


def part2():
    lines = INPUT
    packets = []
    packets.append([[2]])
    packets.append([[6]])

    for l in lines:
        if l:
            packets.append(eval(l))

    sorted_packets = sorted(packets, reverse=True, key=functools.cmp_to_key(day13_compare))

    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

