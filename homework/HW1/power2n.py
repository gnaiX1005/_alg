import time
import signal

# 方法 1：直接用 **
def power2n_1(n):
    return 2 ** n

# 方法 2a：遞迴，power2n(n-1)+power2n(n-1)
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

# 方法 2b：遞迴，2*power2n(n-1)
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：遞迴 + 查表（memoization）
table = {0: 1}
def power2n_3(n):
    if n in table:
        return table[n]
    table[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return table[n]


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("超出時間限制")


def test(name, fn, n, expect, limit=None):
    if limit:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(limit)
    start = time.perf_counter()
    try:
        result = fn(n)
        elapsed = time.perf_counter() - start
        ok = result == expect
        print(f"{name:18s} 結果={result} 正確={ok} 耗時={elapsed:.6f}s")
    except TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"{name:18s} n={n} 超出 {limit} 秒，跑不出來（時間複雜度太高）")
    except RecursionError:
        elapsed = time.perf_counter() - start
        print(f"{name:18s} n={n} 遞迴深度超過限制")
    finally:
        if limit:
            signal.alarm(0)
    return


if __name__ == "__main__":
    n = 100
    expect = 2 ** n
    print(f"測試 n = {n}（預期結果 = 2**100）\n")
    test("方法1 (2**n)", power2n_1, n, expect)
    test("方法2a (+遞迴)", power2n_2a, n, expect, limit=5)
    test("方法2b (*遞迴)", power2n_2b, n, expect)
    test("方法3 (查表)", power2n_3, n, expect)

    print("\n結論：")
    print("  方法1: 直接 2**n，O(1)，瞬間完成")
    print("  方法2a: 每次分裂成兩個呼叫，O(2^n)，n=100 根本跑不完")
    print("  方法2b: 每次只遞迴一次，O(n)，很快")
    print("  方法3: 查表記錄算過的結果，O(n)，一樣快")