import numpy as np
import requests
import argparse
from pathlib import Path
import time
import queue


# ADVENT OF CODE VARIABLES
AOC_YEAR = int(Path(__file__).resolve().parents[0].stem)
AOC_DAY = int(Path(__file__).resolve().stem.replace('day', ''))
TEST_MODE = False
INPUT = None
TEST_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

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
    if len(lines) == 2 and not lines[1] or len(lines) == 1:
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
def valid(x, y, z, grid):
    for c, max in zip([x, y, z], grid.shape):
        if c < 0 or c >= max:
            return False

    return True


def neighbours(x, y, z, grid):
    counter = 0
    possible = [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z),
                (x, y, z - 1), (x, y, z + 1)]
    for i, j, k in possible:
        if valid(i, j, k, grid) and grid[i, j, k] != 0:
            counter += 1

    return counter

    
def surface_area(coords):
    max_x, max_y, max_z = 0, 0, 0
    for x, y, z in coords:
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)
        max_z = max(max_z, z + 1)
        
    grid = np.zeros([max_x, max_y, max_z])
    area = 0
    for x, y, z in coords:
        grid[x, y, z] = 1
        area += (6 - 2 * (neighbours(x, y, z, grid)))
        
    return area, grid


def part1():
    coords = INPUT
    parsed_coords = []
    max_x, max_y, max_z = 0, 0, 0
    for c in coords: 
        x, y, z = [int(s) for s in c.split(',')] 
        parsed_coords.append((x, y, z))
        max_x = max(max_x, x + 1)
        max_y = max(max_y, y + 1)
        max_z = max(max_z, z + 1)
        
    grid = np.zeros([max_x, max_y, max_z])
    area = 0
    for x, y, z in parsed_coords:
        grid[x, y, z] = 1
        area += (6 - 2 * (neighbours(x, y, z, grid)))
    
    return area


def traversal(x, y, z, grid, visited, counter):
    # Stopping check: out of bounds or block encountered
    if not valid(x, y, z, grid):
        return visited, counter
    elif grid[x, y, z] != 0:
        counter += 1
        return visited, counter

    # Search for neighbours 
    visited.add((x, y, z))
    possible = [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z),
                (x, y, z - 1), (x, y, z + 1)]

    for i, j, k in possible:
        if (i, j, k) not in visited:
            visited, counter = traversal(i, j, k, grid, visited, counter) 
            
    return visited, counter


def part2():
    coords = INPUT
    parsed_coords = []
    max_x, max_y, max_z = 0, 0, 0
    for c in coords: 
        x, y, z = [int(s) for s in c.split(',')] 
        # Modify coords to always leave one empty layer around 
        parsed_coords.append((x + 1, y + 1, z + 1))
        max_x = max(max_x, x + 3)
        max_y = max(max_y, y + 3)
        max_z = max(max_z, z + 3)
        
    grid = np.zeros([max_x, max_y, max_z])
    for x, y, z in parsed_coords:
        grid[x, y, z] = 1    

    # Starting from an empty corner, traverse all reachable blocks
    visited = set()
    pending = queue.Queue()
    pending.put((0, 0, 0))
    area = 0

    while not pending.empty():
        # Get next visited position
        x, y, z = pending.get() 

        # Stopping check: out of bounds, already visited or block encountered
        if not valid(x, y, z, grid) or (x, y, z) in visited:
            continue
        elif grid[x, y, z] != 0:
            area += 1
            continue

        # Search for neighbours 
        visited.add((x, y, z))
        possible = [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z),
                    (x, y, z - 1), (x, y, z + 1)]

        for pos in possible:
            pending.put(pos)
                    
    return area


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

