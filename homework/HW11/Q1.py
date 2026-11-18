"""
第 1 題：用數值方法計算單變數微分與積分
  - 微分：前向差分、中央差分
  - 積分：黎曼和（中點法）、梯形法、Simpson 法
"""
import math


# ---------- 微分 ----------
def diff_forward(f, x, h=1e-6):
    """前向差分 f'(x) ≈ (f(x+h) - f(x)) / h，誤差 O(h)"""
    return (f(x + h) - f(x)) / h


def diff_central(f, x, h=1e-5):
    """中央差分 f'(x) ≈ (f(x+h) - f(x-h)) / 2h，誤差 O(h^2)"""
    return (f(x + h) - f(x - h)) / (2 * h)


# ---------- 積分 ----------
def integral_riemann(f, a, b, n=10000):
    """黎曼和（取每個小區間的中點）"""
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h


def integral_trapezoid(f, a, b, n=10000):
    """梯形法"""
    h = (b - a) / n
    s = (f(a) + f(b)) / 2 + sum(f(a + i * h) for i in range(1, n))
    return s * h


def integral_simpson(f, a, b, n=10000):
    """Simpson 法（n 必須為偶數）"""
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    s += 4 * sum(f(a + i * h) for i in range(1, n, 2))
    s += 2 * sum(f(a + i * h) for i in range(2, n, 2))
    return s * h / 3


if __name__ == "__main__":
    print("=== 微分 ===")
    # f(x) = sin(x)，f'(1) = cos(1)
    print(f"d/dx sin(x) at x=1   前向差分 = {diff_forward(math.sin, 1):.10f}")
    print(f"                     中央差分 = {diff_central(math.sin, 1):.10f}")
    print(f"                     理論值   = {math.cos(1):.10f}")

    # f(x) = x^3，f'(2) = 12
    cube = lambda x: x ** 3
    print(f"d/dx x^3 at x=2      中央差分 = {diff_central(cube, 2):.10f}   (理論值 12)")

    print("\n=== 積分 ===")
    # ∫_0^π sin(x) dx = 2
    print(f"∫_0^π sin(x) dx  黎曼和 = {integral_riemann(math.sin, 0, math.pi):.10f}")
    print(f"                 梯形法 = {integral_trapezoid(math.sin, 0, math.pi):.10f}")
    print(f"                 Simpson = {integral_simpson(math.sin, 0, math.pi):.10f}")
    print(f"                 理論值 = 2")

    # ∫_0^1 x^2 dx = 1/3
    sq = lambda x: x * x
    print(f"∫_0^1 x^2 dx     黎曼和 = {integral_riemann(sq, 0, 1):.10f}   (理論值 {1/3:.10f})")