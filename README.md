# Pathfinding Algorithm Visualization

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Methaphur/path-finding.git 
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Features
1. Visualize A* and Dijkstra's pathfinding algorithms.
2. Create custom mazes with barriers and paths
3. Random maze generation feature with adjustable obstacle density.
4. Toggle between diagonal and non-diagonal movement.
5. Clear paths while retaining barriers and start/end points.
6. Interactive grid to set start, end, and barriers using mouse controls.


## Usage

1. **Run the main script:**
    ```bash
    python main.py
    ```

2. **Set the starting and ending positions:**
    - Use the left mouse button to click on the grid to set the starting position.
    - Click again to set the ending position.

3. **Add barriers:**
    - Any subsequent left mouse button clicks will add barriers.
    - You can drag-click to add multiple barriers.

4. **Reset a cell:**
    - Right-click on a cell to reset it.

5. **Generate a random maze:**
    - Press `M` to generate a random maze (30% of the cells will be obstacles).

6. **Reset the board:**
    - Press `C` to clear the screen reset the board.

7. **Find the shortest path:**
    - Press `A` to find the shortest path using the A* algorithm.
    - Press `D` to solve it using Dijkstra's algorithm.

8. **Erasing path:**
    - Press `R` to reset the path, but not the barriers or starting and ending cells.

9. **Switch path mode:**
    - Press `S` to switch between diagonal movement and non-diagonal movement
    
Enjoy visualizing the pathfinding algorithms!
