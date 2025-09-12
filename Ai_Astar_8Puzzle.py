# ------------- Heuristics ---------------- #
def misplaced_tiles(state, goal):
    """Count tiles not in the correct position (Best Fit heuristic)."""
    return sum(1 for i in range(len(state)) if state[i] != 0 and state[i] != goal[i])

def manhattan_distance(state, goal):
    """Sum of Manhattan distances for all tiles."""
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:  # skip blank
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal.index(state[i]), 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# ------------- A* Algorithm ---------------- #
def a_star(start, goal, heuristic="manhattan"):
    # Select heuristic
    if heuristic == "manhattan":
        h = lambda s: manhattan_distance(s, goal)
    elif heuristic == "misplaced":
        h = lambda s: misplaced_tiles(s, goal)
    else:
        raise ValueError("Invalid heuristic: choose 'manhattan' or 'misplaced'")

    # Open and closed sets
    open_set = [(start, [], 0, h(start))]  # (state, path, g, f)
    closed_set = set()

    while open_set:
        # Pick state with minimum f = g+h
        current = min(open_set, key=lambda x: x[2] + x[3])
        open_set.remove(current)

        state, path, g, _ = current

        if tuple(state) in closed_set:
            continue
        closed_set.add(tuple(state))

        # Goal test
        if state == goal:
            return path + [state]

        # Find blank (0) position
        blank = state.index(0)
        x, y = divmod(blank, 3)

        # Possible moves: Up, Down, Left, Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_blank = nx * 3 + ny
                new_state = state[:]
                new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]

                if tuple(new_state) not in closed_set:
                    new_g = g + 1
                    new_h = h(new_state)
                    open_set.append((new_state, path + [state], new_g, new_h))

    return None  # No solution

# ------------- Helper to Print 8 Puzzle ---------------- #
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# ------------- Example Run ---------------- #
if __name__ == "__main__":
    start = [2, 8, 3,
            1, 6, 4,
            7, 0, 5]

    goal = [1, 2, 3,
           8, 0, 4,
           7, 6, 5]

    print("Solving with Manhattan Distance Heuristic:")
    path = a_star(start, goal, heuristic="manhattan")
    if path:
        for step in path:
            print_state(step)

    print("Solving with Misplaced Tiles Heuristic:")
    path = a_star(start, goal, heuristic="misplaced")
    if path:
        for step in path:
            print_state(step)
