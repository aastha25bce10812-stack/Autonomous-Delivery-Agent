import heapq
from collections import deque
import time
import copy

# ------------------------------------------------------------
# GRID SETTINGS
# ------------------------------------------------------------

ROWS = 10   # Number of rows in the grid
COLS = 10   # Number of columns in the grid

# Symbols used in the grid
EMPTY = 0
WALL = 1
START = 'S'
GOAL = 'G'
AGENT = 'A'
MOVING_OBS = 'M'

# ------------------------------------------------------------
# CREATE INITIAL GRID
# ------------------------------------------------------------

def create_grid():
    """
    Creates a 10x10 grid with static obstacles.
    """
    grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

    # Add static obstacles (walls)
    walls = [(1, 3), (2, 3), (3, 3), (4, 3), (6, 6), (6, 7), (6, 8), (7, 8)]
    for r, c in walls:
        grid[r][c] = WALL

    return grid

# ------------------------------------------------------------
# PRINT GRID
# ------------------------------------------------------------

def print_grid(grid, start, goal, agent_pos, moving_obstacles):
    """
    Prints the current state of the grid.
    """
    temp = copy.deepcopy(grid)

    # Mark moving obstacles
    for obs in moving_obstacles:
        temp[obs[0]][obs[1]] = MOVING_OBS

    # Mark start, goal, and agent
    temp[start[0]][start[1]] = START
    temp[goal[0]][goal[1]] = GOAL
    temp[agent_pos[0]][agent_pos[1]] = AGENT

    print("\nCurrent Grid:")
    for row in temp:
        print(" ".join(str(cell) for cell in row))
    print("-" * 30)

# ------------------------------------------------------------
# CHECK VALID CELL
# ------------------------------------------------------------

def is_valid(grid, row, col, moving_obstacles):
    """
    Checks if a cell is inside the grid and not blocked.
    """
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False

    if grid[row][col] == WALL:
        return False

    if (row, col) in moving_obstacles:
        return False

    return True

# ------------------------------------------------------------
# GET NEIGHBORS
# ------------------------------------------------------------

def get_neighbors(grid, node, moving_obstacles):
    """
    Returns valid neighboring cells.
    """
    row, col = node
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []

    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if is_valid(grid, nr, nc, moving_obstacles):
            neighbors.append((nr, nc))

    return neighbors

# ------------------------------------------------------------
# RECONSTRUCT PATH
# ------------------------------------------------------------

def reconstruct_path(parent, goal):
    """
    Reconstructs the path from goal to start using parent dictionary.
    """
    path = []
    current = goal

    while current in parent:
        path.append(current)
        current = parent[current]

    path.append(current)  # Add start
    path.reverse()        # Reverse to get correct order
    return path

# ------------------------------------------------------------
# BFS ALGORITHM
# ------------------------------------------------------------

def bfs(grid, start, goal, moving_obstacles):
    """
    Breadth-First Search algorithm.
    Finds shortest path in terms of number of steps.
    """
    queue = deque([start])         # Queue for BFS
    visited = set([start])         # Visited nodes
    parent = {}                    # To store path

    while queue:
        current = queue.popleft()

        if current == goal:
            return reconstruct_path(parent, goal)

        for neighbor in get_neighbors(grid, current, moving_obstacles):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None  # No path found

# ------------------------------------------------------------
# UCS ALGORITHM
# ------------------------------------------------------------

def ucs(grid, start, goal, moving_obstacles):
    """
    Uniform Cost Search algorithm.
    Finds least-cost path.
    Here each move has cost 1.
    """
    pq = [(0, start)]              # Priority queue with (cost, node)
    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    while pq:
        cost, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return reconstruct_path(parent, goal)

        for neighbor in get_neighbors(grid, current, moving_obstacles):
            new_cost = cost_so_far[current] + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None  # No path found

# ------------------------------------------------------------
# HEURISTIC FUNCTION FOR A*
# ------------------------------------------------------------

def heuristic(a, b):
    """
    Manhattan distance heuristic for A*.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ------------------------------------------------------------
# A* ALGORITHM
# ------------------------------------------------------------

def a_star(grid, start, goal, moving_obstacles):
    """
    A* Search algorithm.
    Uses path cost + heuristic to find efficient path.
    """
    pq = [(0, start)]              # Priority queue
    parent = {}
    g_cost = {start: 0}            # Cost from start to node
    f_cost = {start: heuristic(start, goal)}  # Estimated total cost

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            return reconstruct_path(parent, goal)

        for neighbor in get_neighbors(grid, current, moving_obstacles):
            tentative_g = g_cost[current] + 1

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                parent[neighbor] = current
                g_cost[neighbor] = tentative_g
                f_cost[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_cost[neighbor], neighbor))

    return None  # No path found

# ------------------------------------------------------------
# MOVE OBSTACLES
# ------------------------------------------------------------

def move_obstacles(moving_obstacles, grid):
    """
    Moves obstacles in a simple left-right pattern if possible.
    """
    new_positions = []

    for r, c in moving_obstacles:
        # Try moving right first
        if c + 1 < COLS and grid[r][c + 1] != WALL and (r, c + 1) not in moving_obstacles:
            new_positions.append((r, c + 1))
        # Otherwise try moving left
        elif c - 1 >= 0 and grid[r][c - 1] != WALL and (r, c - 1) not in moving_obstacles:
            new_positions.append((r, c - 1))
        else:
            new_positions.append((r, c))  # Stay in same place

    return new_positions

# ------------------------------------------------------------
# RUN ALGORITHM AND SIMULATE AGENT
# ------------------------------------------------------------

def simulate_algorithm(name, algorithm, grid, start, goal, moving_obstacles):
    """
    Simulates the selected algorithm and replans if obstacle blocks the path.
    """
    print(f"\n==============================")
    print(f"Running {name}")
    print(f"==============================")

    agent_pos = start
    steps = 0

    start_time = time.time()

    while agent_pos != goal:
        # Find path from current agent position to goal
        path = algorithm(grid, agent_pos, goal, moving_obstacles)

        if not path:
            print(f"{name}: No path found!")
            return

        print(f"{name} planned path: {path}")

        # Move one step at a time
        for next_step in path[1:]:
            # Move obstacles before agent moves
            moving_obstacles = move_obstacles(moving_obstacles, grid)

            # If next step is blocked, replan
            if next_step in moving_obstacles:
                print(f"{name}: Path blocked by moving obstacle! Replanning...")
                break

            # Move agent
            agent_pos = next_step
            steps += 1

            # Print grid
            print_grid(grid, start, goal, agent_pos, moving_obstacles)
            time.sleep(0.3)

            if agent_pos == goal:
                end_time = time.time()
                print(f"{name}: Goal reached in {steps} steps!")
                print(f"{name}: Time taken = {round(end_time - start_time, 4)} seconds")
                return

# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------

def main():
    """
    Main function to run the full simulation.
    """
    grid = create_grid()

    # Start and goal positions
    start = (0, 0)
    goal = (9, 9)

    # Moving obstacles initial positions
    moving_obstacles = [(2, 6), (5, 5)]

    # Run BFS
    simulate_algorithm("BFS", bfs, grid, start, goal, moving_obstacles.copy())

    # Run UCS
    simulate_algorithm("UCS", ucs, grid, start, goal, moving_obstacles.copy())

    # Run A*
    simulate_algorithm("A*", a_star, grid, start, goal, moving_obstacles.copy())

# ------------------------------------------------------------
# RUN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    main()

