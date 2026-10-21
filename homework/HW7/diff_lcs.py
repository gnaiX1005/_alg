# diff 問題的「動態規劃」解法：LCS（最長共同子序列）
#
# 用法：
#   python3 diff_lcs.py                  # 內建示範
#   python3 diff_lcs.py 檔案1 檔案2      # 逐行比對兩個檔案
#
# 原理：
#   dp[i][j] = a 的前 i 個元素與 b 的前 j 個元素的 LCS 長度。
#   轉移式：
#     a[i-1] == b[j-1]  -> dp[i][j] = dp[i-1][j-1] + 1   （接在後面）
#     否則              -> dp[i][j] = max(dp[i-1][j], dp[i][j-1])
#   從 dp[n][m] 回溯即可還原出對齊結果；刪除數 + 插入數 = 最小編輯距離
#   （單純插入/刪除的情況下 D = n + m - 2 * LCS）。
#   時間 O(n*m)，空間 O(n*m)。

import sys


def lcs_table(a, b):
    """建立 LCS 長度表 dp，dp[i][j] = len(LCS(a[:i], b[:j]))。"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i - 1][j] if dp[i - 1][j] >= dp[i][j - 1] else dp[i][j - 1]
    return dp


def diff_lcs(a, b):
    """回傳對齊結果：list of (op, item)，op ∈ {'=', '-', '+'}。"""
    dp = lcs_table(a, b)
    ops = []
    i, j = len(a), len(b)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append(('=', a[i - 1]))          # 相同：沿對角線回溯
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            ops.append(('+', b[j - 1]))          # 插入 b[j-1]
            j -= 1
        else:
            ops.append(('-', a[i - 1]))          # 刪除 a[i-1]
            i -= 1
    ops.reverse()
    return ops


def show_diff(title, ops):
    """以類似 unified diff 的格式印出對齊結果與統計。"""
    same = sum(1 for op, _ in ops if op == '=')
    dele = sum(1 for op, _ in ops if op == '-')
    ins = sum(1 for op, _ in ops if op == '+')
    print(f"----- {title} -----")
    for op, item in ops:
        print(f"  {op} {item}")
    print(f"  共同 {same} 行、刪除 {dele} 行、插入 {ins} 行"
          f"  ->  最小編輯距離（刪+插）= {dele + ins}\n")
    return dele + ins


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


if __name__ == "__main__":
    if len(sys.argv) == 3:                      # 檔案模式
        a, b = read_lines(sys.argv[1]), read_lines(sys.argv[2])
        ops = diff_lcs(a, b)
        show_diff(f"LCS 動態規劃：{sys.argv[1]} vs {sys.argv[2]}", ops)
    else:
        print("===== 1. 字元層級示範（Myers 經典論文例子）=====")
        a, b = "ABCABBA", "CBABAC"
        show_diff(f"LCS 動態規劃：{a!r} vs {b!r}", diff_lcs(a, b))

        print("===== 2. 行層級示範 =====")
        old = ["the quick brown fox", "jumps over", "the lazy dog"]
        new = ["the quick brown fox", "leaps past", "the lazy dog", "and runs away"]
        show_diff("LCS 動態規劃：舊檔 vs 新檔", diff_lcs(old, new))

        print("===== 3. 動態規劃表（小例子）=====")
        a, b = "ABCAB", "BACAB"
        dp = lcs_table(a, b)
        print(f"    a = {a}, b = {b}")
        print("        " + "  ".join(f"{c:>2}" for c in " " + b))
        for i in range(len(a) + 1):
            row = f"{a[i-1] if i else ' ':>2}" if i else "  "
            print(f"    {row:>3}  " + "  ".join(f"{dp[i][j]:>2}" for j in range(len(b) + 1)))
        print(f"    LCS 長度 = {dp[len(a)][len(b)]}"
              f"  ->  編輯距離 = {len(a) + len(b) - 2 * dp[len(a)][len(b)]}")
