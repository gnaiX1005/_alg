"""
第 2 題：用蒙地卡羅法計算單變數積分

  方法一（平均值法）：
      ∫_a^b f(x) dx ≈ (b - a) * (1/N) * Σ f(x_i)，  x_i ~ Uniform(a, b)

  方法二（投點法 hit-or-miss，限 0 <= f(x) <= ymax）：
      在 [a,b] x [0,ymax] 的矩形內隨機投點，
      落在曲線下方的比例 * 矩形面積 ≈ 積分值
"""
import math
import random


def mc_integral(f, a, b, n=100000):
    """平均值法"""
    total = 0.0
    for _ in range(n):
        total += f(random.uniform(a, b))
    return (b - a) * total / n


def mc_integral_hit(f, a, b, ymax, n=100000):
    """投點法（hit-or-miss）"""
    hit = 0
    for _ in range(n):
        x = random.uniform(a, b)
        y = random.uniform(0, ymax)
        if y <= f(x):
            hit += 1
    return (b - a) * ymax * hit / n


if __name__ == "__main__":
    random.seed(42)
    print("∫_0^π sin(x) dx，理論值 = 2")
    for n in [100, 1000, 10000, 100000, 1000000]:
        print(f"  N = {n:>7}  平均值法 = {mc_integral(math.sin, 0, math.pi, n):.6f}"
              f"   投點法 = {mc_integral_hit(math.sin, 0, math.pi, 1, n):.6f}")

    print("\n∫_0^1 x^2 dx，理論值 = 0.333333")
    print(f"  N = 1000000  平均值法 = {mc_integral(lambda x: x * x, 0, 1, 1000000):.6f}")

    print("\n∫_0^1 4/(1+x^2) dx，理論值 = π =", math.pi)
    print(f"  N = 1000000  平均值法 = {mc_integral(lambda x: 4 / (1 + x * x), 0, 1, 1000000):.6f}")
    print("\n（誤差大約跟 1/√N 成正比：N 變 100 倍，誤差約變成 1/10）")