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
    map = [x.replace('\n', '') for x in INPUT]
    heights = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]
    start = None
    end = None

    def valid_neighbors(node, heights):
        valid = []
        possible = []
        for i in range(-1, 2, 1):
            # Vertical
            v = (max(min(node[0] + i, len(heights) - 1), 0), node[1])
            # Horizontal
            h = (node[0], max(min(node[1] + i, len(heights[0]) - 1), 0))
            if v != node and v not in possible:
                possible.append(v)
            if h != node and h not in possible:
                possible.append(h)
    
        for n in possible:
            if heights[n[0]][n[1]] <= heights[node[0]][node[1]] + 1 and n not in valid:
                valid.append(n)

        return valid

    # Read heights and starting/end points 
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'S':
                heights[i][j] = 0
                start = (i, j)
            elif map[i][j] == 'E':
                heights[i][j] = ord('z') - ord('a')
                end = (i, j)
            else:
                heights[i][j] = ord(map[i][j]) - ord('a')

    # Perform dijkstra
    d_prev = {}
    d_dist = {}
    s = {}
    pq = queue.PriorityQueue() 

    # Initialize structures
    for i in range(len(heights)):
        for j in range(len(heights[0])):
            d_prev[(i, j)] = None
            d_dist[(i, j)] = np.Inf
            s[(i, j)] = False

    # Push starting node to Queue
    d_dist[start] = 0
    pq.put((d_dist[start], start))

    # Dijkstra loop
    while not pq.empty():
        _, v = pq.get()
        if v == end:
            break
        if not s[v]:
            s[v] = True
            # If the node has not been checked 
            valid = valid_neighbors(v, heights)

            for next in valid:
                # If better path found, update it
                if d_dist[next] > d_dist[v] + 1:
                    d_dist[next] = d_dist[v] + 1
                    d_prev[next] = v
                    pq.put((d_dist[next], next))

    return d_dist[end]


def part2():
    map = [x.replace('\n', '') for x in INPUT]
    heights = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]
    possible_starts = []
    end = None

    def valid_neighbors(node, heights):
        valid = []
        possible = []
        for i in range(-1, 2, 1):
            # Vertical
            v = (max(min(node[0] + i, len(heights) - 1), 0), node[1])
            # Horizontal
            h = (node[0], max(min(node[1] + i, len(heights[0]) - 1), 0))
            if v != node and v not in possible:
                possible.append(v)
            if h != node and h not in possible:
                possible.append(h)
    
        for n in possible:
            if heights[n[0]][n[1]] <= heights[node[0]][node[1]] + 1 and n not in valid:
                valid.append(n)

        return valid

    # Read heights and starting/end points 
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'S':
                heights[i][j] = 0
                possible_starts.append((i, j))
            elif map[i][j] == 'E':
                heights[i][j] = ord('z') - ord('a')
                end = (i, j)
            else:
                heights[i][j] = ord(map[i][j]) - ord('a')
                if heights[i][j] == 0:
                    possible_starts.append((i, j))

    # Iterate dijkstra for all possible starts
    shortest_path = np.Inf

    for start in possible_starts:
        # Perform dijkstra
        d_prev = {}
        d_dist = {}
        s = {}
        pq = queue.PriorityQueue() 

        # Initialize structures
        for i in range(len(heights)):
            for j in range(len(heights[0])):
                d_prev[(i, j)] = None
                d_dist[(i, j)] = np.Inf
                s[(i, j)] = False

        # Push starting node to Queue
        d_dist[start] = 0
        pq.put((d_dist[start], start))

        # Dijkstra loop
        while not pq.empty():
            _, v = pq.get()
            if v == end:
                break
            if not s[v]:
                s[v] = True
                # If the node has not been checked 
                valid = valid_neighbors(v, heights)

                for next in valid:
                    # If better path found, update it
                    if d_dist[next] > d_dist[v] + 1:
                        d_dist[next] = d_dist[v] + 1
                        d_prev[next] = v
                        pq.put((d_dist[next], next))

        shortest_path = min(shortest_path, d_dist[end])

    return shortest_path


if __name__ == '__main__':
    # Argument parser configuration
    parser = argparse.ArgumentParser(prog=Path(__file__).resolve())
    parser.add_argument('-t', action='store_true')
    args = parser.parse_args()
    TEST_MODE = args.t

    # Main execution
    main()

