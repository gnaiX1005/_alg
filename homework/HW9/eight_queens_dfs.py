"""
八皇后問題 - 深度優先搜尋 + 回溯（DFS / backtracking）

用法：
    python3 eight_queens_dfs.py

原理：
    棋盤有 8 列，一列一列放皇后，第 r 列放在第 c 行。
    每次放之前檢查這個位置是否安全：
      - 同一個 column 已經有皇后
      - 同一個左上到右下對角線（r - c 相同）已經有皇后
      - 同一個右上到左下對角線（r + c 相同）已經有皇后
    安全就放下去、往下一列遞迴；若後面怎樣都放不下，
    就把這顆皇后拿起來（回溯），換下一個 column 再試。
    走到第 8 列代表找到一組解。

    用三個集合記錄已被佔用的 column 與兩條對角線，
    可以讓「檢查是否安全」變成 O(1)。
"""

N = 8


def solve(n=N):
    solutions = []
    explored = [0]

    def dfs(row, queens, cols, diag1, diag2):
        explored[0] += 1
        if row == n:
            solutions.append(queens[:])
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            queens.append(col)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            dfs(row + 1, queens, cols, diag1, diag2)

            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    dfs(0, [], set(), set(), set())
    return solutions, explored[0]


def draw_board(solution, n=N):
    lines = []
    for row in range(n):
        line = []
        for col in range(n):
            line.append("Q" if solution[row] == col else ".")
        lines.append(" ".join(line))
    return "\n".join(lines)


def main():
    solutions, explored = solve(N)

    print("=== 八皇后問題（DFS 回溯法） ===")
    print(f"棋盤大小: {N} x {N}")
    print(f"遞迴節點數: {explored}")
    print(f"總共找到 {len(solutions)} 組解")
    print()

    print("前 3 組解的棋盤（Q 代表皇后）：")
    for i, sol in enumerate(solutions[:3], 1):
        print(f"--- 第 {i} 組：每列皇后所在的行 = {sol} ---")
        print(draw_board(sol))
        print()

    print("每組解的第一列皇后行號：")
    print([sol[0] for sol in solutions])


if __name__ == "__main__":
    main()
