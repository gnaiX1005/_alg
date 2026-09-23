import itertools

# SAT 問題：給一個布林公式，找一組變數賦值讓公式為真
# 暴力法：窮舉所有 2^n 組賦值（n 個變數），一一代入檢查
# 公式以 CNF（合取範式）表示：AND of OR clauses
# 範例：(x1 or x2) AND (not x1 or x3) AND (not x2 or not x3)
# 表示成：[[1, 2], [-1, 3], [-2, -3]]


def clause_satisfied(clause, assignment):
    for lit in clause:
        var = abs(lit)
        is_true = assignment[var] if lit > 0 else not assignment[var]
        if is_true:
            return True
    return False


def formula_satisfied(formula, assignment):
    return all(clause_satisfied(c, assignment) for c in formula)


def print_truth_table(formula, variables):
    print("真值表（每個 variable 一欄 + 最後一欄為公式結果）：")
    header = variables + ["公式結果"]
    print("  ".join(f"{v:>4}" for v in header))
    for assign in itertools.product([True, False], repeat=len(variables)):
        a = {var: val for var, val in zip(variables, assign)}
        r = formula_satisfied(formula, a)
        row = "  ".join(f"{str(int(a[v])):>4}" for v in variables) + f"{str(int(r)):>8}"
        print(row)


def brute_sat(formula, variables):
    print(f"共有 {len(variables)} 個變數，需窮舉 2^{len(variables)} = {2 ** len(variables)} 種組合\n")
    solutions = []
    for assign in itertools.product([True, False], repeat=len(variables)):
        a = {var: val for var, val in zip(variables, assign)}
        if formula_satisfied(formula, a):
            solutions.append(a)
    return solutions


if __name__ == "__main__":
    # 範例公式：(x1 or x2) AND (not x1 or x3) AND (not x2 or not x3)
    formula = [[1, 2], [-1, 3], [-2, -3]]
    variables = [1, 2, 3]

    print("公式：(x1 OR x2) AND (~x1 OR x3) AND (~x2 OR ~x3)\n")
    print_truth_table(formula, variables)
    print()

    solutions = brute_sat(formula, variables)
    print(f"滿足條件的賦值（SAT）共 {len(solutions)} 組：")
    for s in solutions:
        print("  ", {f"x{v}": int(s[v]) for v in variables})

    if solutions:
        print("\n=> 此公式可滿足（SAT）")
    else:
        print("\n=> 此公式不可滿足（UNSAT）")