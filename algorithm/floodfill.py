# floodfill.py
from collections import deque
from algorithm.maze import Maze

def flood_fill(maze, goal):
    """
    Compute Manhattan distance from every cell to the goal using floodfill (BFS).
    :param maze: Maze object with wall information.
    :param goal: Goal cell or list/tuple of goal cells (row, col). 
                 If multiple goal cells (e.g., center of maze), provide a list of (r,c) pairs.
    :return: 2D list of distances of size maze.height x maze.width.
    """
    # Initialize distance grid with a large number (treated as "unreached/blank").
    dist = [[9999 for _ in range(maze.width)] for _ in range(maze.height)]
    queue = deque()

    # Determine list of goal cells
    if isinstance(goal, list):
        goal_cells = goal
    elif isinstance(goal, tuple) and len(goal) > 0 and isinstance(goal[0], tuple):
        # If goal is a tuple of tuples, convert to list (to handle multiple goals given as tuple)
        goal_cells = list(goal)
    else:
        goal_cells = [goal]

    # Initialize queue with goal cell(s)
    for (gr, gc) in goal_cells:
        dist[gr][gc] = 0
        queue.append((gr, gc))

    # BFS floodfill to assign distances
    while queue:
        r, c = queue.popleft()
        current_d = dist[r][c]
        # Explore all four directions from (r,c)
        for direction, (dr, dc) in [('N', (-1, 0)), ('E', (0, 1)), ('S', (1, 0)), ('W', (0, -1))]:
            nr, nc = r + dr, c + dc
            # If neighbor is within bounds and accessible (no wall) and not visited yet
            if 0 <= nr < maze.height and 0 <= nc < maze.width:
                if maze.is_open(r, c, direction) and dist[nr][nc] == 9999:
                    dist[nr][nc] = current_d + 1
                    queue.append((nr, nc))
    return dist

# Function to update flood map based on new sensor data (walls).
def update_flood_map(maze, current_cell, sensor_walls, goal):
    """
    Update the maze with new walls from sensors and recompute the floodfill distances.
    :param maze: Maze object.
    :param current_cell: (row, col) of the robot's current position.
    :param sensor_walls: dict indicating where walls are detected relative to robot, 
                         e.g., {'N': True/False, 'E': ..., 'S': ..., 'W': ...}.
    :param goal: goal cell(s) to pass to flood_fill.
    :return: Updated distance map (2D list).
    """
    # Add walls to the maze based on sensor data at current cell
    r, c = current_cell
    for dir, has_wall in sensor_walls.items():
        if has_wall:
            maze.add_wall(r, c, dir)
    # Recompute and return new distance map
    return flood_fill(maze, goal)

# Independent testing of floodfill module
if __name__ == "__main__":
    from algorithm.maze import Maze
    # Create a 4x4 maze and add some walls for testing
    maze = Maze(4, 4)
    # Add a wall east of (1,1) and south of (0,2) to create a simple obstacle
    maze.add_wall(1, 1, 'E')  # wall between (1,1) and (1,2)
    maze.add_wall(0, 2, 'S')  # wall between (0,2) and (1,2)

    # Define goal cell (3,3) for example (bottom-right corner)
    goal = (3, 3)
    dist_map = flood_fill(maze, goal)
    print("Floodfill distance map (goal at (3,3)):")
    for row in dist_map:
        print(row)

    # Simulate updating flood map with a new wall detected at current position (1,2) on its north side
    current_pos = (1, 2)
    sensor_walls = {'N': True, 'E': False, 'S': False, 'W': False}  # suppose a wall was detected to the North of (1,2)
    new_map = update_flood_map(maze, current_pos, sensor_walls, goal)
    print("\nAfter adding wall north of (1,2), new distance map:")
    for row in new_map:
        print(row)
