"""
旅行推銷員問題（TSP） - 梯度下降法（連續鬆弛）
"""
import math
import random
import time
import numpy as np

N_CITIES = 20
rng = random.Random(42)
CITIES = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(N_CITIES)]
DIST = np.array([[math.dist(a, b) for b in CITIES] for a in CITIES])

def tour_length(tour):
    return sum(DIST[tour[i], tour[(i + 1) % len(tour)]] for i in range(len(tour)))

def gradient_descent(steps=3000, lr=0.05, lam=30.0, seed=1):
    n = N_CITIES
    r = np.random.default_rng(seed)
    W = r.normal(0, 0.1, (n, n))
    Dn = DIST / DIST.mean()

    def softmax(x):
        e = np.exp(x - x.max(axis=1, keepdims=True))
        return e / e.sum(axis=1, keepdims=True)

    for t in range(steps):
        P = softmax(W)
        nxt, prv = np.roll(P, -1, axis=0), np.roll(P, 1, axis=0)
        gP = nxt @ Dn + prv @ Dn
        col = P.sum(axis=0) - 1.0
        gP += 2 * lam * col[None, :]
        gW = P * (gP - (gP * P).sum(axis=1, keepdims=True))
        W -= lr * (1 - t / steps * 0.9) * gW * 10

    P = softmax(W)
    tour = [-1] * n
    Pm = P.copy()
    for _ in range(n):
        k, i = np.unravel_index(np.argmax(Pm), Pm.shape)
        tour[k] = int(i)
        Pm[k, :] = -1
        Pm[:, i] = -1
    return tour

if __name__ == "__main__":
    t0 = time.time()
    tour = gradient_descent()
    L = tour_length(tour)
    print("=== 梯度下降法（連續鬆弛） ===")
    print(f"路徑長度: {L:.2f}")
    print(f"耗時: {time.time()-t0:.6f}s")
    print(f"路徑: {tour}")
