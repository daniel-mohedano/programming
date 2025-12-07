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
def day14_sim_sand(start_x, grid):
    correct = True
    x, y = start_x, 0

    while True:
        # Go down
        try:
            if not grid[y + 1, x]:
                y += 1
            elif not grid[y + 1, x - 1]:
                y += 1
                x -= 1
            elif not grid[y + 1, x + 1]:
                y += 1
                x += 1
            else:
                # Rest
                grid[y, x] = 1
                if y == 0:
                    correct = False
                break
        except:
            correct = False
            break

    return correct


def part1():
    rock_paths = [[(int(y.split(',')[0]), int(y.split(',')[1]))for y in x.replace('\n', '').split(' -> ')] for x in INPUT]
    max_x, min_x = 0, 500
    max_y = 0 

    # Search for min and max coordinates
    for rock in rock_paths:
        for line in rock:
            max_x = max(line[0], max_x)
            min_x = min(line[0], min_x)
            max_y = max(line[1], max_y)
    
    start_x = 500 - min_x
    grid = np.zeros([max_y + 1, max_x - min_x + 1])

    for rock in rock_paths:
        for i in range(len(rock) - 1):
            ini_x, ini_y = rock[i]
            end_x, end_y = rock[i + 1]
            range_x = range(ini_x, end_x + 1) if ini_x <= end_x else range(end_x, ini_x + 1)
            range_y = range(ini_y, end_y + 1) if ini_y <= end_y else range(end_y, ini_y + 1)

            for x in range_x:
                for y in range_y:
                    grid[y, x - min_x] = 1

    sand_grains = 0
    rest = True
    while rest:
        sand_grains += 1
        rest = day14_sim_sand(start_x, grid)

    return sand_grains - 1


def part2():
    rock_paths = [[(int(y.split(',')[0]), int(y.split(',')[1]))for y in x.replace('\n', '').split(' -> ')] for x in INPUT]
    max_x, min_x = 0, 500
    max_y = 0 

    # Search for min and max coordinates
    for rock in rock_paths:
        for line in rock:
            max_x = max(line[0], max_x)
            min_x = min(line[0], min_x)
            max_y = max(line[1], max_y)
    
    max_y += 2
    min_x = min_x - max_y
    max_x = max_x + max_y
    start_x = 500 - min_x
    grid = np.zeros([max_y + 1, max_x - min_x + 1])
    grid[-1, :] = 1

    for rock in rock_paths:
        for i in range(len(rock) - 1):
            ini_x, ini_y = rock[i]
            end_x, end_y = rock[i + 1]
            range_x = range(ini_x, end_x + 1) if ini_x <= end_x else range(end_x, ini_x + 1)
            range_y = range(ini_y, end_y + 1) if ini_y <= end_y else range(end_y, ini_y + 1)

            for x in range_x:
                for y in range_y:
                    grid[y, x - min_x] = 1
    

    sand_grains = 0
    rest = True
    while rest:
        sand_grains += 1
        rest = day14_sim_sand(start_x, grid)

    return sand_grains


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

