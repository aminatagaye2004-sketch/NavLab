import random
from time import perf_counter

from environment import detour_grid, get_reward, goal, grid, move, start

# Define the possible actions: up, down, left, right.
actions = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
]

# Choose an action based on the Q-table and epsilon-greedy policy.
def choose_action(q_table, position, epsilon):
    if random.random() < epsilon:
        return random.randrange(len(actions))

    values = q_table[position]
    best_value = max(values)
    best_actions = []

    for index, value in enumerate(values):
        if value == best_value:
            best_actions.append(index)

    return random.choice(best_actions)

# Run the Q-learning algorithm on the given map grid.
def run_q_learning(seed=42, map_grid=grid):
    random.seed(seed)

    q_table = {}
    for row in range(len(map_grid)):
        for col in range(len(map_grid[row])):
            if map_grid[row][col] == 0:
                q_table[(row, col)] = [0.0, 0.0, 0.0, 0.0]

    alpha = 0.1
    gamma = 0.9
    epsilon = 0.2
    episodes = 1000
    max_steps = 200

    # Time the training loop.
    training_start = perf_counter()

    for episode in range(episodes):
        position = start
        steps = 0

        while position != goal and steps < max_steps:
            action_index = choose_action(q_table, position, epsilon)
            next_position = move(map_grid, position, actions[action_index])
            reward = get_reward(next_position, goal)

            old_value = q_table[position][action_index]
            if next_position == goal:
                target = reward
            else:
                target = reward + gamma * max(q_table[next_position])

            q_table[position][action_index] = (
                old_value + alpha * (target - old_value)
            )

            position = next_position
            steps += 1

    training_seconds = perf_counter() - training_start

    # Time evaluation with exploration and Q-value updates off.
    position = start
    evaluation_path = [position]
    evaluation_steps = 0
    evaluation_start = perf_counter()

    while position != goal and evaluation_steps < max_steps:
        action_index = choose_action(q_table, position, 0.0)
        position = move(map_grid, position, actions[action_index])
        evaluation_path.append(position)
        evaluation_steps += 1

    evaluation_seconds = perf_counter() - evaluation_start

    print("Training seed:", seed)
    print(f"Training time: {training_seconds * 1_000:.3f} ms")
    print(f"Evaluation time: {evaluation_seconds * 1_000_000:.1f} µs")
    print("Evaluation reached goal:", position == goal)
    print("Evaluation steps:", evaluation_steps)
    print("Evaluation path:", evaluation_path)

    return evaluation_path

# Main function to run Q-learning on both maps.
if __name__ == "__main__":
    for map_name, map_grid in (("One-wall map", grid), ("Two-wall detour", detour_grid)):
        print(f"\nMap: {map_name}")
        run_q_learning(seed=42, map_grid=map_grid)
