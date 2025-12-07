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
    arrangement = INPUT
    n_stacks = 0

    # Read number of stacks
    for l in arrangement:
        if "[" not in l:
            no_space = " ".join(l.split())
            n_stacks = max([int(x) for x in no_space.split(" ")])
            break

    stacks = [[] for i in range(n_stacks)]

    # Read stacks
    for l in arrangement:
        if "[" not in l:
            break

        for i in range(n_stacks):
            # Read crate of each stack (if there is one)
            if l[i * 4] == "[":
                stacks[i].insert(0, l[i * 4 + 1])

    # Read instructions
    for l in arrangement:
        if "move" in l:
            n_moved, origin, dest = [
                int(x)
                for x in l.replace(" ", "")
                .replace("move", "")
                .replace("from", ",")
                .replace("to", ",")
                .split(",")
            ]
            # Correct indices
            origin -= 1
            dest -= 1
            # Move crates from origin to destination
            stacks[dest] += reversed(
                stacks[origin][len(stacks[origin]) - n_moved :]
            )
            stacks[origin] = stacks[origin][: len(stacks[origin]) - n_moved]

    top_stacks = ""
    for s in stacks:
        if len(s) > 0:
            top_stacks += s[-1]

    return top_stacks


def part2():
    arrangement = INPUT
    n_stacks = 0

    # Read number of stacks
    for l in arrangement:
        if "[" not in l:
            no_space = " ".join(l.split())
            n_stacks = max([int(x) for x in no_space.split(" ")])
            break

    stacks = [[] for i in range(n_stacks)]

    # Read stacks
    for l in arrangement:
        if "[" not in l:
            break

        for i in range(n_stacks):
            # Read crate of each stack (if there is one)
            if l[i * 4] == "[":
                stacks[i].insert(0, l[i * 4 + 1])

    # Read instructions
    for l in arrangement:
        if "move" in l:
            n_moved, origin, dest = [
                int(x)
                for x in l.replace(" ", "")
                .replace("move", "")
                .replace("from", ",")
                .replace("to", ",")
                .split(",")
            ]
            # Correct indices
            origin -= 1
            dest -= 1
            # Move crates from origin to destination
            stacks[dest] += stacks[origin][len(stacks[origin]) - n_moved:]
            stacks[origin] = stacks[origin][: len(stacks[origin]) - n_moved]

    top_stacks = ""
    for s in stacks:
        if len(s) > 0:
            top_stacks += s[-1]

    return top_stacks


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

