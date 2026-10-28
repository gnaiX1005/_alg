"""
旅行推銷員問題（TSP） - 模擬退火法（Simulated Annealing）
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

def simulated_annealing(T0=100.0, T_end=1e-3, alpha=0.995, per_temp=100, seed=1):
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    best, best_len = tour[:], cur
    T = T0
    while T > T_end:
        for _ in range(per_temp):
            i, j = sorted(r.sample(range(N_CITIES), 2))
            cand = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
            new = tour_length(cand)
            d = new - cur
            if d < 0 or r.random() < math.exp(-d / T):
                tour, cur = cand, new
                if cur < best_len:
                    best, best_len = tour[:], cur
        T *= alpha
    return best

if __name__ == "__main__":
    t0 = time.time()
    tour = simulated_annealing()
    L = tour_length(tour)
    print("=== 模擬退火法（Simulated Annealing） ===")
    print(f"路徑長度: {L:.2f}")
    print(f"耗時: {time.time()-t0:.6f}s")
    print(f"路徑: {tour}")
