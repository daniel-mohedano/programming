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
    monkey_desc = INPUT

    class Monkey:
        def __init__(self):
            self.items = []
            self.operation = ""
            self.test = 0
            self.dest_true = 0
            self.dest_false = 0
            self.inspected = 0

    l_read = 0
    monkeys = []

    # Read monkey descriptions
    while l_read < len(monkey_desc):
        monkey = Monkey()
        items = monkey_desc[l_read + 1].replace('\n', '').split(':')[1].split(',')
        monkey.items = [int(x) for x in items]
        monkey.operation = monkey_desc[l_read + 2].replace('\n', '').split(':')[1].split('=')[1]
        monkey.test = int(monkey_desc[l_read + 3].replace('\n', '').split(':')[1].split(' ')[3])
        monkey.dest_true = int(monkey_desc[l_read + 4].replace('\n', '').split(':')[1].split(' ')[4])
        monkey.dest_false = int(monkey_desc[l_read + 5].replace('\n', '').split(':')[1].split(' ')[4])

        l_read += 7
        monkeys.append(monkey)

    # Rounds
    for _ in range(20):
        for m_idx in range(len(monkeys)):
            m = monkeys[m_idx]
            for old in m.items:
                m.inspected += 1
                new = eval(m.operation)
                new = new // 3
                if new % m.test == 0:
                    monkeys[m.dest_true].items.append(new)
                else:
                    monkeys[m.dest_false].items.append(new)
                
            # Remove items from monkey
            m.items = []

    inspected = sorted([m.inspected for m in monkeys])
    
    return inspected[-1] * inspected[-2]


def part2():
    monkey_desc = INPUT

    class Monkey:
        def __init__(self):
            self.items = []
            self.operation = ""
            self.test = 0
            self.dest_true = 0
            self.dest_false = 0
            self.inspected = 0

    l_read = 0
    monkeys = []

    # Read monkey descriptions
    while l_read < len(monkey_desc):
        monkey = Monkey()
        items = monkey_desc[l_read + 1].replace('\n', '').split(':')[1].split(',')
        monkey.items = [int(x) for x in items]
        monkey.operation = monkey_desc[l_read + 2].replace('\n', '').split(':')[1].split('=')[1]
        monkey.test = int(monkey_desc[l_read + 3].replace('\n', '').split(':')[1].split(' ')[3])
        monkey.dest_true = int(monkey_desc[l_read + 4].replace('\n', '').split(':')[1].split(' ')[4])
        monkey.dest_false = int(monkey_desc[l_read + 5].replace('\n', '').split(':')[1].split(' ')[4])

        l_read += 7
        monkeys.append(monkey)

    # Compute LCM of all tests
    tests = [m.test for m in monkeys]
    lcm = int(np.lcm.reduce(tests))

    # Rounds
    for _ in range(10000):
        for m_idx in range(len(monkeys)):
            m = monkeys[m_idx]
            for old in m.items:
                m.inspected += 1
                new = eval(m.operation)
                new = new % lcm
                if new % m.test == 0:
                    monkeys[m.dest_true].items.append(new)
                else:
                    monkeys[m.dest_false].items.append(new)
                
            # Remove items from monkey
            m.items = []

    inspected = sorted([m.inspected for m in monkeys])
    
    return inspected[-1] * inspected[-2]


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

