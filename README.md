# NavLab

NavLab compares A* path planning and Q-learning on two 10x10 grid maps. I started the project after attending the Embodied Intelligence Summer School at UCL. I wanted to see how a robot could solve the same navigation problem by planning with a known map or by learning from experience.


## Run the demo

With Python 3.12 and your virtual environment active, run these commands from the project folder:

```bash
python -m pip install pygame==2.6.1
python simulation.py
```

- **1** replays A*.
- **2** replays Q-learning.
- **M** switches between the one-wall map and the two-wall detour.
- **Space** restarts the replay.

To run both maps in the terminal:

```bash
python astar.py
python qlearning.py
```

## How it works

The robot moves up, down, left, or right. Walls and grid boundaries block movement. A* uses the known map and Manhattan distance to find a shortest route. Q-learning updates a table of action values during training. Every attempt earns −1, except the move that reaches the goal, which earns +10. Evaluation follows the highest learned values with exploration and updates disabled. Ties are broken randomly.

## Results

| Map | A* route | Q-learning route after training |
| --- | ---: | ---: |
| One wall with a gap | 18 moves | 18 moves |
| Two walls with offset gaps | 28 moves | 28 moves |

Q-learning matched the A* route length on both maps after 1,000 training episodes with seeds 7, 21, and 42. The terminal command uses seed 42 by default. The two-wall map forces the robot to travel down through the first gap and then back up to the second.

On the one-wall map, a policy trained for 100 episodes with seed 42 repeatedly chose a blocked move at the start during evaluation. With 1,000 training episodes, it reached the goal in 18 moves.

## Timing Result

| Measurement | One-wall map (single run) | Two-wall detour (median of six runs) |
| --- | ---: | ---: |
| A* planning | 87.1 µs | 120.55 µs |
| Q-learning training loop, 1,000 episodes with seed 42 | 39.087 ms | 61.350 ms |
| Q-learning evaluation after training | 16.4 µs | 25.55 µs |

The A* timer covers finding a route from the map. The Q-learning evaluation timer covers choosing and executing actions with a trained table. These results come from two fixed maps with a fixed start and goal on each.
