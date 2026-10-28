"""
旅行推銷員問題（TSP） - 改良法（2-opt）
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

def greedy(start=0):
    unvisited = set(range(N_CITIES)) - {start}
    tour = [start]
    while unvisited:
        nxt = min(unvisited, key=lambda c: DIST[tour[-1], c])
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour

def two_opt_improve(init=None):
    tour = list(init) if init else greedy()
    n = len(tour)
    improved = True
    while improved:
        improved = False
        best_delta, best_ij = -1e-9, None
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b = tour[i], tour[i + 1]
                c, d = tour[j], tour[(j + 1) % n]
                delta = DIST[a, c] + DIST[b, d] - DIST[a, b] - DIST[c, d]
                if delta < best_delta:
                    best_delta, best_ij = delta, (i, j)
        if best_ij:
            i, j = best_ij
            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
            improved = True
    return tour

if __name__ == "__main__":
    t0 = time.time()
    tour = two_opt_improve()
    L = tour_length(tour)
    print("=== 改良法（2-opt） ===")
    print(f"路徑長度: {L:.2f}")
    print(f"耗時: {time.time()-t0:.6f}s")
    print(f"路徑: {tour}")
