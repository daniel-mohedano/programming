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
def get_dir(tree, dirs):
    final_dir = tree["/"]["content"]
    for d in dirs:
        final_dir = final_dir[d]["content"]

    return final_dir


def add_dir(tree, pwd, new_dir):
    parent = get_dir(tree, pwd)
    parent[new_dir] = {"content": {}, "size": 0}


def add_file(tree, pwd, size, name):
    parent = get_dir(tree, pwd)
    parent[name] = {"size": size}


def calc_sizes_recursive(current_dir):
    for ele in current_dir["content"]:
        if "content" in current_dir["content"][ele]:
            # Recursively go into sub-dir
            current_dir["size"] += calc_sizes_recursive(current_dir["content"][ele])
        else:
            # If file, just update size
            current_dir["size"] += current_dir["content"][ele]["size"]

    return current_dir["size"]


def calc_sizes(tree):
    tree["/"]["size"] = calc_sizes_recursive(tree["/"])


def find_limited_dirs_max(current_dir, max_size):
    sizes = []
    if current_dir["size"] <= max_size:
        sizes.append(current_dir["size"])

    # Iterate through contained dirs
    for ele in current_dir["content"]:
        if "content" in current_dir["content"][ele]:
            # If sub-dir, check size
            sizes += find_limited_dirs_max(current_dir["content"][ele], max_size)

    return sizes


def find_limited_dirs_min(current_dir, min_size):
    sizes = []
    if current_dir["size"] >= min_size:
        sizes.append(current_dir["size"])

    # Iterate through contained dirs
    for ele in current_dir["content"]:
        if "content" in current_dir["content"][ele]:
            # If sub-dir, check size
            sizes += find_limited_dirs_min(current_dir["content"][ele], min_size)

    return sizes


def part1():
    commands = INPUT
    # Tree definition: {'dir_name': {'content': {'dir_name': ...}, 'size': x}
    # File definition: 'file_name': {'size': x}

    global_tree = {"/": {"content": {}, "size": 0}}
    path = []

    # Build directory tree
    for c in commands:
        tokens = c.split(" ")
        if tokens[0] == "$":
            # Shell command
            if tokens[1] == "cd":
                # cd command
                new_dir = tokens[2]
                if new_dir == "/":
                    path = []
                elif new_dir == "..":
                    path = path[:-1]
                elif new_dir not in path:
                    add_dir(global_tree, path, new_dir)
                    path.append(new_dir)
                else:
                    path.append(new_dir)
            else:
                # ls command does nothing
                continue
        elif tokens[0] == "dir":
            # Directory definition
            new_dir = tokens[1]
            add_dir(global_tree, path, new_dir)
        else:
            # File definition
            add_file(global_tree, path, int(tokens[0]), tokens[1])

    calc_sizes(global_tree)
    sizes = find_limited_dirs_max(global_tree["/"], 100000)
    return sum(sizes)


def part2():
    commands = INPUT
    # Tree definition: {'dir_name': {'content': {'dir_name': ...}, 'size': x}
    # File definition: 'file_name': {'size': x}

    global_tree = {"/": {"content": {}, "size": 0}}
    path = []

    # Build directory tree
    for c in commands:
        tokens = c.split(" ")
        if tokens[0] == "$":
            # Shell command
            if tokens[1] == "cd":
                # cd command
                new_dir = tokens[2]
                if new_dir == "/":
                    path = []
                elif new_dir == "..":
                    path = path[:-1]
                elif new_dir not in path:
                    add_dir(global_tree, path, new_dir)
                    path.append(new_dir)
                else:
                    path.append(new_dir)
            else:
                # ls command does nothing
                continue
        elif tokens[0] == "dir":
            # Directory definition
            new_dir = tokens[1]
            add_dir(global_tree, path, new_dir)
        else:
            # File definition
            add_file(global_tree, path, int(tokens[0]), tokens[1])

    calc_sizes(global_tree)
    needed_space = 30000000
    free_space = 70000000 - global_tree["/"]["size"]
    sizes = find_limited_dirs_min(global_tree["/"], needed_space - free_space)
    return min(sizes)


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

