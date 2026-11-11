# diff 問題的「非動態規劃」解法：Myers O(ND) 演算法（貪婪最短路徑）
#
# 用法：
#   python3 diff_myers.py                  # 內建示範
#   python3 diff_myers.py 檔案1 檔案2      # 逐行比對兩個檔案
#
# 原理（出自 Myers 1986, "An O(ND) Difference Algorithm and Its Variations"）：
#   把 diff 看成「編輯圖」上的最短路徑問題：
#     - 橫軸 x = 0..n（a 的位置）、縱軸 y = 0..m（b 的位置）
#     - 對角線走法：a[x] == b[y] 時沿對角線前進（相同，不花代價）
#     - 向右：刪除 a[x]（代價 1）；向下：插入 b[y]（代價 1）
#   D = 最小編輯距離 = 最短路徑長度。
#   貪婪做法：d = 0, 1, 2, ... 一層一層擴張，每一層只記錄「每條對角線 k = x-y
#   上走最遠的點」V[k]。因為每步只會從上一層的相鄰對角線過來，所以只要 O(D)
#   個狀態/層，不需要填整個 n*m 表格。走到 (n, m) 那一刻的 d 就是最小編輯距離。
#   再用每一層的 V 快照回溯出完整編輯腳本。
#   時間 O((n+m)*D)，空間 O(D^2)（存 trace）。D 很小（檔案只差幾行）時遠快過
#   動態規劃的 O(n*m)；D 接近 n+m（兩檔幾乎不同）時退化成 O(n^2)。

import sys


def myers_diff(a, b):
    """回傳對齊結果：list of (op, item)，op ∈ {'=', '-', '+'}。"""
    n, m = len(a), len(b)
    max_d = n + m
    v = {1: 0}                      # V[k]：對角線 k 上走最遠的 x
    trace = []                      # 每一層 d 開始前的 V 快照，供回溯

    found_d = None
    for d in range(max_d + 1):
        trace.append(v.copy())
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)          # 從下面（插入）過來
            else:
                x = v.get(k - 1, 0) + 1      # 從左邊（刪除）過來
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x += 1                        # 蛇行：相同元素免費前進
                y += 1
            v[k] = x
            if x >= n and y >= m:
                found_d = d
                break
        if found_d is not None:
            break

    return _backtrack(trace, a, b, found_d)


def _backtrack(trace, a, b, d):
    """從每一層的 V 快照往回走，還原編輯腳本。"""
    x, y = len(a), len(b)
    ops = []
    for dd in range(d, 0, -1):
        v = trace[dd]
        k = x - y
        if k == -dd or (k != dd and v.get(k - 1, -1) < v.get(k + 1, -1)):
            prev_k = k + 1                   # 上一步是插入（往下）
        else:
            prev_k = k - 1                   # 上一步是刪除（往右）
        prev_x = v.get(prev_k, 0)
        prev_y = prev_x - prev_k

        while x > prev_x and y > prev_y:     # 沿對角線退回（相同元素）
            x -= 1
            y -= 1
            ops.append(('=', a[x]))
        if x == prev_x:                      # 往下 = 插入 b[y-1]
            y -= 1
            ops.append(('+', b[y]))
        else:                                # 往右 = 刪除 a[x-1]
            x -= 1
            ops.append(('-', a[x]))
    while x > 0 and y > 0:                   # d = 0 的對角線剩餘部分
        x -= 1
        y -= 1
        ops.append(('=', a[x]))
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
        ops = myers_diff(a, b)
        show_diff(f"Myers O(ND)：{sys.argv[1]} vs {sys.argv[2]}", ops)
    else:
        print("===== 1. 字元層級示範（Myers 經典論文例子）=====")
        a, b = "ABCABBA", "CBABAC"
        show_diff(f"Myers O(ND)：{a!r} vs {b!r}", myers_diff(a, b))

        print("===== 2. 行層級示範 =====")
        old = ["the quick brown fox", "jumps over", "the lazy dog"]
        new = ["the quick brown fox", "leaps past", "the lazy dog", "and runs away"]
        show_diff("Myers O(ND)：舊檔 vs 新檔", myers_diff(old, new))

        print("===== 3. 逐 d 層擴張過程（同上例）=====")
        n, m = len(old), len(new)
        v = {1: 0}
        done_at = None
        for d in range(6):
            layer = []
            for k in range(-d, d + 1, 2):
                if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                    x = v.get(k + 1, 0)
                else:
                    x = v.get(k - 1, 0) + 1
                y = x - k
                while x < n and y < m and old[x] == new[y]:
                    x += 1
                    y += 1
                v[k] = x
                layer.append(f"k={k:>2} -> ({x},{y})")
                if x >= n and y >= m and done_at is None:
                    done_at = (d, k, x, y)
            print(f"  d={d}: " + "   ".join(layer))
            if done_at is not None and done_at[0] == d:
                print(f"  -> d={d} 時 k={done_at[1]} 線上的 ({n},{m}) 終點被抵達，"
                      f"最小編輯距離 D={d}，停止擴張")
                break
