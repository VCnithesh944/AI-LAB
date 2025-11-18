import math

# -------- DECLARE TREE EXACTLY AS NUMERIC LEAF PAIRS -------- #
tree = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H", "I"],
    "E": ["J", "K"],
    "F": ["L", "M"],
    "G": ["N", "O"],

    # FINAL UPDATED LEAF VALUES
    "H": [41, 5],
    "I": [12, 90],
    "J": [101, 80],
    "K": [20, 30],
    "L": [34, 80],
    "M": [36, 35],
    "N": [50, 36],
    "O": [25, 3]
}

best_path = []
pruned = []


def is_leaf(node):
    """Return True if node is a numeric leaf pair."""
    return isinstance(tree[node], (list, tuple)) and \
           all(isinstance(x, (int, float)) for x in tree[node])


def alphabeta(node, is_max, alpha, beta, path):
    global best_path

    # ------- LEAF FIX (WORKS ALWAYS) -------- #
    if is_leaf(node):
        return max(tree[node]) if is_max else min(tree[node])

    # ------- INTERNAL NODE ------- #
    value = -math.inf if is_max else math.inf
    chosen = None

    for child in tree[node]:

        child_value = alphabeta(child, not is_max, alpha, beta, path + [child])

        if is_max:
            if child_value > value:
                value = child_value
                chosen = path + [child]
            alpha = max(alpha, value)

        else:  # MIN node
            if child_value < value:
                value = child_value
                chosen = path + [child]
            beta = min(beta, value)

        # ---- PRUNING ---- #
        if beta <= alpha:
            pruned.append((node, child))
            break

    # Save best path at root only
    if path == ["A"] and chosen:
        best_path = chosen

    return value


# -------- RUN -------- #
final_value = alphabeta("A", True, -math.inf, math.inf, ["A"])


# -------- OUTPUT -------- #
print("\n======== ALPHA–BETA PRUNING RESULT ========\n")

print("Final Maximum Value at Root (A):", final_value, "\n")

print("Best Path from Root to Leaf:")
print(" → ".join(best_path), "→", final_value, "\n")

print("Pruned Branches (Cut-Offs):")
if not pruned:
    print("No branches pruned.")
else:
    for p in pruned:
        print(f"- Pruned under {p[0]} when exploring {p[1]}")

print("\n===========================================\n")
