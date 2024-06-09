# Simulated-Self-Driving-Car

# Grid-Based Pathfinding Simulation with Pygame

This Python project is a grid-based simulation that implements three different pathfinding algorithms: A* Search, Hill Climbing, and Breadth-First Search (BFS). The simulation uses Pygame for visualization, allowing players to navigate through a grid containing various entities such as coins, potholes, and obstacles.

## Features

- **Grid Setup**: Define the grid size and place different entities randomly, including coins (with varying scores), potholes (with different penalties), and obstacles.
- **Player Management**: Multiple players can be added to the grid, each using one of the three pathfinding algorithms.
- **Pathfinding Algorithms**:
  - **A* Search**: Uses Manhattan distance as the heuristic for finding the optimal path.
  - **Hill Climbing**: Chooses the next step based on the minimum heuristic value.
  - **BFS**: Explores all possible paths level by level to find the shortest path.
- **Alpha-Beta Pruning**: Marks the path taken by each algorithm to prevent other players from reusing the same path.
- **Scoring System**: Calculates the player's score based on the entities encountered on the path (coins and potholes).
- **Pygame Visualization**: Provides a graphical interface to visualize the grid and the entities.

## How to Use

1. **Grid Initialization**: Define the grid's width and height, the number of players, and the number of goals.
2. **Entity Deployment**: Randomly place coins, potholes, and obstacles on the grid.
3. **Player Addition**: Add players to the grid by specifying their starting coordinates and the algorithm they will use.
4. **Pathfinding**: Each player will navigate to a randomly chosen goal using their selected algorithm.
5. **Scoring**: The path taken and the score of each player will be displayed.
6. **Visualization**: Run the Pygame visualization to see the grid and the positions of all entities.

## How to Run

1. Ensure you have Python and Pygame installed.
2. Run the `setup_simulation()` function to start the simulation.
3. Follow the prompts to input grid dimensions, player positions, and algorithm choices.
4. Observe the results and pathfinding process in the Pygame window.

## Code Structure

- **heuristic(a, b)**: Calculates the Manhattan distance between two points.
- **a_star_search(grid, start, goal)**: Implements the A* Search algorithm.
- **bfs_search(grid, start, goal)**: Implements the BFS algorithm.
- **hill_climbing_search(grid, start, goal)**: Implements the Hill Climbing algorithm.
- **alpha_beta_pruning(grid, path)**: Marks the path taken by players.
- **calculate_score(grid, path)**: Calculates the score based on the entities encountered on the path.
- **Grid class**: Manages the grid, entities, players, and Pygame visualization.
- **setup_simulation()**: Sets up and runs the simulation based on user input.

## Notes

- The grid is visualized in a Pygame window, with different symbols representing players, goals, coins, potholes, and obstacles.
- Players navigate through the grid avoiding obstacles and potholes while collecting coins to maximize their score.
- The path and score of each player are displayed in the console.

This project provides an interactive and visual way to understand and compare different pathfinding algorithms in a grid-based environment.
