"""
老鼠走迷宮問題 - 深度優先搜尋（DFS）

用法：
    python3 maze_dfs.py

原理：
    從起點 S 出發，沿著「下、右、上、左」的順序往相鄰格子走，
    走過的格子標記為已拜訪。遇到牆壁、邊界或走過的格子就退回上一格，
    換下一個方向再試。這就是遞迴式的回溯法（DFS + backtracking）。
    一旦走到終點 E，就沿著遞迴回傳的路徑把答案組出來。
"""

MAZE = [
    "S.#......",
    ".#..#.#..",
    ".#.#...#.",
    "...#.#.#.",
    "##...#...",
    "...#.....",
    "..#..#.E.",
]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 下、右、上、左


def find_start_end(maze):
    start = end = None
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    return start, end


def dfs(maze, cur, end, visited, path, explored):
    """遞迴 DFS，找到終點就回傳 True，並把路徑留在 path 裡。"""
    if cur == end:
        path.append(cur)
        return True

    visited.add(cur)
    explored.append(cur)
    r, c = cur

    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        nxt = (nr, nc)
        if not (0 <= nr < len(maze) and 0 <= nc < len(maze[0])):
            continue
        if maze[nr][nc] == "#" or nxt in visited:
            continue
        if dfs(maze, nxt, end, visited, path, explored):
            path.append(cur)
            return True

    return False


def draw(maze, path):
    grid = [list(row) for row in maze]
    for r, c in path:
        if grid[r][c] not in ("S", "E"):
            grid[r][c] = "*"
    return "\n".join("".join(row) for row in grid)


def main():
    start, end = find_start_end(MAZE)
    visited, path, explored = set(), [], []
    found = dfs(MAZE, start, end, visited, path, explored)
    path.reverse()

    print("=== 老鼠走迷宮（DFS） ===")
    print(f"起點: {start}  終點: {end}")
    print(f"拜訪格子數: {len(explored)}")
    print()
    print("原始迷宮：")
    print("\n".join(MAZE))
    print()

    if not found:
        print("找不到從 S 到 E 的路徑")
        return

    print("DFS 找到的路徑（* 代表走過的路）：")
    print(draw(MAZE, path))
    print()
    print(f"路徑長度: {len(path)} 格（步數 {len(path) - 1}）")
    print(f"路徑座標: {path}")


if __name__ == "__main__":
    main()
