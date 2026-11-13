from time import perf_counter

from astar import astar


# Original map: one wall with a gap at (5, 4).
grid = []
for row in range(10):
    grid.append([0] * 10)
    if row != 5:
        grid[row][4] = 1

# Detour map: two walls with gaps at (7, 3) and (2, 6).
detour_grid = []
for row in range(10):
    detour_grid.append([0] * 10)
    if row != 7:
        detour_grid[row][3] = 1
    if row != 2:
        detour_grid[row][6] = 1

start = (0, 0)
goal = (9, 9)

# Define the possible actions: up, down, left, right.
def move(grid, position, direction):
    row, col = position
    row_change, col_change = direction
    new_row = row + row_change
    new_col = col + col_change

    if (
        0 <= new_row < len(grid)
        and 0 <= new_col < len(grid[new_row])
        and grid[new_row][new_col] == 0
    ):
        return new_row, new_col

    return position

# Reset the position to the start.
def reset(start):
    return start

# Get the reward for reaching the goal or hitting a wall.
def get_reward(position, goal):
    if position == goal:
        return 10
    return -1

# Main function to test the A* algorithm.
if __name__ == "__main__":
    for map_name, map_grid in (
        ("One-wall map", grid),
        ("Two-wall detour", detour_grid),
    ):
        planning_start = perf_counter()
        path = astar(map_grid, start, goal)
        planning_seconds = perf_counter() - planning_start

        print(f"\nMap: {map_name}")
        print(f"A* planning time: {planning_seconds * 1_000_000:.1f} µs")
        print("A* path:", path)

        if path is not None:
            print("Number of moves:", len(path) - 1)
        else:
            print("No path exists.")