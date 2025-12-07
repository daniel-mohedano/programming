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
def _sum_vectors(numbers):
    sum = np.zeros(len(numbers[0]))

    for n in numbers:
        sum += n
    
    return sum


def part1():
    numbers = INPUT
    numbers = [np.array([-1 + 2*int(c) for c in n]) for n in numbers]
    
    sum = np.zeros(len(numbers[0]))

    for n in numbers:
        sum += n

    gamma_rate = 0
    epsilon_rate = 0
    
    for i in range(len(sum)):
        if sum[i] > 0:
            gamma_rate = gamma_rate * 2 + 1
            epsilon_rate *= 2
        else:
            gamma_rate *= 2
            epsilon_rate = epsilon_rate * 2 + 1

    return gamma_rate * epsilon_rate


def part2():
    numbers = INPUT
    numbers = [np.array([-1 + 2*int(c) for c in n]) for n in numbers]
    
    sum = _sum_vectors(numbers)

    # Oxygen Rating
    oxygen_nums = numbers.copy()
    bit = 0

    while len(oxygen_nums) != 1:
        oxygen_nums = [n for n in oxygen_nums if (sum[bit] == 0 and n[bit] == 1) or (n[bit] == np.sign(sum[bit]))]
        sum = _sum_vectors(oxygen_nums)
        bit += 1
        

    # CO2 Rating
    co2_nums = numbers.copy()
    bit = 0

    sum = _sum_vectors(numbers)

    while len(co2_nums) != 1:
        co2_nums = [n for n in co2_nums if (sum[bit] == 0 and n[bit] == -1) or (n[bit] == (-1)*np.sign(sum[bit]))]
        sum = _sum_vectors(co2_nums)
        bit += 1

    oxygen_rate = int(''.join([str(c) for c in oxygen_nums[0]]).replace('-1', '0'), 2)
    co2_rate = int(''.join([str(c) for c in co2_nums[0]]).replace('-1', '0'), 2)

    return oxygen_rate*co2_rate


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

