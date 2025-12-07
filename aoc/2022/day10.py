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
    instructions = INPUT
    reg = 1
    cycle = 1
    signal_strength = 0

    def check_cycle(cycle, reg):
        if (cycle - 20) % 40 == 0:
            return reg * cycle

        return 0

    for inst in instructions:
        if inst == 'noop':
            signal_strength += check_cycle(cycle, reg)
            cycle += 1
        else:
            value = int(inst.split(" ")[1])
            signal_strength += check_cycle(cycle, reg)
            cycle += 1
            signal_strength += check_cycle(cycle, reg)
            cycle += 1
            reg += value

    return signal_strength


def part2():
    instructions = INPUT
    reg = 1
    cycle = 0

    def draw_crt(reg, cycle):
        print_pos = cycle % 40
        if print_pos == 0:
            print('\n', end='')
        if reg - 1 <= print_pos <= reg + 1:
            print('#', end='')
        else:
            print('.', end='')

    for inst in instructions:
        if inst == 'noop':
            draw_crt(reg, cycle)
            cycle += 1
        else:
            value = int(inst.split(" ")[1])
            draw_crt(reg, cycle)
            cycle += 1
            draw_crt(reg, cycle)
            cycle += 1
            reg += value

    print('\n', end='')
    return 0


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()
