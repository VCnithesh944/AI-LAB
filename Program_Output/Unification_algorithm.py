import re
from typing import List, Dict, Optional, Tuple

# ----------------------------
# TERM CLASSES
# ----------------------------

class Term:
    pass

class Var(Term):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return self.name

class Const(Term):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return self.name

class Func(Term):
    def __init__(self, name: str, args: List[Term]):
        self.name = name
        self.args = args
    def __repr__(self):
        if not self.args:
            return self.name
        return f"{self.name}({', '.join(map(repr, self.args))})"


# ----------------------------
# PARSER
# ----------------------------

def parse_term(s: str) -> Term:
    s = s.replace(" ", "")
    return _parse(s)


def _parse(s: str) -> Term:
    # variable: lowercase single letter or word starting with lowercase
    if re.fullmatch(r"[a-z]\w*", s):
        return Var(s)

    # constant: uppercase single token / word
    if re.fullmatch(r"[A-Z]\w*", s):
        return Const(s)

    # function or predicate: name(args...)
    m = re.match(r"(\w+)\((.*)\)", s)
    if m:
        name = m.group(1)
        inside = m.group(2)

        # split args by commas (handle nested parentheses)
        args = []
        depth = 0
        arg = ""
        for c in inside:
            if c == ',' and depth == 0:
                args.append(parse_term(arg))
                arg = ""
            else:
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                arg += c
        if arg:
            args.append(parse_term(arg))
        return Func(name, args)

    raise ValueError(f"Cannot parse term: {s}")


# ----------------------------
# SUBSTITUTION HELPERS
# ----------------------------

Subst = Dict[str, Term]

def apply_subst(t: Term, subst: Subst) -> Term:
    if isinstance(t, Var):
        if t.name in subst:
            return apply_subst(subst[t.name], subst)
        return t
    if isinstance(t, Const):
        return t
    if isinstance(t, Func):
        return Func(t.name, [apply_subst(arg, subst) for arg in t.args])
    return t

def occurs_check(var: Var, term: Term, subst: Subst) -> bool:
    term = apply_subst(term, subst)
    if isinstance(term, Var):
        return var.name == term.name
    if isinstance(term, Func):
        return any(occurs_check(var, arg, subst) for arg in term.args)
    return False

def compose_subst(s1: Subst, s2: Subst) -> Subst:
    result = {v: apply_subst(t, s1) for v, t in s2.items()}
    result.update(s1)
    return result


# ----------------------------
# UNIFIER
# ----------------------------

def unify(t1: Term, t2: Term, subst: Optional[Subst] = None) -> Optional[Subst]:
    if subst is None:
        subst = {}
    pairs = [(t1, t2)]
    s = dict(subst)

    while pairs:
        a, b = pairs.pop()
        a = apply_subst(a, s)
        b = apply_subst(b, s)

        if repr(a) == repr(b):
            continue

        # variable cases
        if isinstance(a, Var):
            if occurs_check(a, b, s):
                return None
            s = compose_subst({a.name: b}, s)
            continue

        if isinstance(b, Var):
            if occurs_check(b, a, s):
                return None
            s = compose_subst({b.name: a}, s)
            continue

        # constant mismatch
        if isinstance(a, Const) and isinstance(b, Const):
            if a.name != b.name:
                return None
            continue

        # function mismatch
        if isinstance(a, Func) and isinstance(b, Func):
            if a.name != b.name or len(a.args) != len(b.args):
                return None
            pairs.extend(list(zip(a.args, b.args)))
            continue

        return None

    return s


# ----------------------------
# OUTPUT FORMATTER
# ----------------------------

def format_subst(subst: Optional[Subst]) -> str:
    if subst is None:
        return "FAIL (no unifier)"
    if not subst:
        return "{} (empty substitution)"
    items = [f"{v} -> {repr(apply_subst(t, subst))}" for v, t in subst.items()]
    return "{" + ", ".join(items) + "}"


# ----------------------------
# DEFAULT QUESTIONS
# ----------------------------

EXAMPLES = [
    ("Eats(x, Apple)", "Eats(Riya, y)"),
    ("p(f(a), g(Y))", "p(X, X)"),
    ("Knows(John, x)", "Knows(x, Elisabeth)"),
    ("f(x, g(y))", "f(g(z), g(a))"),
    ("P(x, h(y))", "P(a, f(z))"),
    ("Ancestor(x, Father(x))", "Ancestor(Father(John), y)"),
    ("f(x,x)", "f(a,b)"),
    ("Knows(x, x)", "Knows(John, y)")
]


# ----------------------------
# MAIN EXECUTION
# ----------------------------

print("\nUNIFICATION RESULTS:\n")

for a_str, b_str in EXAMPLES:
    A = parse_term(a_str)
    B = parse_term(b_str)
    result = unify(A, B)
    print(f"{a_str}  =?=  {b_str}\n  => {format_subst(result)}\n")
