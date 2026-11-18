"""
第 3 題：用數值方法計算 n 變數微分（梯度）與積分（超體積）
  - 梯度：對每個變數做中央差分
  - 積分：把每一維切成 m 等分，在每個小超立方體的中點取值（多維黎曼和）
"""
import math
import itertools


# ---------- 偏微分與梯度 ----------
def partial(f, x, i, h=1e-5):
    """f 對第 i 個變數的偏微分（中央差分）"""
    x1 = list(x); x1[i] += h
    x2 = list(x); x2[i] -= h
    return (f(x1) - f(x2)) / (2 * h)


def gradient(f, x, h=1e-5):
    """梯度 ∇f(x) = [∂f/∂x_0, ∂f/∂x_1, ..., ∂f/∂x_{n-1}]"""
    return [partial(f, x, i, h) for i in range(len(x))]


# ---------- n 維積分（超體積） ----------
def integral_nd(f, low, high, m=20):
    """
    在超矩形 [low[0],high[0]] x ... x [low[n-1],high[n-1]] 上積分 f
    每一維切 m 等分，總共要算 m^n 個點
    """
    n = len(low)
    h = [(high[i] - low[i]) / m for i in range(n)]
    dv = math.prod(h)                       # 每個小格子的體積
    total = 0.0
    for idx in itertools.product(range(m), repeat=n):
        x = [low[i] + (idx[i] + 0.5) * h[i] for i in range(n)]
        total += f(x)
    return total * dv


if __name__ == "__main__":
    print("=== 梯度 ===")
    # f(x,y,z) = x^2 + y^2 + z^2，∇f = (2x, 2y, 2z)
    f1 = lambda p: p[0] ** 2 + p[1] ** 2 + p[2] ** 2
    g = gradient(f1, [1, 2, 3])
    print(f"f = x²+y²+z², ∇f(1,2,3) = {[round(v, 6) for v in g]}   理論值 [2, 4, 6]")

    # f(x,y) = x^2 * y + sin(y)，∇f = (2xy, x^2 + cos y)
    f2 = lambda p: p[0] ** 2 * p[1] + math.sin(p[1])
    g = gradient(f2, [2, 0])
    print(f"f = x²y+sin(y), ∇f(2,0) = {[round(v, 6) for v in g]}   理論值 [0, 5]")

    print("\n=== n 維積分（超體積） ===")
    # ∫∫ (x+y) dx dy over [0,1]^2 = 1
    r = integral_nd(lambda p: p[0] + p[1], [0, 0], [1, 1], m=100)
    print(f"∫∫(x+y) over [0,1]²            = {r:.6f}   理論值 1")

    # ∫∫∫ (x²+y²+z²) over [0,1]^3 = 1
    r = integral_nd(f1, [0, 0, 0], [1, 1, 1], m=50)
    print(f"∫∫∫(x²+y²+z²) over [0,1]³      = {r:.6f}   理論值 1")

    # 單位球體積：在 [-1,1]^3 上積分「點在球內 = 1，否則 0」
    ball = lambda p: 1.0 if sum(t * t for t in p) <= 1 else 0.0
    r = integral_nd(ball, [-1, -1, -1], [1, 1, 1], m=100)
    print(f"三維單位球體積                  = {r:.6f}   理論值 4π/3 = {4 * math.pi / 3:.6f}")