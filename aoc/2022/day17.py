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
TEST_INPUT = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

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
class Grid:
    def __init__(self, width):
        self.blocks = set()
        self.width = width
        self.height = 0

    def add(self, rock):
        # Add rock to grid
        self.blocks.update(rock)
        # Update height of grid
        for _, y in rock:
            self.height = max(self.height, y + 1)
        
    def collision(self, rock):
        # Check collision with other rocks
        if self.blocks.intersection(set(rock)):
            return True
        # Check collision with width and bottom limits
        for x, y in rock:
            if x < 0 or x >= self.width or y < 0:
                return True

        return False


def grid_to_string(grid, rock):
    max_i = grid.width
    max_rock = 0
    for p in rock:
        max_rock = max(max_rock, p[1])
    max_j = max(max_rock, grid.height)
    string = '=======\n'
    for j in range(max_j, -1, -1):
        for i in range(max_i):
            if (i, j) in grid.blocks or (i, j) in rock:
                string += '#'
            else:
                string += '.'

        string += '\n'

    return string


def move(rock, jet=None):
    if not jet:
        vec = [0, -1]
    else:
        vec = [1, 0] if jet == '>' else [-1, 0]
    new_rock = [(p[0] + vec[0], p[1] + vec[1]) for p in rock]
    return new_rock 


def hash_grid(grid, rock_idx, rocks, jet_idx, jets, height_lim=None):
    grid_hash = 0b0
    if not height_lim:
        height_lim = grid.height

    # Only look at height_lim top rows of the grid to look for collisions
    correction = max(grid.height - height_lim, 0)

    for b in grid.blocks:
        if b[1] >= correction:
            bit_pos = b[0] + (b[1] - correction) * grid.width
            grid_hash = grid_hash | 1 << bit_pos

    rock_bits = int(np.ceil(np.log2(len(rocks) + 1)))
    rock_hash = (rock_idx % len(rocks))

    jet_bits = int(np.ceil(np.log2(len(jets) + 1)))
    jet_hash = (jet_idx % len(jets))
    
    hash = grid_hash << (jet_bits + rock_bits) | rock_hash << jet_bits | jet_hash
    return hash


def simulate_fall(iterations, jets, hash=False):
    rocks = [
        [[0, 0], [1, 0], [2, 0], [3, 0]], 
        [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]], 
        [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], 
        [[0, 0], [0, 1], [0, 2], [0, 3]], 
        [[0, 0], [1, 0], [0, 1], [1, 1]],
    ] 
    grid = Grid(width=7)
    jet_idx = 0 
    hash_dict = {}
    hash_pos = {}

    for rock_idx in range(iterations):
        rock = rocks[rock_idx % len(rocks)].copy()
        height = grid.height
        # Move rock to starting position
        rock = [(p[0] + 2, p[1] + height + 3) for p in rock]

        # Drop rock until no move possible
        while True:
            # Move with jet
            new_rock = move(rock, jets[jet_idx % len(jets)])
            jet_idx += 1
            if not grid.collision(new_rock):
                rock = new_rock

            # Drop one position
            new_rock = move(rock)
            if grid.collision(new_rock):
                grid.add(rock)
                break

            rock = new_rock

        if hash:
            hash_val = hash_grid(grid, rock_idx, rocks, jet_idx, jets, 21)
            if hash_val in hash_dict:
                # Position variables 
                loop_start = hash_pos[hash_val]
                loop_end = rock_idx
                loop_len = loop_end - loop_start
                n_loops = (iterations - 1 - loop_start) // loop_len
                offset = (iterations - 1 - loop_start) % loop_len
                offset_hash = list(hash_pos.keys())[list(hash_pos.values()).index(loop_start + offset)] 
                # Height variables
                height_per_loop = grid.height - hash_dict[hash_val]
                offset_height = hash_dict[offset_hash] - hash_dict[hash_val] 
                # Compute final height after all loops
                final_height = hash_dict[hash_val]  # Starting height of loop
                final_height += (height_per_loop * n_loops)  # Height gain per loop
                final_height += offset_height  # Height gain in offset at the end
                grid.height = final_height
                break

            hash_dict[hash_val] = grid.height
            hash_pos[hash_val] = rock_idx

    return grid


def part1():
    jets = INPUT

    # Simulate fall
    grid = simulate_fall(2022, jets)
    return grid.height

def part2():
    jets = INPUT

    # Simulate fall
    grid = simulate_fall(1000000000000, jets, hash=True)
    return grid.height

if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

