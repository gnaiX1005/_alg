# 比較兩種 diff 解法：LCS（動態規劃） vs Myers O(ND)（非動態規劃）
#
# 用法： python3 compare.py
#
# 1. 正確性：隨機產生多組字串，檢查兩種演算法算出的最小編輯距離是否一致，
#    且兩者回溯出的編輯腳本套用後都能把 a 變成 b。
# 2. 效能：在「差異很小」與「差異很大」兩種情境下計時，觀察 O(n*m) 與 O((n+m)*D)
#    的實際差異。

import random
import time

from diff_lcs import diff_lcs
from diff_myers import myers_diff


def distance(ops):
    return sum(1 for op, _ in ops if op in ('-', '+'))


def apply_ops(a, ops):
    """把編輯腳本套回 a，確認結果等於 b。"""
    out = []
    for op, item in ops:
        if op == '=':
            out.append(item)
        elif op == '+':
            out.append(item)
    return out


def check_ops(a, b, ops):
    """等號處必須與 a 一致，'-+' 處必須合成 b。"""
    i = 0
    out = []
    for op, item in ops:
        if op == '=':
            if i >= len(a) or a[i] != item:
                return False
            out.append(item)
            i += 1
        elif op == '-':
            if i >= len(a) or a[i] != item:
                return False
            i += 1
        else:
            out.append(item)
    return i == len(a) and out == list(b)


def rand_str(n, alphabet):
    return ''.join(random.choice(alphabet) for _ in range(n))


def main():
    random.seed(7)

    print("===== 1. 正確性驗證（隨機 300 組）=====")
    ok = True
    for t in range(300):
        n = random.randint(0, 30)
        m = random.randint(0, 30)
        a = rand_str(n, "ABCD")
        b = rand_str(m, "ABCD")
        ops1 = diff_lcs(a, b)
        ops2 = myers_diff(a, b)
        d1, d2 = distance(ops1), distance(ops2)
        if d1 != d2 or not check_ops(a, b, ops1) or not check_ops(a, b, ops2):
            ok = False
            print(f"  不一致！a={a!r} b={b!r} LCS距離={d1} Myers距離={d2}")
            break
    print(f"  兩種演算法 300 組最小編輯距離全數一致、腳本皆可還原：{ok}\n")

    print("===== 2. 經典例子 =====")
    a, b = "ABCABBA", "CBABAC"
    d1 = distance(diff_lcs(a, b))
    d2 = distance(myers_diff(a, b))
    print(f"  a = {a}, b = {b}（Myers 論文宣稱最小編輯距離 = 5）")
    print(f"  LCS/DP 算出 D = {d1}   Myers O(ND) 算出 D = {d2}   一致：{d1 == d2 == 5}\n")

    def bench(label, a, b):
        t0 = time.perf_counter()
        d1 = distance(diff_lcs(a, b))
        t1 = time.perf_counter()
        d2 = distance(myers_diff(a, b))
        t2 = time.perf_counter()
        print(f"  {label:<28} D={d2:<4} "
              f"LCS/DP {t1 - t0:8.4f}s   Myers {t2 - t1:8.4f}s   距離一致：{d1 == d2}")

    print("===== 3. 效能比較（n = m = 3000 行）=====")
    n = 3000

    base = [rand_str(40, "abcdefghij") for _ in range(n)]

    # 情境 A：只改 20 行（D 很小，接近一般 git diff 情境）
    a = list(base)
    b = list(base)
    for i in random.sample(range(n), 10):
        b[i] = rand_str(40, "abcdefghij")          # 10 個修改 = 10 刪 + 10 插
    bench("A. 小差異（改 20 行）", a, b)

    # 情境 B：整份重寫（D 接近 n+m）
    a = [rand_str(40, "abcdefghij") for _ in range(n)]
    b = [rand_str(40, "abcdefghij") for _ in range(n)]
    bench("B. 大差異（幾乎全改）", a, b)

    # 情境 C：中等差異
    a = list(base)
    b = list(base)
    for i in random.sample(range(n), n // 2):
        b[i] = rand_str(40, "abcdefghij")
    bench("C. 中差異（改 1500 行）", a, b)


if __name__ == "__main__":
    main()
