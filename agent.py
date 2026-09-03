from collections import deque
import heapq
import random
import math

class GreedyGridAgent:
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']
    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """Pure condition-action rules — no memory."""
    def sense_and_act(self, percept: dict) -> str:
        if percept.get('wall_ahead'):
            return 'Left'          # IF wall_ahead THEN turn_left
        if percept.get('food_here'):
            return 'Up'            # IF food_here THEN act
        return 'Up'                # ELSE move_forward


class ModelBasedAgent:
    """Keeps internal state so it doesn't repeat a failed action."""
    def __init__(self):
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        options = ['Left', 'Right', 'Down', 'Up']
        if percept.get('wall_ahead'):
            if self.last_action in options:
                idx = options.index(self.last_action)
                action = options[(idx + 1) % len(options)]   # rotate to a NEW action
            else:
                action = options[0]
        elif percept.get('food_here'):
            action = 'Up'
        else:
            action = 'Up'
        self.last_action = action
        return action

class SearchAgent:
    """Uninformed Search Agent supporting BFS, DFS, and UCS."""
    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'  # Can be changed to 'DFS' or 'UCS'

    def _neighbors(self, pos, walls, grid_size):
        x, y = pos
        w, h = grid_size
        for action, (nx, ny) in (('Up', (x, y+1)), ('Down', (x, y-1)),
                                  ('Left', (x-1, y)), ('Right', (x+1, y))):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in walls:
                yield action, (nx, ny)

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(walls)
        frontier = deque([(start_pos, [])])
        reached = {start_pos}
        while frontier:
            pos, path = frontier.popleft()
            if pos == goal_pos:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(walls)
        frontier = [(start_pos, [])]
        reached = {start_pos}
        while frontier:
            pos, path = frontier.pop()
            if pos == goal_pos:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                if npos not in reached:
                    reached.add(npos)
                    frontier.append((npos, path + [action]))
        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        walls = set(walls)
        frontier = [(0, start_pos, [])]
        best = {start_pos: 0}
        while frontier:
            cost, pos, path = heapq.heappop(frontier)
            if pos == goal_pos:
                return path
            for action, npos in self._neighbors(pos, walls, grid_size):
                new_cost = cost + 1
                if npos not in best or new_cost < best[npos]:
                    best[npos] = new_cost
                    heapq.heappush(frontier, (new_cost, npos, path + [action]))
        return None

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        walls = set(walls)
        h_fn = self.manhattan_distance if heuristic_type == 'manhattan' else self.euclidean_distance
        
        # Priority Queue stores: (f_cost, g_cost, current_pos, path_taken)
        frontier = [(h_fn(start_pos, goal_pos), 0, start_pos, [])]
        reached_states = set()

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            for action, npos in self._neighbors(current_pos, walls, grid_size):
                if npos not in reached_states:
                    g_new = g_cost + 1
                    f_new = g_new + h_fn(npos, goal_pos)
                    heapq.heappush(frontier, (f_new, g_new, npos, path_taken + [action]))

        return None

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            start = tuple(percept['agent_pos'])
            walls = set(percept['walls'])
            grid_size = percept['grid_size']
            foods = percept['all_food']
            if not foods:
                return 'Up'
            
            # Select target food item using Manhattan distance
            goal = min(foods, key=lambda f: abs(f[0]-start[0]) + abs(f[1]-start[1]))

            if self.active_algo == 'BFS':
                path = self.bfs_search(start, goal, walls, grid_size)
            elif self.active_algo == 'DFS':
                path = self.dfs_search(start, goal, walls, grid_size)
            elif self.active_algo == 'UCS':
                path = self.ucs_search(start, goal, walls, grid_size)
            elif self.active_algo == 'AStar':
                path = self.astar_search(start, goal, walls, grid_size, heuristic_type='manhattan')
            else:
                path = None
            self.plan = path if path else ['Up']

        return self.plan.pop(0)