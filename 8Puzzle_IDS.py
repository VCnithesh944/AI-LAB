from collections import deque

# Manhattan Distance (for display purpose)
def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            current_row, current_col = i // 3, i % 3
            goal_index = goal.index(state[i])
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

# Goal state
goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)  # 0 = blank tile

# Print 3x3 grid
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Find neighbors
def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = index // 3, index % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dx, dy in moves:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(tuple(new_state))
    return neighbors

# Check if puzzle is solvable
def is_solvable(state):
    arr = [x for x in state if x != 0]
    inversions = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions % 2 == 0

# Depth-Limited Search (recursive)
def depth_limited_search(state, goal, depth_limit, path, visited):
    if state == goal:
        return path

    if depth_limit == 0:
        return None

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            result = depth_limited_search(neighbor, goal, depth_limit - 1, path + [neighbor], visited)
            if result is not None:
                return result

    return None

# Iterative Deepening Search
def iterative_deepening_search(start, goal, max_depth=30):
    for depth in range(max_depth + 1):
        visited = set()
        print(f"\n🔹 Searching at depth limit: {depth}")
        result = depth_limited_search(start, goal, depth, [start], visited)
        if result is not None:
            print(f"✅ Solution found at depth {depth}!")
            return result
    print("❌ Reached max depth limit. No solution found.")
    return None

# Main function
def main():
    print("8-Puzzle Problem using Iterative Deepening Search (IDS)\n")
    print("Enter the start state as 9 numbers (0 for blank):")
    # Example input: 1 2 3 4 0 6 7 5 8
    start = tuple(map(int, input().strip().split()))

    print("\nStart State:")
    print_puzzle(start)
    print("Goal State:")
    print_puzzle(goal_state)

    # Check solvability
    if not is_solvable(start):
        print("❌ This puzzle configuration is unsolvable.")
        return

    solution_path = iterative_deepening_search(start, goal_state)

    if solution_path:
        print(f"\n✅ Solution found in {len(solution_path) - 1} moves:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_puzzle(state)
    else:
        print("❌ No solution found within depth limit.")

if __name__ == "__main__":
    main()
