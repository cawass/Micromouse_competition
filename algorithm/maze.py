# maze.py
class Maze:
    # Bit masks for walls
    WALL_N = 1  # 0001 - wall to the North
    WALL_E = 2  # 0010 - wall to the East
    WALL_S = 4  # 0100 - wall to the South
    WALL_W = 8  # 1000 - wall to the West

    def __init__(self, width, height):
        """Initialize a maze of given dimensions with no internal walls."""
        self.width = width
        self.height = height
        # 2D array for wall information, initialized with 0 (no walls).
        self.walls = [[0 for _ in range(width)] for _ in range(height)]
        # (Optionally, outer boundary walls could be initialized here, 
        # but is_open will treat out-of-range as walls anyway.)

    def add_wall(self, r, c, direction):
        """
        Add a wall at cell (r, c) in the given direction.
        Also updates the adjacent cell's opposite wall for consistency.
        """
        if direction == 'N':
            # Wall on north side of (r,c) -> also wall on south side of (r-1,c)
            self.walls[r][c] |= Maze.WALL_N
            if r - 1 >= 0:
                self.walls[r-1][c] |= Maze.WALL_S
        elif direction == 'E':
            # Wall on east side of (r,c) -> also wall on west side of (r,c+1)
            self.walls[r][c] |= Maze.WALL_E
            if c + 1 < self.width:
                self.walls[r][c+1] |= Maze.WALL_W
        elif direction == 'S':
            # Wall on south side of (r,c) -> also wall on north side of (r+1,c)
            self.walls[r][c] |= Maze.WALL_S
            if r + 1 < self.height:
                self.walls[r+1][c] |= Maze.WALL_N
        elif direction == 'W':
            # Wall on west side of (r,c) -> also wall on east side of (r,c-1)
            self.walls[r][c] |= Maze.WALL_W
            if c - 1 >= 0:
                self.walls[r][c-1] |= Maze.WALL_E
        else:
            raise ValueError("Invalid direction. Use 'N', 'E', 'S', or 'W'.")

    def is_open(self, r, c, direction):
        """
        Check if the cell (r,c) has an open path in the given direction 
        (no wall and within maze bounds). Returns True if movement is possible.
        """
        if direction == 'N':
            if r - 1 < 0:
                return False  # out of bounds (treat as wall)
            # No wall on current cell's north and neighbor's south
            return not (self.walls[r][c] & Maze.WALL_N or self.walls[r-1][c] & Maze.WALL_S)
        elif direction == 'S':
            if r + 1 >= self.height:
                return False
            return not (self.walls[r][c] & Maze.WALL_S or self.walls[r+1][c] & Maze.WALL_N)
        elif direction == 'W':
            if c - 1 < 0:
                return False
            return not (self.walls[r][c] & Maze.WALL_W or self.walls[r][c-1] & Maze.WALL_E)
        elif direction == 'E':
            if c + 1 >= self.width:
                return False
            return not (self.walls[r][c] & Maze.WALL_E or self.walls[r][c+1] & Maze.WALL_W)
        else:
            raise ValueError("Invalid direction. Use 'N', 'E', 'S', or 'W'.")

# Independent testing of Maze module
if __name__ == "__main__":
    # Create a 2x2 maze and add some walls, then test is_open logic
    maze = Maze(2, 2)
    print("Initial walls:", maze.walls)  # Expect all zeros (no walls)

    # Add a wall on the north side of cell (1,0)
    maze.add_wall(1, 0, 'N')
    # This should also add a wall on the south side of cell (0,0)
    print("After adding wall between (1,0) and (0,0):", maze.walls)
    # Test movement between these cells
    print("is_open(1,0,'N') ->", maze.is_open(1, 0, 'N'))  # Expect False (wall present)
    print("is_open(0,0,'S') ->", maze.is_open(0, 0, 'S'))  # Expect False (wall present)
    print("is_open(0,0,'E') ->", maze.is_open(0, 0, 'E'))  # Expect True (no wall to the east)")
