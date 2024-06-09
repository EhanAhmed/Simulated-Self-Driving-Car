import pygame
import sys
import random
import heapq
from collections import deque

def heuristic(a, b):   #uses Manhattan distance
    
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
   
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < grid.width and 0 <= neighbor[1] < grid.height and grid.grid[neighbor[1]][neighbor[0]] != 'X' and grid.grid[neighbor[1]][neighbor[0]] != 'P':      #contstraint(can't go on x and cant use pruned path)
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return False

def bfs_search(grid, start, goal):
   
    queue = deque([(start, [start])])
    seen = set([start])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        (current, path) = queue.popleft()
        if current == goal:
            return path

        x, y = current
        for dx, dy in directions:
            next_position = (x + dx, y + dy)
            if 0 <= next_position[0] < grid.width and 0 <= next_position[1] < grid.height and grid.grid[next_position[1]][next_position[0]] != 'X' and grid.grid[next_position[1]][next_position[0]] != 'P':
                if next_position not in seen:
                    seen.add(next_position)
                    queue.append((next_position, path + [next_position]))

    return None

def hill_climbing_search(grid, start, goal):
   
    current = start
    path = [current]
    while current != goal:
        neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        valid_neighbors = [n for n in neighbors if 0 <= n[0] < grid.width and 0 <= n[1] < grid.height and grid.grid[n[1]][n[0]] != 'X' and grid.grid[n[1]][n[0]] != 'P']
        current = min(valid_neighbors, key=lambda x: heuristic(x, goal), default=current)
        if current in path or not valid_neighbors:  # Stuck 
            break
        path.append(current)
    return path

def alpha_beta_pruning(grid, path):
  
    for x, y in path:
        if grid.grid[y][x] == '.':
            grid.grid[y][x] = 'P'  # P for Pruned/Used path this is used by all algos

def calculate_score(grid, path):
   
    score = 0
    for x, y in path:
        cell = grid.grid[y][x]
        if cell == 'c':
            score += 5  # Score of small coin
        elif cell == 'C':
            score += 10  # Score of large coin
        elif cell == 'o':
            score -= 6   # Penalty of small pothole
        elif cell == 'O':
            score -= 90  # Penalty of large pothole
    return score

class Grid:
    def __init__(self, width, height, num_players):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_width = 800 // width
        self.cell_height = 600 // height
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Grid Simulation with Pygame")
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.players = []
        self.coins = []
        self.potholes = []
        self.obstacles = []
        self.goals = []

    def add_player(self, player_id, x, y, algorithm):
        player_label = f"P{player_id + 1}"
        self.players.append((x, y, player_label, algorithm))
        self.grid[y][x] = player_label

    def deploy_entities(self, entity_type, count, char, value_range):
        for _ in range(count):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            while self.grid[y][x] != '.':
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            value = random.choice(value_range)
            self.grid[y][x] = char(value)
            getattr(self, entity_type).append((x, y, value))

    def deploy_goals(self, num_goals):
        for i in range(num_goals):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            while self.grid[y][x] != '.':
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            goal_label = f"G{i+1}"
            self.grid[y][x] = goal_label
            self.goals.append((x, y, goal_label))

    def draw_grid(self):
        self.screen.fill((0, 0, 0)) 
        font = pygame.font.Font(None, 36)
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                item = self.grid[y][x]
                if item != '.':
                    text = font.render(item, True, (255, 255, 255))
                    self.screen.blit(text, (x * self.cell_width + 10, y * self.cell_height + 10))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

def setup_simulation():
    width = int(input("Enter the width of the grid: "))
    height = int(input("Enter the height of the grid: "))
    num_players = int(input("Enter the number of players: "))
    num_goals = int(input("Enter the number of goals: "))
    grid = Grid(width, height, num_players)

    grid.deploy_entities('coins', grid.width * grid.height // 4, lambda v: 'c' if v == 5 else 'C', [5, 10])
    grid.deploy_entities('potholes', (grid.width + grid.height) // 3, lambda v: 'o' if v == 6 else 'O', [6, 90])
    grid.deploy_entities('obstacles', (grid.width + grid.height) // 3, lambda _: 'X', [None])
    grid.deploy_goals(num_goals)

    for i in range(num_players):
        while True:
            x = int(input(f"Enter the x-coordinate of player {i+1}: "))
            y = int(input(f"Enter the y-coordinate of player {i+1}: "))
            if grid.grid[y][x] == '.':                                   # Ensure the position is unoccupied(CONSTRAINT)
                break
            print("Position already taken. Please choose another position.")

        print("Select algorithm: 1. A* Search 2. Hill Climbing 3. BFS")
        algo_choice = int(input("Your choice (1-3): "))
        grid.add_player(i, x, y, algo_choice)

        goal = random.choice(grid.goals)
        path = None
        algo_used = ""
        if algo_choice == 1:
            path = a_star_search(grid, (x, y), (goal[0], goal[1]))
            algo_used = "A* Search"
        elif algo_choice == 2:
            path = hill_climbing_search(grid, (x, y), (goal[0], goal[1]))
            algo_used = "Hill Climbing"
        elif algo_choice == 3:
            path = bfs_search(grid, (x, y), (goal[0], goal[1]))
            algo_used = "BFS"

        if path:
            alpha_beta_pruning(grid, path)
            score = calculate_score(grid, path)
            path_string = " -> ".join([f"({p[0]},{p[1]})" for p in path])
            print(f"Player {i+1} using {algo_used} navigated path: {path_string}")
            print(f"Player {i+1} scored: {score}")
        else:
            print(f"Player {i+1} using {algo_used}: No path found.")

    grid.run()

if __name__ == "__main__":
    setup_simulation()
