import pygame
import sys
from queue import PriorityQueue
import random
import time  # Import the time module

# Set up the display
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* and Dijkstra Pathfinding Visualization")
clock = pygame.time.Clock()
SPEED = 2000
ROWS = 50

diagonals = True

# Define colors
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Node class
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == GREEN

    def visited(self):
        self.visited = False    

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = LIGHT_BLUE

    def make_open(self):
        pass

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        global diagonals
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        
        if diagonals:
        # Diagonals movement
            if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():  # Down-Right
                self.neighbors.append(grid[self.row + 1][self.col + 1])
            if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():  # Down-Left
                self.neighbors.append(grid[self.row + 1][self.col - 1])
            if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():  # Up-Right
                self.neighbors.append(grid[self.row - 1][self.col + 1])
            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():  # Up-Left
                self.neighbors.append(grid[self.row - 1][self.col - 1])

    

# Heuristic for A* (Manhattan distance) L1 norm
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstruct the path
def reconstruct_path(came_from, start, current, draw):
    total_cost = 0
    while current in came_from:
        current = came_from[current]
        if current != start:
            current.make_path()
        draw()
        total_cost += 1
    return total_cost

# A* pathfinding algorithm
def astar(draw, grid, start, end):
    start_time = time.time()  # Start time
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    cells_explored = 0  # Counter for cells explored

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            total_cost = reconstruct_path(came_from, start, end, draw)
            end.make_end()
            end_time = time.time()  # End time
            print(f"A* Algorithm Time: {end_time - start_time:.4f} seconds")  # Print the time taken
            print(f"Total Cells Explored: {cells_explored}")  # Print the total cells explored
            print(f"Total Path Cost: {total_cost} \n")  # Print the total path cost
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    cells_explored += 1  # Increment the counter

        draw()

        if current != start:
            current.make_closed()

    end_time = time.time()  # End time
    print(f"A* Algorithm Time: {end_time - start_time:.4f} seconds")  # Print the time taken
    print(f"Total Cells Explored: {cells_explored}")  # Print the total cells explored
    print("There is no path \n")
    return False

# Dijkstra's pathfinding algorithm
def dijkstra(draw, grid, start, end):
    start_time = time.time()  # Start time
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}
    cells_explored = 0  # Counter for cells explored

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            total_cost = reconstruct_path(came_from, start, end, draw)
            end.make_end()
            end_time = time.time()  # End time
            print(f"Dijkstra's Algorithm Time: {end_time - start_time:.4f} seconds")  # Print the time taken
            print(f"Total Cells Explored: {cells_explored}")  # Print the total cells explored
            print(f"Total Path Cost: {total_cost} \n")  # Print the total path cost
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    cells_explored += 1  # Increment the counter

        draw()

        if current != start:
            current.make_closed()

    end_time = time.time()  # End time
    print(f"Dijkstra's Algorithm Time: {end_time - start_time:.4f} seconds")  # Print the time taken
    print(f"Total Cells Explored: {cells_explored}")  # Print the total cells explored
    print("There is no path \n")
    return False

# Create the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# Draw the grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Draw the grid
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    clock.tick(SPEED)
    pygame.display.update()

# Get the clicked position
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def random_maze(grid, rows):
    # Clear all existing barriers
    for row in grid:
        for node in row:
            node.reset()

    # Create random barriers
    for i in range(rows):
        for j in range(rows):
            node = grid[i][j]
            if random.random() < 0.3:  # Adjust the probability 
                # if not node.is_barrier() and not (node.is_start() and node.is_end()):
                node.make_barrier()


# Clear the grid while keeping start, end, and barriers
def reset_grid(grid):
    for row in grid:
        for node in row:
            if not node.is_barrier() and not(node.is_start() or node.is_end()):
                node.reset()

# Main function
def main(win, width):
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:   # Switch between diagonal and non-diagonal movement
                    global diagonals
                    diagonals = not diagonals

                if event.key == pygame.K_a and start and end:  # Run A* algorithm
                    reset_grid(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end:  # Run Dijkstra's algorithm
                    reset_grid(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_r:  # Reset grid
                    reset_grid(grid)
                
                if event.key == pygame.K_c:  # Clear grid
                    start, end = None, None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_m:  # Generate random maze
                    random_maze(grid, ROWS) 

    pygame.quit()

main(WIN, WIDTH)
