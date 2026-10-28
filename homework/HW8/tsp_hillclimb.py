"""
旅行推銷員問題（TSP） - 爬山演算法（Hill Climbing）
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

def hill_climbing(iters=20000, seed=1):
    r = random.Random(seed)
    tour = list(range(N_CITIES))
    r.shuffle(tour)
    cur = tour_length(tour)
    for _ in range(iters):
        i, j = r.sample(range(N_CITIES), 2)
        tour[i], tour[j] = tour[j], tour[i]
        new = tour_length(tour)
        if new < cur:
            cur = new
        else:
            tour[i], tour[j] = tour[j], tour[i]
    return tour

if __name__ == "__main__":
    t0 = time.time()
    tour = hill_climbing()
    L = tour_length(tour)
    print("=== 爬山演算法（Hill Climbing） ===")
    print(f"路徑長度: {L:.2f}")
    print(f"耗時: {time.time()-t0:.6f}s")
    print(f"路徑: {tour}")
