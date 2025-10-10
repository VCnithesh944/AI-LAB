import random

def calculate_conflicts(state):
    """Calculate number of attacking pairs of queens."""
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def get_neighbors(state):
    """Generate all possible neighbors by moving one queen per column."""
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if state[col] != row:
                new_state = list(state)
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors


def hill_climbing(n, max_restarts=1000):
    """Solve N-Queens using Hill Climbing with random restarts."""
    for attempt in range(max_restarts):
        current_state = [random.randint(0, n - 1) for _ in range(n)]
        current_h = calculate_conflicts(current_state)

        while True:
            neighbors = get_neighbors(current_state)
            neighbor_h_values = [calculate_conflicts(neighbor) for neighbor in neighbors]
            min_h = min(neighbor_h_values)
            best_neighbor = neighbors[neighbor_h_values.index(min_h)]

            if min_h >= current_h:  # No better neighbor
                break

            current_state = best_neighbor
            current_h = min_h

        if current_h == 0:
            print(f"Solution found after {attempt+1} restarts:")
            return current_state

    print("Failed to find a solution after maximum restarts.")
    return None


def print_board(state):
    """Display the board."""
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()


# Example usage
if __name__ == "__main__":
    N = int(input("Enter number of queens (N): "))
    solution = hill_climbing(N)
    if solution:
        print_board(solution)
