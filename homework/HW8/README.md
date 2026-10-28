# 第7週習題：優化算法 — 旅行推銷員問題（TSP）

使用下列五種方法解決旅行推銷員問題：

1. 改良法（2-opt） - `tsp_twoopt.py`
2. 爬山演算法（Hill Climbing） - `tsp_hillclimb.py`
3. 模擬退火法（Simulated Annealing） - `tsp_sa.py`
4. 梯度下降法（Gradient Descent，連續鬆弛） - `tsp_gd.py`
5. 貪婪演算法（最近鄰居） - `tsp_greedy.py`

## 測試資料

- 20 個城市，座標隨機產生（固定亂數種子 42）
- 所有程式使用同一組資料

## 執行方式

```bash
pip install numpy

python tsp_greedy.py
python tsp_twoopt.py
python tsp_hillclimb.py
python tsp_sa.py
python tsp_gd.py
```

也可使用整合版：
```bash
python tsp.py
```

## 參考

- [原始參考解答](https://github.com/ccc115a/alg/tree/main/_more/homework/week7-tsp)
