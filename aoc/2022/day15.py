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
class Day15Interval:
    def __init__(self):
        self.intervals = []

    def sort(self):
        self.intervals = sorted(self.intervals)

    def check_overlap(self, a, b):
        # a contains b
        if a[0] <= b[0] and a[1] >= b[1]:
            return True

        # b contains a
        if b[0] <= a[0] and b[1] >= a[1]:
            return True

        # Partial overlap
        if (a[0] <= b[0] and a[1] >= b[0]) or (b[1] >= a[0] and b[1] <= a[1]):
            return True

        return False

    def add_interval(self, left, right):
        overlap = []
        for inter in self.intervals:
            if self.check_overlap(inter, (left, right)):
                overlap.append(inter)

        new_interval = [left, right]
        for o in overlap:
            # Treat overlaps
            self.intervals.remove(o)
            new_interval[0] = min(new_interval[0], o[0])
            new_interval[1] = max(new_interval[1], o[1])

        self.intervals.append(new_interval)
        self.sort()

    def remove_point(self, val):
        # Remove a point from the intervals
        found = None
        for inter in self.intervals:
            if inter[0] <= val <= inter[1]:
                found = inter
                break

        if not found:
            return
        
        self.intervals.remove(found)
        int_left = [inter[0], val - 1]
        int_right = [val + 1, inter[1]]

        if int_left[0] <= int_left[1]:
            self.intervals.append(int_left)
        if int_right[0] <= int_right[1]:
            self.intervals.append(int_right)

        self.intervals.sort()

    def _empty_sum(self):
        s = 0
        for i in self.intervals:
            s += (i[1] - i[0] + 1)

        return s

    def sum(self, left=None, right=None):
        if not left and not right:
            return self._empty_sum()

        s = 0
        for i in self.intervals:
            if (i[0] < left and i[1] < left) or (i[0] > right and i[1] > right):
                continue

            s += (min(i[1], right) - max(i[0], left) + 1)

        return s

    def find_empty_space(self):
        spaces = []
        for j in range(len(self.intervals) - 1):
            if self.intervals[j][1] == self.intervals[j + 1][0] - 2:
                spaces.append(self.intervals[j][1] + 1)

        return spaces

    def __str__(self):
        return str(self.intervals)


def part1():
    lines = INPUT
    desired_row = 2000000
    sensors = []
    beacons = []

    for l in lines:
        tokens = l.replace('\n', '').split(' ')
        sensor_x, sensor_y = int(tokens[2][2:-1]), int(tokens[3][2:-1])
        beacon_x, beacon_y = int(tokens[8][2:-1]), int(tokens[9][2:])
        sensors.append((sensor_x, sensor_y))
        beacons.append((beacon_x, beacon_y))
        
    interval = Day15Interval()
    for s, b in zip(sensors, beacons):
        dist = abs(s[0] - b[0]) + abs(s[1] - b[1])
        range_size = dist - abs(s[1] - desired_row)
        if range_size < 0:
            # Not affected
            continue
        
        left = s[0] - range_size
        right = s[0] + range_size

        # Add new invalid interval
        interval.add_interval(left, right)

        # Remove point if beacon is in the problematic row
        if b[1] == desired_row:
            interval.remove_point(b[0])

    return interval.sum()


def part2():
    lines = INPUT
    distress_min, distress_max = 0, 4000000
    sensors = []
    beacons = []

    for l in lines:
        tokens = l.replace('\n', '').split(' ')
        sensor_x, sensor_y = int(tokens[2][2:-1]), int(tokens[3][2:-1])
        beacon_x, beacon_y = int(tokens[8][2:-1]), int(tokens[9][2:])
        sensors.append((sensor_x, sensor_y))
        beacons.append((beacon_x, beacon_y))

    for desired_row in range(distress_min, distress_max):
        interval = Day15Interval()
        # Check row for just one spot empty
        for s, b in zip(sensors, beacons):
            dist = abs(s[0] - b[0]) + abs(s[1] - b[1])
            range_size = dist - abs(s[1] - desired_row)
            if range_size < 0:
                # Not affected
                continue
            
            left = s[0] - range_size
            right = s[0] + range_size

            # Add new invalid interval
            interval.add_interval(left, right)

        if interval.sum(distress_min, distress_max) == distress_max - distress_min:
            return interval.find_empty_space()[0] * 4000000 + desired_row

    return 0


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

