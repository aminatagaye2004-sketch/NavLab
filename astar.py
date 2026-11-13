import heapq

# calculate the Manhattan distance between two points.
def manhattan(position, goal):
    row, col = position
    goal_row, goal_col = goal
    return abs(row - goal_row) + abs(col - goal_col)

# Reconstruct the path from the start to the goal using the came_from dictionary.
def reconstruct_path(came_from, current_cell):
    path = [current_cell]

    while current_cell in came_from:
        current_cell = came_from[current_cell]
        path.append(current_cell)

    path.reverse()
    return path

# A* algorithm implementation to find the shortest path in a grid.
def astar(grid, start, goal):
    frontier = []
    heapq.heappush(frontier, (manhattan(start, goal), start))
    g_score = {start: 0}
    came_from = {}

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
    ]

    while frontier:
        _, current_cell = heapq.heappop(frontier)

        if current_cell == goal:
            return reconstruct_path(came_from, current_cell)

        row, col = current_cell

        for row_change, col_change in directions:
            new_row = row + row_change
            new_col = col + col_change
            neighbour = (new_row, new_col)

            if (
                0 <= new_row < len(grid)
                and 0 <= new_col < len(grid[new_row])
                and grid[new_row][new_col] == 0
            ):
                tentative_g = g_score[current_cell] + 1

                if neighbour not in g_score or tentative_g < g_score[neighbour]:
                    came_from[neighbour] = current_cell
                    g_score[neighbour] = tentative_g
                    f_score = tentative_g + manhattan(neighbour, goal)
                    heapq.heappush(frontier, (f_score, neighbour))

    return None


# Main function to test the A* algorithm.
if __name__ == "__main__":
    from time import perf_counter

    from environment import detour_grid, goal, grid, start

    for map_name, map_grid in (("One-wall map", grid), ("Two-wall detour", detour_grid)):
        planning_start = perf_counter()
        path = astar(map_grid, start, goal)
        planning_seconds = perf_counter() - planning_start

        print(f"\nMap: {map_name}")
        print(f"A* planning time: {planning_seconds * 1_000_000:.1f} µs")
        print("A* path:", path)
        if path is None:
            print("No path exists.")
        else:
            print("Number of moves:", len(path) - 1)
