"""
第 4 題：用蒙地卡羅法計算 n 變數積分（超體積）

  ∫_Ω f(x) dx ≈ Vol(Ω) * (1/N) * Σ f(x_i)，  x_i 在超矩形 Ω 中均勻隨機取樣

  優點：誤差約為 O(1/√N)，跟維度 n 無關，所以高維時比格點法好用很多
"""
import math
import random


def mc_integral_nd(f, low, high, N=100000):
    n = len(low)
    vol = math.prod(high[i] - low[i] for i in range(n))
    total = 0.0
    for _ in range(N):
        x = [random.uniform(low[i], high[i]) for i in range(n)]
        total += f(x)
    return vol * total / N


def ball_volume_exact(n, r=1.0):
    """n 維球體積公式 V_n = π^(n/2) / Γ(n/2 + 1) * r^n"""
    return math.pi ** (n / 2) / math.gamma(n / 2 + 1) * r ** n


if __name__ == "__main__":
    random.seed(42)
    ball = lambda p: 1.0 if sum(t * t for t in p) <= 1 else 0.0

    print("=== n 維單位球體積（投點計算比例） ===")
    for n in [2, 3, 4, 5, 6, 8, 10]:
        est = mc_integral_nd(ball, [-1] * n, [1] * n, 200000)
        print(f"  n = {n:>2}   蒙地卡羅 = {est:.5f}   理論值 = {ball_volume_exact(n):.5f}")

    print("\n=== 其他函數 ===")
    # ∫ (x1² + ... + x10²) over [0,1]^10 = 10/3
    f = lambda p: sum(t * t for t in p)
    print(f"  ∫ Σx_i² over [0,1]^10   = {mc_integral_nd(f, [0]*10, [1]*10, 200000):.5f}   理論值 {10/3:.5f}")

    # ∫ exp(-(x²+y²)) over [-3,3]^2 ≈ π
    g = lambda p: math.exp(-(p[0] ** 2 + p[1] ** 2))
    print(f"  ∫ e^-(x²+y²) over [-3,3]² = {mc_integral_nd(g, [-3,-3], [3,3], 200000):.5f}   理論值 ≈ π = {math.pi:.5f}")