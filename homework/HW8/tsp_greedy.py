"""
旅行推銷員問題（TSP） - 貪婪演算法（最近鄰居法）
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

if __name__ == "__main__":
    t0 = time.time()
    tour = greedy()
    L = tour_length(tour)
    print("=== 貪婪演算法（最近鄰居法） ===")
    print(f"路徑長度: {L:.2f}")
    print(f"耗時: {time.time()-t0:.6f}s")
    print(f"路徑: {tour}")
