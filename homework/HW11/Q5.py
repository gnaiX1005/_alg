"""
第 5 題：用黎曼積分法寫函數 integral(f, low, high) 來做 n 變數積分
        n = len(low) = len(high)
        分別用 1 維、2 維、5 維、100 維計算
        範例：f(x) = x1² + x2² + ... + xn²，low = 0，high = 1

理論值：∫_[0,1]^n Σ x_i² dx = n * ∫_0^1 x² dx = n / 3
"""
import math


def integral(f, low, high, budget=10**6):
    """
    n 維黎曼積分（中點法）。
    每一維切 m 等分，總共要算 m^n 個點；
    m 由「最多算 budget 個點」自動決定：m = floor(budget^(1/n))，至少 1。
    用遞迴：固定第 d 維的值，再對後面的維度做黎曼和。
    """
    n = len(low)
    m = max(1, int(round(budget ** (1 / n), 9)))   # round 避免 1000000**(1/2)=999.999…
    h = [(high[i] - low[i]) / m for i in range(n)]
    x = [0.0] * n

    def rec(d):
        if d == n:
            return f(x)
        s = 0.0
        for k in range(m):
            x[d] = low[d] + (k + 0.5) * h[d]   # 取每個小區間的中點
            s += rec(d + 1)
        return s * h[d]

    return rec(0), m


def f(x):
    return sum(t * t for t in x)


if __name__ == "__main__":
    print("f(x) = x1² + ... + xn²，low = 0，high = 1，理論值 = n/3\n")
    for n in [1, 2, 5, 100]:
        r, m = integral(f, [0] * n, [1] * n)
        exact = n / 3
        print(f"n = {n:>3}  每維切 {m:>7} 等分 (共 {m**n:,} 個點)  "
              f"黎曼積分 = {r:.8f}   理論值 = {exact:.8f}   誤差 = {abs(r - exact):.2e}")

    print("""
說明：
  中點法對 x² 每一維的誤差是 1/(12 m²)，n 維總誤差 = n/(12 m²)。
  1、2、5 維都能切得夠細，所以很準。
  100 維就算每維只切 2 等分也要 2^100 ≈ 1.27e30 個點，算不完（維度災難），
  在 100 萬個點的預算下每維只能切 1 等分，得到 100 × 0.25 = 25，誤差很大。
  → 這就是高維積分要改用蒙地卡羅法的原因（見 q6_montecarlo_nd.py）。""")