"""
狼、羊、甘藍菜過河問題 - 廣度優先搜尋（BFS）

用法：
    python3 wolf_goat_cabbage_bfs.py

原理：
    把「農夫、狼、羊、甘藍菜分別在哪一岸」編碼成一個狀態，
    例如 (0, 0, 0, 0) 代表全部都在左岸，1 代表右岸。
    每次農夫划船可以自己走，或帶一樣東西一起走。
    移動後若某一岸在沒有農夫看管時出現「狼+羊」或「羊+甘藍菜」，
    這個狀態就不合法（羊會被吃掉）。
    用 BFS 一層一層擴張，第一次抵達目標狀態 (1,1,1,1) 的路徑
    就是最少渡河次數的解。
"""

from collections import deque

NAMES = ["農夫", "狼", "羊", "甘藍菜"]
START = (0, 0, 0, 0)
GOAL = (1, 1, 1, 1)


def is_valid(state):
    """檢查某一岸在沒有農夫時，是否留下會被吃掉的組合。"""
    farmer, wolf, goat, cabbage = state
    # 狼和羊同岸、農夫不在 -> 羊被吃
    if wolf == goat and farmer != wolf:
        return False
    # 羊和甘藍菜同岸、農夫不在 -> 甘藍菜被吃
    if goat == cabbage and farmer != goat:
        return False
    return True


def next_states(state):
    """回傳所有合法的下一步狀態，以及這一步的動作說明。"""
    farmer = state[0]
    results = []

    # 農夫自己過河
    new_state = list(state)
    new_state[0] = 1 - farmer
    new_state = tuple(new_state)
    if is_valid(new_state):
        results.append((new_state, "農夫自己過河"))

    # 農夫帶一樣東西過河
    for i in range(1, 4):
        if state[i] == farmer:  # 東西必須跟農夫在同一岸才能帶走
            new_state = list(state)
            new_state[0] = 1 - farmer
            new_state[i] = 1 - farmer
            new_state = tuple(new_state)
            if is_valid(new_state):
                results.append((new_state, f"農夫帶{NAMES[i]}過河"))

    return results


def solve():
    queue = deque([START])
    parent = {START: (None, None)}   # state -> (上一個狀態, 動作)
    visited_order = []

    while queue:
        state = queue.popleft()
        visited_order.append(state)

        if state == GOAL:
            # 回溯出整條路徑
            path = []
            cur = state
            while parent[cur][0] is not None:
                path.append((cur, parent[cur][1]))
                cur = parent[cur][0]
            path.reverse()
            return path, len(parent), visited_order

        for nxt, action in next_states(state):
            if nxt not in parent:
                parent[nxt] = (state, action)
                queue.append(nxt)

    return None, len(parent), visited_order


def side(state):
    """把狀態印成「左岸 / 右岸」兩欄。"""
    left = [NAMES[i] for i in range(4) if state[i] == 0]
    right = [NAMES[i] for i in range(4) if state[i] == 1]
    return "、".join(left) if left else "（空）", "、".join(right) if right else "（空）"


def main():
    path, visited_count, visited_order = solve()

    print("=== 狼、羊、甘藍菜過河（BFS） ===")
    print(f"合法狀態總數: {visited_count}")
    print(f"BFS 拜訪狀態數: {len(visited_order)}")
    print()

    left, right = side(START)
    print(f"初始：左岸[{left}]  右岸[{right}]")
    print()

    if path is None:
        print("無解")
        return

    for step, (state, action) in enumerate(path, 1):
        left, right = side(state)
        print(f"第 {step} 步：{action}")
        print(f"        左岸[{left}]  右岸[{right}]")

    print()
    print(f"總共需要渡河 {len(path)} 次，即找到最少步數解。")


if __name__ == "__main__":
    main()
