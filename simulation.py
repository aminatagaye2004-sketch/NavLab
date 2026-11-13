import math

import pygame

from astar import astar
from environment import detour_grid, goal, grid, start
from qlearning import run_q_learning


CELL = 48
LEFT = 32
TOP = 146
STEP_MS = 240
INK = (77, 30, 65)
PINK = (214, 48, 125)
PURPLE = (139, 75, 189)


def center(cell):
    row, col = cell
    return pygame.Vector2(LEFT + col * CELL + CELL / 2,
                          TOP + row * CELL + CELL / 2)


def main():
    maps = (("One-wall map", grid), ("Two-wall detour", detour_grid))
    paths = []
    for _, map_grid in maps:
        paths.append((
            astar(map_grid, start, goal) or [start],
            run_q_learning(map_grid=map_grid) or [start],
        ))
    pygame.init()
    width = LEFT * 2 + len(grid[0]) * CELL
    bottom = TOP + len(grid) * CELL
    screen = pygame.display.set_mode((width, bottom + 66))
    pygame.display.set_caption("NavLab")
    clock = pygame.time.Clock()
    title = pygame.font.Font(None, 53)
    font = pygame.font.Font(None, 24)

    def label(message, x, y, color=INK, face=font):
        screen.blit(face.render(message, True, color), (x, y))

    map_index = 0
    mode = 0
    started = pygame.time.get_ticks()
    running = True

    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_m, pygame.K_SPACE):
                    if event.key == pygame.K_1:
                        mode = 0
                    elif event.key == pygame.K_2:
                        mode = 1
                    elif event.key == pygame.K_m:
                        map_index = 1 - map_index
                    started = now

        map_name, map_grid = maps[map_index]
        path = paths[map_index][mode]
        accent = (PINK, PURPLE)[mode]
        progress = min((now - started) / STEP_MS, len(path) - 1)
        index = int(progress)
        fraction = progress - index
        eased = fraction * fraction * (3 - 2 * fraction)
        robot = center(path[index]).lerp(center(path[min(index + 1, len(path) - 1)]), eased)

        screen.fill((255, 232, 245))
        label("NavLab", LEFT, 25, face=title)
        label(("A* planning", "Q-learning replay")[mode], LEFT + 2, 78, accent)
        label(map_name, LEFT + 2, 104)
        label(f"{index} / {len(path) - 1} steps", width - 145, 78)

        for row, cells in enumerate(map_grid):
            for col, blocked in enumerate(cells):
                square = pygame.Rect(LEFT + col * CELL + 2,
                                     TOP + row * CELL + 2, CELL - 4, CELL - 4)
                color = (112, 55, 95) if blocked else (255, 247, 252)
                if (row, col) == start:
                    color = (252, 196, 224)
                elif (row, col) == goal:
                    color = (247, 163, 205)
                pygame.draw.rect(screen, color, square, border_radius=10)

        trail = [center(cell) for cell in path[:index + 1]] + [robot]
        pygame.draw.lines(screen, (233, 154, 206), False, trail, 5)
        for point in trail[:-1]:
            pygame.draw.circle(screen, accent, point, 3)

        pulse = (1 + math.sin(now / 130)) / 2
        goal_center = center(goal)
        pygame.draw.circle(screen, (255, 224, 242), goal_center, 12 + int(5 * pulse), 2)
        pygame.draw.circle(screen, INK, goal_center, 5)
        pygame.draw.circle(screen, (255, 219, 238), robot, 18 + int(3 * pulse))
        pygame.draw.circle(screen, accent, robot, 13)
        pygame.draw.circle(screen, (255, 249, 253), robot + (-4, -3), 2)
        pygame.draw.circle(screen, (255, 249, 253), robot + (4, -3), 2)

        label("1 A*   2 Q-learning   M Map   Space Replay", LEFT, bottom + 22)
        if index == len(path) - 1:
            status = "Goal reached" if path[-1] == goal else "Goal not reached"
            label(status, width - 155, bottom + 22, accent)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
