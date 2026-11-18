"""
改用蒙地卡羅法做 n 變數積分，題目同上一題
  f(x) = x1² + x2² + ... + xn²，low = 0，high = 1，n = 1, 2, 5, 100
  理論值 = n / 3

蒙地卡羅法：
  ∫_Ω f(x) dx ≈ Vol(Ω) * (1/N) * Σ f(x_i)，x_i 在 Ω 內均勻隨機取樣
  誤差約為 σ/√N，跟維度 n 沒有直接關係，所以高維也算得動。
"""
import math
import random


def integral(f, low, high, N=100000):
    n = len(low)
    vol = math.prod(high[i] - low[i] for i in range(n))
    total = 0.0
    for _ in range(N):
        x = [random.uniform(low[i], high[i]) for i in range(n)]
        total += f(x)
    return vol * total / N


def f(x):
    return sum(t * t for t in x)


if __name__ == "__main__":
    random.seed(42)
    N = 100000
    print(f"f(x) = x1² + ... + xn²，low = 0，high = 1，理論值 = n/3，取樣 N = {N:,}\n")
    for n in [1, 2, 5, 100]:
        r = integral(f, [0] * n, [1] * n, N)
        exact = n / 3
        print(f"n = {n:>3}  蒙地卡羅 = {r:.6f}   理論值 = {exact:.6f}   "
              f"誤差 = {abs(r - exact):.2e}   相對誤差 = {abs(r - exact) / exact:.3%}")

    print("""
說明：
  每一維 x² 的變異數是 1/5 - 1/9 = 4/45，n 維 f 的標準差 σ = √(4n/45)，
  所以估計誤差約 σ/√N：n=100 時約 0.0094（相對誤差約 0.03%），
  每次實際跑出的誤差會在這個量級上下浮動。
  跟黎曼積分在 100 維只能得到 25（誤差 8.3）相比，蒙地卡羅在高維明顯好用。""")