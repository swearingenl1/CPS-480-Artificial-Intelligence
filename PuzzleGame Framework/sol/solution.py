#This is the only file you need to work on. You do NOT need to modify other files

# Below are the functions you need to implement. For the first project, you only need to finish implementing iddfs() 
# ie iterative deepening depth first search

import heapq
import itertools

# here you need to implement the Iterative Deepening Search Method
def iterativeDeepening(puzzle):
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    start = tuple(puzzle)
 
    # Already solved -> empty path
    if start == goal:
        return []

    # Find every state reachable by sliding one tile into the blank space. Returns a list of (new_state, new_blank_position) pairs.
    def get_neighbors(state):
        blank_idx = state.index(8) # find where 8 (blank) currently is
        row, col = divmod(blank_idx, 3)
        neighbors = []
        # Try moving the blank up, down, left, and right one cell.
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                # Make a copy of the board and swap the blank with the neighboring tile.
                new_state = list(state)
                new_state[blank_idx], new_state[new_idx] = new_state[new_idx], new_state[blank_idx]
                neighbors.append((tuple(new_state), new_idx))
        return neighbors

    # Explore depth-first, but not deeper than 'limit' moves from the start. 'visited' keeps track of states already used , so we don't go in circles.
    def depth_limited_dfs(state, depth, limit, path, visited):
        # Success -> reached the solved board.
        if state == goal: 
            return path
        # Used up allowed depth for this round without finding the goal. Give up on this branch.
        if depth == limit:
            return None
        # Try every possible next move from here.
        for new_state, blank_pos in get_neighbors(state):
            if new_state not in visited:
                visited.add(new_state)
                result = depth_limited_dfs(new_state, depth + 1, limit, path + [blank_pos], visited)
                if result is not None:
                    return result
                visited.remove(new_state)  # backtrack
 
        return None
 
    # Iterative deepening: increase the depth bound one level at a time.
    # Because the bound grows by 1 each round, the first solution found is guaranteed to be of minimal length (optimal).
    limit = 0
    while True:
        visited = {start}
        result = depth_limited_dfs(start, 0, limit, [], visited)
        if result is not None:
            return result
        limit += 1
 
 
# This will be for next project
def astar(puzzle):
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    start = tuple(puzzle)
 
    # Already solved -> empty path
    if start == goal:
        return []
 
    # Find every state reachable by sliding one tile into the blank space. Returns a list of (new_state, new_blank_position) pairs.
    def get_neighbors(state):
        blank_idx = state.index(8)  # find where 8 (blank) currently is
        row, col = divmod(blank_idx, 3)
        neighbors = []
        # Try moving the blank up, down, left, and right one cell.
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_idx = nr * 3 + nc
                # Make a copy of the board and swap the blank with the neighboring tile.
                new_state = list(state)
                new_state[blank_idx], new_state[new_idx] = new_state[new_idx], new_state[blank_idx]
                neighbors.append((tuple(new_state), new_idx))
        return neighbors
 
    # Heuristic distance: for each tile (not the blank), how many rows + cols away it is from where it belongs.
    # Never overestimates the true distance, so A* using it is guaranteed to find the shortest path.
    def h(state):
        total = 0
        for idx, value in enumerate(state):
            if value == 8:
                continue  # skip the blank
            row, col = divmod(idx, 3)
            goal_row, goal_col = divmod(value, 3)  # tile `value` belongs at index `value`
            total += abs(row - goal_row) + abs(col - goal_col)
        return total
 
    # Min-heap of (f_score, tiebreak, state, path_so_far). f = g (moves so far) + h (estimated moves left).
    # Popping the smallest f each time means we always expand the most promising state next.
    counter = itertools.count() 
    open_heap = [(h(start), next(counter), start, [])]
    g_score = {start: 0}  # cheapest known move-count to reach each state
 
    while open_heap:
        f, _, state, path = heapq.heappop(open_heap)
 
        if state == goal:
            return path
 
        current_g = g_score[state]
        for new_state, blank_pos in get_neighbors(state):
            new_g = current_g + 1  # each move costs 1
            # Only explore this neighbor if it's new, or we found a cheaper way to it.
            if new_state not in g_score or new_g < g_score[new_state]:
                g_score[new_state] = new_g
                new_f = new_g + h(new_state)
                heapq.heappush(open_heap, (new_f, next(counter), new_state, path + [blank_pos]))
 
    return []  # no solution found (shouldn't happen for a solvable puzzle)