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
    # Rock-paper-scissors symbols
    rps = ["A", "B", "C"]
    xyz = ["X", "Y", "Z"]
    rps_points = {"X": 1, "Y": 2, "Z": 3}

    # Head to head point calculation
    points = [3, 0, 6]
    h2h = {
        xyz[i]: {rps[(j + i) % 3]: points[j] for j in range(3)}
        for i in range(3)
    }

    # Total score
    score = 0
    matches = INPUT

    for m in matches:
        # Obtain opponent's and our decision
        op, dec = m.split(' ')
        score += h2h[dec][op] + rps_points[dec]

    return score


def part2():
    # Rock-paper-scissors symbols
    rps = ["A", "B", "C"]
    xyz = ["X", "Y", "Z"]
    rps_points = {"X": 1, "Y": 2, "Z": 3}

    # Head to head decision depending on result
    res_points = {"X": 0, "Y": 3, "Z": 6}
    h2h = {
        rps[i]: {xyz[j]: xyz[(j + i + 2) % 3] for j in range(3)} for i in range(3)
    }

    # Total score
    score = 0
    matches = INPUT
    
    for m in matches:
        # Obtain opponent decision and result
        op, res = m.split(" ")
        dec = h2h[op][res]
        score += res_points[res] + rps_points[dec]

    return score


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

