# Forward Reasoning (Forward Chaining) in First Order Logic
# Example: Criminal(Robert) Proof

# Knowledge Base: Represented as Horn clauses (IF conditions THEN conclusion)

from collections import defaultdict

# Rule representation: (premises, conclusion)
rules = [
    # Rule 1: If American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z) → Criminal(x)
    (["American(x)", "Weapon(y)", "Sells(x,y,z)", "Hostile(z)"], "Criminal(x)"),

    # Rule 2: Missile(x) → Weapon(x)
    (["Missile(x)"], "Weapon(x)"),

    # Rule 3: Enemy(x, America) → Hostile(x)
    (["Enemy(x,America)"], "Hostile(x)"),

    # Rule 7: Missile(x) & Owns(A,x) → Sells(Robert,x,A)
    (["Missile(x)", "Owns(A,x)"], "Sells(Robert,x,A)")
]

# Facts (initial knowledge base)
facts = {
    "American(Robert)",
    "Enemy(A,America)",
    "Owns(A,t1)",
    "Missile(t1)"
}

# Forward Chaining function
def forward_chaining(rules, facts, query):
    inferred = set(facts)
    new_fact_added = True

    print("Initial Facts:")
    for f in facts:
        print("  ", f)
    print("\n--- Forward Chaining Reasoning ---")

    while new_fact_added:
        new_fact_added = False

        for premises, conclusion in rules:
            # Try to find substitutions that make the premises true
            for fact in list(inferred):
                for premise in premises:
                    # Naive variable substitution matching
                    if "(" in premise:
                        # Example: Missile(x) vs Missile(t1)
                        pred_prem, args_prem = premise.split("(")
                        pred_fact, args_fact = fact.split("(")
                        if pred_prem == pred_fact:
                            vars_prem = args_prem.strip(")").split(",")
                            vals_fact = args_fact.strip(")").split(",")

                            # Create substitution mapping
                            substitution = dict(zip(vars_prem, vals_fact))

                            # Check if all premises hold under this substitution
                            all_true = True
                            for p in premises:
                                temp = p
                                for k, v in substitution.items():
                                    temp = temp.replace(k, v)
                                if temp not in inferred:
                                    all_true = False
                                    break

                            # If all premises are true, infer conclusion
                            if all_true:
                                new_conclusion = conclusion
                                for k, v in substitution.items():
                                    new_conclusion = new_conclusion.replace(k, v)

                                if new_conclusion not in inferred:
                                    inferred.add(new_conclusion)
                                    new_fact_added = True
                                    print(f"Inferred: {new_conclusion}  from {premises}")

    print("\nFinal Facts:")
    for f in sorted(inferred):
        print("  ", f)

    print("\nQuery:", query)
    if query in inferred:
        print("✅ Query is TRUE – proven by forward chaining.")
    else:
        print("❌ Query cannot be proven from the knowledge base.")

# Run the reasoning
query = "Criminal(Robert)"
forward_chaining(rules, facts, query)
