"""
IC 設計中的電路繞線問題 - 多種搜尋法比較

用法：
    python3 ic_routing.py

原理：
    把晶片的繞線區域看成格子圖，每個格子是可用空間，'#' 是障礙物。
    一條連線（net）要從端點走到另一個端點，只能上下左右移動，
    不可以穿過障礙物，也不可以和其他已完成的線重疊。
    本程式依序繞兩條線：
        net1: A -> B
        net2: C -> D
    每條線分別用四種方法找路徑：
        1. Lee maze routing：BFS，一圈一圈擴張，保證最短。
        2. Dijkstra：以距離為成本的最短路徑（均勻成本時結果同 BFS）。
        3. A*：Dijkstra + 曼哈頓距離啟發式，展開最少格子。
        4. 貪婪最佳優先（Greedy Best-First）：只看 h，跑得快但不保證最短。
    第一條線繞完後，把它走過的格子當成障礙物，再繞第二條線（避免短路）。
"""

import heapq
from collections import deque

GRID = [
    "...............",
    "..###..........",
    "..#..#....A....",
    "..#..#.........",
    ".....######....",
    "...............",
    ".C.............",
    "...............",
    ".............B.",
    ".D.............",
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上、下、左、右


def find(grid, ch):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
    return None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid, cur, blocked):
    rows, cols = len(grid), len(grid[0])
    r, c = cur
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        nxt = (nr, nc)
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue
        if grid[nr][nc] == "#" or nxt in blocked:
            continue
        yield nxt


def rebuild(parent, goal):
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def lee(grid, start, goal, blocked):
    """BFS / Lee maze routing：第 1 次抵達目標即最短。"""
    queue = deque([start])
    parent = {start: None}
    explored = 0

    while queue:
        cur = queue.popleft()
        explored += 1
        if cur == goal:
            return rebuild(parent, goal), explored
        for nxt in neighbors(grid, cur, blocked):
            if nxt not in parent:
                parent[nxt] = cur
                queue.append(nxt)
    return None, explored


def dijkstra(grid, start, goal, blocked):
    heap = [(0, start)]
    dist = {start: 0}
    parent = {start: None}
    explored = 0

    while heap:
        d, cur = heapq.heappop(heap)
        if d > dist.get(cur, float("inf")):
            continue
        explored += 1
        if cur == goal:
            return rebuild(parent, goal), explored
        for nxt in neighbors(grid, cur, blocked):
            nd = d + 1
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                parent[nxt] = cur
                heapq.heappush(heap, (nd, nxt))
    return None, explored


def astar(grid, start, goal, blocked):
    heap = [(heuristic(start, goal), 0, start)]
    best_g = {start: 0}
    parent = {start: None}
    explored = 0

    while heap:
        f, g, cur = heapq.heappop(heap)
        if g > best_g.get(cur, float("inf")):
            continue
        explored += 1
        if cur == goal:
            return rebuild(parent, goal), explored
        for nxt in neighbors(grid, cur, blocked):
            ng = g + 1
            if ng < best_g.get(nxt, float("inf")):
                best_g[nxt] = ng
                parent[nxt] = cur
                heapq.heappush(heap, (ng + heuristic(nxt, goal), ng, nxt))
    return None, explored


def greedy_best_first(grid, start, goal, blocked):
    """只看 h(n)，不保證最短，但通常展開很少格子。"""
    heap = [(heuristic(start, goal), start)]
    visited = {start}
    parent = {start: None}
    explored = 0

    while heap:
        h, cur = heapq.heappop(heap)
        explored += 1
        if cur == goal:
            return rebuild(parent, goal), explored
        for nxt in neighbors(grid, cur, blocked):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                heapq.heappush(heap, (heuristic(nxt, goal), nxt))
    return None, explored


ALGORITHMS = [
    ("Lee (BFS)", lee),
    ("Dijkstra", dijkstra),
    ("A*", astar),
    ("Greedy Best-First", greedy_best_first),
]


def route_all(algo):
    """用同一種演算法依序繞 net1、net2，回傳結果。"""
    blocked = set()
    results = []

    for name, start_ch, goal_ch in [("net1", "A", "B"), ("net2", "C", "D")]:
        start, goal = find(GRID, start_ch), find(GRID, goal_ch)
        path, explored = algo(GRID, start, goal, blocked)
        if path is None:
            results.append((name, start_ch, goal_ch, None, explored))
            continue
        results.append((name, start_ch, goal_ch, path, explored))
        # 把這條線走過的格子設為障礙，避免下一條線重疊（端點除外）
        blocked.update(p for p in path if p not in (start, goal))

    return results


def draw(all_paths):
    canvas = [list(row) for row in GRID]
    markers = ["*", "+"]
    for path, marker in zip(all_paths, markers):
        if path is None:
            continue
        for r, c in path:
            if canvas[r][c] in (".", "*", "+"):
                canvas[r][c] = marker
    return "\n".join("".join(row) for row in canvas)


def main():
    print("=== IC 電路繞線（多種搜尋法） ===")
    print()
    print("原始繞線區域（A/B 與 C/D 是兩條線的端點，# 是障礙物）：")
    print("\n".join(GRID))
    print()

    summary = {}

    for algo_name, algo in ALGORITHMS:
        results = route_all(algo)
        summary[algo_name] = results

        print(f"----- {algo_name} -----")
        for name, s, g, path, explored in results:
            if path is None:
                print(f"  {name} {s}->{g}: 繞線失敗（拜訪 {explored} 格）")
            else:
                print(f"  {name} {s}->{g}: 長度 {len(path) - 1} 步，"
                      f"拜訪 {explored} 格")
        paths = [r[3] for r in results]
        if all(p is not None for p in paths):
            print("  繞線結果（* 是 net1，+ 是 net2）：")
            for line in draw(paths).splitlines():
                print("    " + line)
        print()

    print("----- 綜合比較 -----")
    print(f"{'方法':<20}{'net1 長度':>10}{'net2 長度':>10}{'總長度':>8}")
    for algo_name, _ in ALGORITHMS:
        lengths = [0 if r[3] is None else len(r[3]) - 1 for r in summary[algo_name]]
        total = sum(lengths)
        print(f"{algo_name:<20}{lengths[0]:>10}{lengths[1]:>10}{total:>8}")

    print()
    print("說明：BFS/Dijkstra/A* 都保證最短；Greedy 只看估計值，可能較長。")


if __name__ == "__main__":
    main()
