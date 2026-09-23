# 求解四個遞迴方程式，並用程式驗證閉合公式是否正確

def T1(n):
    # T(n) = T(n-1) + 8, T(1) = 1
    t = 1
    for _ in range(2, n + 1):
        t += 8
    return t

def formula1(n):
    # 閉合公式：T(n) = 8n - 7
    return 8 * n - 7


def T2(n):
    # T(n) = 2 T(n-1) + 9, T(1) = 1
    t = 1
    for _ in range(2, n + 1):
        t = 2 * t + 9
    return t

def formula2(n):
    # 閉合公式：T(n) = 10 * 2^(n-1) - 9
    return 10 * 2 ** (n - 1) - 9


def T3(n):
    # T(n) = 2 T(n/2) + 1, T(1) = 1  (n 為 2 的冪)
    t = 1
    m = 1
    while m < n:
        t = 2 * t + 1
        m *= 2
    return t

def formula3(n):
    # 閉合公式：T(n) = 2n - 1
    return 2 * n - 1


def T4(n):
    # T(n) = T(n/2) + 1, T(1) = 1  (n 為 2 的冪)
    t = 1
    m = 1
    while m < n:
        t += 1
        m *= 2
    return t

def formula4(n):
    # 閉合公式：T(n) = log2(n) + 1
    return n.bit_length()  # = 下取整(log2 n) + 1


if __name__ == "__main__":
    print("驗證閉合公式（n 取幾個值）\n")
    for n in [2, 4, 8, 16, 100]:
        ok1 = T1(n) == formula1(n)
        ok2 = T2(n) == formula2(n)
        print(f"n={n:4d}  T1 遞迴={T1(n):4d} 公式={formula1(n):4d} 相符={ok1}   "
              f"T2 遞迴={T2(n)} 公式={formula2(n)} 相符={ok2}")
    for n in [2, 4, 8, 16, 1024]:
        ok3 = T3(n) == formula3(n)
        ok4 = T4(n) == formula4(n)
        print(f"n={n:4d}  T3 遞迴={T3(n):4d} 公式={formula3(n):4d} 相符={ok3}   "
              f"T4 遞迴={T4(n):4d} 公式={formula4(n):4d} 相符={ok4}")

    print("\n解法與複雜度：")
    print("1. T(n) = T(n-1) + 8,  T(1)=1  =>  T(n) = 8n - 7            => O(n)")
    print("2. T(n) = 2T(n-1) + 9,  T(1)=1  =>  T(n) = 10*2^(n-1) - 9   => O(2^n)")
    print("3. T(n) = 2T(n/2) + 1,  T(1)=1  =>  T(n) = 2n - 1           => O(n)")
    print("4. T(n) = T(n/2) + 1,   T(1)=1  =>  T(n) = log2(n) + 1      => O(log n)")