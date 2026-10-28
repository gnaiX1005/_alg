# 第7週習題：優化算法 — 旅行推銷員問題（TSP）

我用 opencode

作業要求分別用下列五種方法，解決旅行推銷員問題：

1. 改良法（2-opt）
2. 爬山演算法（Hill Climbing）
3. 模擬退火法（Simulated Annealing）
4. 梯度下降法（Gradient Descent，連續鬆弛）
5. 貪婪演算法（最近鄰居）

測試資料使用 20 個隨機城市（固定亂數種子 42），所有方法使用同一組資料進行比較。

## 1. 我的理解

旅行推銷員問題（TSP）是給定 $n$ 個城市與任兩城市間的距離，求一條**每個城市恰好造訪一次、最後回到起點**的最短路徑（哈密頓迴路）。

## 2. 程式原理

### `tsp_greedy.py`（貪婪演算法 — 最近鄰居法）
- 從起點出發，每一步都走向「目前位置最近、且尚未造訪」的城市，直到全部走完再回到起點。
- 特性：速度極快，但只做局部最優選擇，整體不保證最佳。

### `tsp_twoopt.py`（改良法 — 2-opt）
- 以貪婪演算法的結果為初始解，反覆對路徑做 2-opt 調整：取兩條邊 $(a,b),(c,d)$，將中間路段反轉成 $(a,c),(b,d)$。
- 若新路徑更短（$\Delta < 0$）就採用，直到找不到任何改善為止。
- 能有效消除路徑交叉，品質大幅提升。

### `tsp_hillclimb.py`（爬山演算法）
- 隨機產生初始路徑，每次隨機交換兩個城市產生鄰居解。
- 只接受「比較短」的解，若較差則還原。
- 容易停在局部最佳解，無法逃脫。

### `tsp_sa.py`（模擬退火法）
- 源自金屬退火原理，高溫時允許接受較差解以探索空間，隨溫度降低逐漸只接受較好解。
- 使用 Metropolis 準則：$\Delta<0$ 一定接受，$\Delta>=0$ 則以 $e^{-\Delta/T}$ 機率接受。
- 採用 2-opt 鄰域並持續記錄歷史最佳解，有機會逃離局部最佳。

### `tsp_gd.py`（梯度下降法 — 連續鬆弛）
- 將離散的排列問題鬆弛為連續機率矩陣 $P \in \mathbb{R}^{n\times n}$，其中 $P_{k,i}$ 表示第 $k$ 步造訪城市 $i$ 的機率。
- 目標函數包含期望路徑長度與懲罰項（確保每個城市恰好造訪一次）。
- 對 $W$（經 row-softmax 得到 $P$）進行梯度下降優化，最後以貪婪方式解碼回合法路徑。

## 3. 執行方式

```bash
pip install numpy

python tsp_greedy.py
python tsp_twoopt.py
python tsp_hillclimb.py
python tsp_sa.py
python tsp_gd.py
```

整合比較：
```bash
python tsp.py
```

## 4. 參考

- [原始參考解答（week7-tsp）](https://github.com/ccc115a/alg/tree/main/_more/homework/week7-tsp)
- [Claude 分享連結](https://claude.ai/share/36c286d7-0b9d-4e67-8684-76733347dffc)
