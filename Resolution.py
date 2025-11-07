
def fol_resolution():
    # Knowledge Base (converted into CNF clauses)
    kb = [
        # John likes all kinds of food
        ['¬Food(x)', 'Likes(John, x)'],

        # Apple and vegetables are food
        ['Food(Apple)'],
        ['Food(Vegetable)'],

        # Anything anyone eats and not killed is food
        ['¬Eats(x, y)', '¬¬Killed(x)', 'Food(y)'],

        # Anil eats peanuts and still alive
        ['Eats(Anil, Peanuts)'],
        ['Alive(Anil)'],

        # Harry eats everything that Anil eats
        ['¬Eats(Anil, x)', 'Eats(Harry, x)'],

        # Anyone who is alive implies not killed
        ['¬Alive(x)', '¬Killed(x)'],

        # Anyone who is not killed implies alive
        ['Killed(x)', 'Alive(x)']
    ]

    # Query (negated for resolution proof)
    query = ['¬Likes(John, Peanuts)']

    # Add negated query to KB
    clauses = kb + [query]

    print("Knowledge Base (Clauses):")
    for c in kb:
        print(" ", c)

    print("\nNegated Query:")
    print(" ", query)

    print("\nStarting Resolution...\n")

    new = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if [] in resolvents:
                print("Derived empty clause ⇒ Query PROVED ✅")
                return True
            for r in resolvents:
                new.add(tuple(r))
        if new.issubset(set(map(tuple, clauses))):
            print("No new clauses ⇒ Query CANNOT be proved ❌")
            return False
        for c in new:
            if list(c) not in clauses:
                clauses.append(list(c))


def resolve(ci, cj):
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = list(set(ci + cj))
                new_clause.remove(di)
                new_clause.remove(dj)
                resolvents.append(new_clause)
    return resolvents


def negate(literal):
    """Negates a literal (adds/removes ¬ symbol)."""
    return literal[1:] if literal.startswith('¬') else '¬' + literal


if __name__ == "__main__":
    fol_resolution()
