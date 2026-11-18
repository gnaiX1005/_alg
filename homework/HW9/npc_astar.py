"""
NPC 搜尋玩家問題 - A* 演算法

用法：
    python3 npc_astar.py

原理：
    把地圖看成格子圖，NPC 要從自己的位置走到玩家所在位置，
    只能上下左右移動，不能穿牆。
    A* 對每個格子估計「通過這個格子到目標的總成本」：
        f(n) = g(n) + h(n)
      - g(n)：從起點走到 n 已經走的步數
      - h(n)：從 n 到目標的估計步數，這裡用曼哈頓距離
              |r - r_goal| + |c - c_goal|
    每次從待探索的格子中挑 f 最小的優先展開（用 min-heap），
    因此會比盲目 BFS 少拜訪很多格子，又能保證找到最短路徑。

    程式同時跑一次 BFS 當對照，比較兩者拜訪的格子數。
"""

import heapq
from collections import deque

GRID = [
    "..........",
    ".N..#.....",
    "....#..P..",
    ".#..#.....",
    ".#........",
    ".#..###...",
    "....#.....",
    "..........",
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右


def find(grid, ch):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
    return None


def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_heap = [(heuristic(start, goal), 0, start)]
    g_score = {start: 0}
    parent = {start: None}
    explored = []

    while open_heap:
        f, g, cur = heapq.heappop(open_heap)
        if cur in explored:
            continue
        explored.append(cur)

        if cur == goal:
            return build_path(parent, goal), explored

        r, c = cur
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#":
                continue
            ng = g + 1
            if ng < g_score.get(nxt, float("inf")):
                g_score[nxt] = ng
                parent[nxt] = cur
                heapq.heappush(open_heap, (ng + heuristic(nxt, goal), ng, nxt))

    return None, explored


def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    parent = {start: None}
    explored = []

    while queue:
        cur = queue.popleft()
        explored.append(cur)
        if cur == goal:
            return build_path(parent, goal), explored

        r, c = cur
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "#" or nxt in parent:
                continue
            parent[nxt] = cur
            queue.append(nxt)

    return None, explored


def build_path(parent, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def draw(grid, path):
    canvas = [list(row) for row in grid]
    for r, c in path:
        if canvas[r][c] not in ("N", "P"):
            canvas[r][c] = "*"
    return "\n".join("".join(row) for row in canvas)


def main():
    start = find(GRID, "N")
    goal = find(GRID, "P")

    path, a_explored = astar(GRID, start, goal)
    bfs_path, b_explored = bfs(GRID, start, goal)

    print("=== NPC 搜尋玩家（A* 演算法） ===")
    print(f"NPC 位置: {start}   玩家位置: {goal}")
    print()
    print("地圖（N=NPC，P=玩家，#=牆）：")
    print("\n".join(GRID))
    print()

    if path is None:
        print("NPC 找不到玩家")
        return

    print("A* 找到的最短路徑（* 代表 NPC 走的路）：")
    print(draw(GRID, path))
    print()
    print(f"A* 路徑長度: {len(path) - 1} 步")
    print(f"A* 拜訪格子數: {len(a_explored)}")
    print(f"BFS 拜訪格子數: {len(b_explored)}（對照組）")
    print(f"兩者路徑長度相同: {len(path) == len(bfs_path)}")
    print(f"路徑座標: {path}")


if __name__ == "__main__":
    main()
